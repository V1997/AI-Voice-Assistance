import json
import re
from typing import List, Dict, Any
import os

class AvenDataPreprocessor:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.processed_data = []
        self.filtered_data = []
    
    def load_data(self) -> List[Dict[str, Any]]:
        """Load the JSON data from file"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data[0]['page_info'] if data else []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
    
    def filter_relevant_content(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out irrelevant content and keep only Aven-related data"""
        relevant_data = []
        
        for item in raw_data:
            url = item.get('url', '')
            title = item.get('title', '')
            content = item.get('content', '')
            
            # Skip empty content
            if not content or content.strip() == "":
                continue
            
            # Skip network interference messages
            if "network appears to interfere" in content.lower():
                continue
            
            # Skip non-Aven domains
            if url and 'aven.com' not in url.lower():
                continue
            
            # Skip staging/development URLs
            if 'staging' in url.lower():
                continue
            
            # Skip internal/crypto pages
            if 'internal/crypto' in url.lower():
                continue
            
            # Skip empty titles for non-document pages
            if not title and not url.endswith('.pdf'):
                continue
            
            relevant_data.append(item)
        
        return relevant_data
    
    def clean_content(self, content: str) -> str:
        """Clean and normalize content for embedding generation"""
        if not content:
            return ""
        
        # Remove extra whitespace and normalize
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Remove common web artifacts
        content = re.sub(r'\n+', ' ', content)
        content = re.sub(r'\t+', ' ', content)
        
        # Remove HTML-like tags if any
        content = re.sub(r'<[^>]+>', '', content)
        
        # Clean up special characters but keep important ones
        content = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)\$\%]', '', content)
        
        # Remove empty content
        if not content or content.isspace():
            return ""
        
        return content
    
    def categorize_content(self, url: str, title: str, content: str) -> str:
        """Categorize content based on URL and title"""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if 'education' in url_lower or 'education' in title_lower:
            return 'education'
        elif 'support' in url_lower or 'help' in title_lower:
            return 'support'
        elif '.pdf' in url_lower or 'docs' in url_lower:
            return 'legal_document'
        elif 'privacy' in url_lower or 'privacy' in title_lower:
            return 'privacy_policy'
        elif 'login' in url_lower or 'my.aven' in url_lower:
            return 'account_management'
        elif 'join' in url_lower:
            return 'signup'
        else:
            return 'product_info'
    
    def extract_financial_info(self, content: str) -> Dict[str, Any]:
        """Extract key financial information from content"""
        # Extract fees mentioned
        fees = re.findall(r'\$[\d,]+\.?\d*', content)
        
        # Extract percentages
        percentages = re.findall(r'\d+\.?\d*%', content)
        
        # Extract phone numbers
        phone_numbers = re.findall(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', content)
        
        # Extract email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        
        # Extract specific financial terms
        financial_terms = []
        if 'cash back' in content.lower():
            financial_terms.append('cash_back')
        if 'home equity' in content.lower():
            financial_terms.append('home_equity')
        if 'heloc' in content.lower():
            financial_terms.append('heloc')
        if 'credit card' in content.lower():
            financial_terms.append('credit_card')
        if 'balance transfer' in content.lower():
            financial_terms.append('balance_transfer')
        
        return {
            'fees': fees,
            'percentages': percentages,
            'phone_numbers': phone_numbers,
            'emails': emails,
            'financial_terms': financial_terms
        }
    
    def chunk_content(self, content: str, min_chunk_size: int = 25, max_chunk_size: int = 50, overlap: int = 5) -> List[str]:
        """Split content into chunks for embedding generation"""
        # For now, just return the content as a single chunk
        # This avoids the complex chunking logic that was causing issues
        return [content]
    
    def process_data(self, min_chunk_size: int = 25, max_chunk_size: int = 50, overlap: int = 5) -> List[Dict[str, Any]]:
        """Process all data and return structured format for embeddings"""
        raw_data = self.load_data()
        
        # Filter relevant content
        print(f"Original data: {len(raw_data)} entries")
        filtered_data = self.filter_relevant_content(raw_data)
        print(f"Filtered data: {len(filtered_data)} relevant entries")
        
        for item in filtered_data:
            url = item.get('url', '')
            title = item.get('title', '')
            content = item.get('content', '')
            
            # Clean content
            cleaned_content = self.clean_content(content)
            
            # Skip if content is too short after cleaning
            if len(cleaned_content.split()) < 10:
                continue
            
            # Categorize content
            category = self.categorize_content(url, title, cleaned_content)
            
            # Extract financial information
            financial_info = self.extract_financial_info(cleaned_content)
            
            # Split into chunks
            chunks = self.chunk_content(cleaned_content, min_chunk_size, max_chunk_size, overlap)
            
            # Create processed items for each chunk
            for i, chunk in enumerate(chunks):
                # Create unique ID using URL and a unique counter
                unique_id = f"{url}_{len(self.processed_data)}"
                
                processed_item = {
                    'id': unique_id,
                    'content': chunk,
                    'metadata': {
                        'url': url,
                        'title': title,
                        'category': category,
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'chunk_size': len(chunk),
                        'word_count': len(chunk.split()),
                        'financial_info': financial_info
                    }
                }
                
                self.processed_data.append(processed_item)
        
        return self.processed_data
    
    def save_processed_data(self, output_file: str):
        """Save processed data to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.processed_data, f, indent=2, ensure_ascii=False)
            print(f"Processed data saved to {output_file}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not self.processed_data:
            return {}
        
        total_chunks = len(self.processed_data)
        total_words = sum(item['metadata']['word_count'] for item in self.processed_data)
        
        categories = {}
        financial_terms = {}
        
        for item in self.processed_data:
            category = item['metadata']['category']
            categories[category] = categories.get(category, 0) + 1
            
            # Count financial terms
            for term in item['metadata']['financial_info']['financial_terms']:
                financial_terms[term] = financial_terms.get(term, 0) + 1
        
        return {
            'total_chunks': total_chunks,
            'total_words': total_words,
            'avg_words_per_chunk': total_words / total_chunks if total_chunks > 0 else 0,
            'categories': categories,
            'financial_terms': financial_terms
        }

def main():
    # Initialize preprocessor
    preprocessor = AvenDataPreprocessor('firecrawl/documents_1.json')
    
    # Process data
    print("Processing Aven.com data for precise embedding generation...")
    processed_data = preprocessor.process_data(min_chunk_size=25, max_chunk_size=50, overlap=5)
    
    # Save processed data
    preprocessor.save_processed_data('aven_processed_data.json')
    
    # Generate and display summary
    summary = preprocessor.generate_summary()
    print("\n=== Aven Data Processing Summary ===")
    print(f"Total chunks created: {summary['total_chunks']}")
    print(f"Total words: {summary['total_words']:,}")
    print(f"Average words per chunk: {summary['avg_words_per_chunk']:.1f}")
    
    print("\nCategories:")
    for category, count in summary['categories'].items():
        print(f"  {category}: {count} chunks")
    
    print("\nFinancial terms found:")
    for term, count in summary['financial_terms'].items():
        print(f"  {term}: {count} occurrences")

if __name__ == "__main__":
    main() 