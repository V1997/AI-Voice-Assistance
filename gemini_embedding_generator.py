import json
import google.generativeai as genai
import numpy as np
from typing import List, Dict, Any
import os
from tqdm import tqdm
import time

class GeminiEmbeddingGenerator:
    def __init__(self, api_key: str = None, model: str = "models/embedding-001"):
        """
        Initialize the Gemini embedding generator
        
        Args:
            api_key: Google API key (if None, will try to get from environment)
            model: Embedding model to use
        """
        self.model = model
        
        # Set up Gemini client
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("Google API key not provided. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
            genai.configure(api_key=api_key)
    
    def load_processed_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load processed data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading processed data: {e}")
            return []
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text using Gemini"""
        try:
            result = genai.embed_content(content=text, model=self.model)
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 20) -> List[List[float]]:
        """Generate embeddings for a batch of texts"""
        embeddings = []
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings"):
            batch = texts[i:i + batch_size]
            
            try:
                # Process each text individually for now (simpler approach)
                batch_embeddings = []
                for text in batch:
                    result = genai.embed_content(content=text, model=self.model)
                    batch_embeddings.append(result['embedding'])
                
                embeddings.extend(batch_embeddings)
                
                # Add delay to avoid rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                print(f"Error generating batch embeddings: {e}")
                # If batch fails, try individual texts
                for text in batch:
                    embedding = self.generate_embedding(text)
                    embeddings.append(embedding)
                    time.sleep(0.1)  # Small delay between individual calls
        
        return embeddings
    
    def process_data_with_embeddings(self, processed_data: List[Dict[str, Any]], 
                                   batch_size: int = 20) -> List[Dict[str, Any]]:
        """Process data and add embeddings"""
        # Extract texts for embedding generation
        texts = [item['content'] for item in processed_data]
        
        print(f"Generating embeddings for {len(texts)} text chunks...")
        
        # Generate embeddings
        embeddings = self.generate_embeddings_batch(texts, batch_size)
        
        # Add embeddings to data
        for i, item in enumerate(processed_data):
            if i < len(embeddings):
                item['embedding'] = embeddings[i]
                item['embedding_model'] = self.model
                item['embedding_dimension'] = len(embeddings[i])
        
        return processed_data
    
    def save_embeddings(self, data_with_embeddings: List[Dict[str, Any]], 
                       output_file: str):
        """Save data with embeddings to file"""
        try:
            # Convert numpy arrays to lists for JSON serialization
            for item in data_with_embeddings:
                if 'embedding' in item and isinstance(item['embedding'], np.ndarray):
                    item['embedding'] = item['embedding'].tolist()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data_with_embeddings, f, indent=2, ensure_ascii=False)
            print(f"Embeddings saved to {output_file}")
        except Exception as e:
            print(f"Error saving embeddings: {e}")
    
    def generate_summary(self, data_with_embeddings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of embedding generation"""
        if not data_with_embeddings:
            return {}
        
        total_items = len(data_with_embeddings)
        items_with_embeddings = sum(1 for item in data_with_embeddings if 'embedding' in item)
        
        embedding_dimensions = []
        categories = {}
        
        for item in data_with_embeddings:
            if 'embedding' in item:
                embedding_dimensions.append(len(item['embedding']))
            
            # Count categories
            category = item['metadata']['category']
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_items': total_items,
            'items_with_embeddings': items_with_embeddings,
            'embedding_success_rate': items_with_embeddings / total_items if total_items > 0 else 0,
            'embedding_dimension': embedding_dimensions[0] if embedding_dimensions else 0,
            'model_used': self.model,
            'categories': categories
        }

def main():
    # Check if API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your Google API key as an environment variable:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        return
    
    # Initialize embedding generator
    generator = GeminiEmbeddingGenerator(model="models/embedding-001")
    
    # Load processed data
    print("Loading processed Aven.com data...")
    processed_data = generator.load_processed_data('aven_processed_data.json')
    
    if not processed_data:
        print("No processed data found. Please run data_preprocessor.py first.")
        return
    
    # Generate embeddings
    print(f"Processing {len(processed_data)} items...")
    data_with_embeddings = generator.process_data_with_embeddings(processed_data, batch_size=20)
    
    # Save embeddings
    generator.save_embeddings(data_with_embeddings, 'aven_embeddings_data.json')
    
    # Generate and display summary
    summary = generator.generate_summary(data_with_embeddings)
    print("\n=== Embedding Generation Summary ===")
    print(f"Total items: {summary['total_items']}")
    print(f"Items with embeddings: {summary['items_with_embeddings']}")
    print(f"Success rate: {summary['embedding_success_rate']:.2%}")
    print(f"Embedding dimension: {summary['embedding_dimension']}")
    print(f"Model used: {summary['model_used']}")
    
    print("\nCategories processed:")
    for category, count in summary['categories'].items():
        print(f"  {category}: {count} items")

if __name__ == "__main__":
    main() 