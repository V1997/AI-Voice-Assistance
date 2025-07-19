import chromadb
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AvenChromaDBIntegration:
    def __init__(self):
        """
        Initialize ChromaDB Cloud integration for Aven data
        """
        chroma_api_key = os.getenv('CHROMA_API_KEY')
        chroma_tenant = os.getenv('CHROMA_TENANT')
        chroma_database = os.getenv('CHROMA_DATABASE')
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not chroma_api_key:
            raise ValueError("CHROMA_API_KEY not found in environment variables. Please add it to your .env file.")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")
        self.client = chromadb.CloudClient(
            api_key=chroma_api_key,
            tenant=chroma_tenant,
            database=chroma_database
        )
        print("✓ Connected to ChromaDB Cloud (CloudClient)")
        self.google_api_key = google_api_key

    def load_processed_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load processed data from JSON file (raw docs + metadata)"""
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading processed data: {e}")
            return []

    def create_collection(self, collection_name: str = "aven_financial_products"):
        """Get or create a ChromaDB collection. Embedding model is set in Chroma Cloud UI."""
        collection = self.client.get_or_create_collection(
            name=collection_name
        )
        print(f"Using collection: {collection_name} (embedding model set in Chroma Cloud UI)")
        return collection

    def insert_data_into_chroma(self, collection, processed_data: List[Dict[str, Any]], batch_size: int = 50):
        """Insert raw docs and metadata into ChromaDB collection (no embeddings)"""
        ids = []
        documents = []
        metadatas = []
        for item in processed_data:
            ids.append(item['id'])
            documents.append(item['content'])
            # Use only simple, flat metadata
            metadata = {
                'url': item['metadata']['url'],
                'title': item['metadata']['title'],
                'category': item['metadata']['category'],
                'word_count': item['metadata']['word_count']
            }
            metadatas.append(metadata)
        print(f"Inserting {len(ids)} items into ChromaDB (embedding handled by Chroma Cloud)...")
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i+batch_size]
            batch_docs = documents[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metadatas
            )

    def get_collection_stats(self, collection):
        """Get statistics about the collection"""
        try:
            count = collection.count()
            all_results = collection.get()
            categories = {}
            if all_results['metadatas']:
                for metadata in all_results['metadatas']:
                    category = metadata.get('category', 'unknown')
                    categories[category] = categories.get(category, 0) + 1
            return {
                'total_items': count,
                'categories': categories,
                'collection_name': collection.name
            }
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {}

    def query_collection(self, collection, query_text: str, n_results: int = 5):
        """Query the collection for similar documents (semantic search)"""
        try:
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error querying collection: {e}")
            return {}

def main():
    # Initialize ChromaDB Cloud integration
    chroma_integration = AvenChromaDBIntegration()
    
    # Load processed data
    print("Loading Aven processed data...")
    processed_data = chroma_integration.load_processed_data('aven_processed_data.json')
    
    if not processed_data:
        print("No processed data found. Please run gemini_embedding_generator.py first.")
        return
    
    # Create or get collection
    collection = chroma_integration.create_collection("aven_financial_products")
    
    # Insert data into ChromaDB
    chroma_integration.insert_data_into_chroma(collection, processed_data, batch_size=50)
    
    # Get collection statistics
    stats = chroma_integration.get_collection_stats(collection)
    print("\n=== Aven ChromaDB Collection Statistics ===")
    print(f"Collection name: {stats.get('collection_name', 'N/A')}")
    print(f"Total items: {stats.get('total_items', 0)}")
    
    print("\nCategories:")
    for category, count in stats.get('categories', {}).items():
        print(f"  {category}: {count} items")
    
    # Test financial queries
    print("\n=== Testing Financial Product Queries ===")
    test_queries = [
        "What are the fees for Aven credit card?",
        "How does the home equity credit card work?",
        "What are the cash back rewards?",
        "What are the balance transfer options?",
        "How do monthly payments work?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = chroma_integration.query_collection(collection, query, n_results=3)
        
        if results and 'documents' in results and results['documents']:
            print("Top results:")
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                category = metadata.get('category', 'unknown')
                print(f"  {i+1}. [{category}] {doc[:150]}...")
        else:
            print("  No results found")

if __name__ == "__main__":
    main() 