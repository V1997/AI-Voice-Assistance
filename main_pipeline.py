#!/usr/bin/env python3
"""
Main Pipeline for Aven.com Data Processing
This script orchestrates the entire pipeline from raw Firecrawl data to ChromaDB storage
"""

import os
import sys
import json
from dotenv import load_dotenv
from data_preprocessor import AvenDataPreprocessor
from gemini_embedding_generator import GeminiEmbeddingGenerator
from chromadb_integration import AvenChromaDBIntegration

# Load environment variables from .env file
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'google.generativeai',
        'chromadb',
        'numpy',
        'tqdm'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_api_key():
    """Check if Google API key is set"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        print("Please set your Google API key:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        return False
    return True

def run_pipeline():
    """Run the complete Aven.com data processing pipeline"""
    print("=" * 60)
    print("AVEN.COM DATA PROCESSING PIPELINE")
    print("=" * 60)
    
    # Step 1: Check dependencies and API key
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        return False
    
    if not check_api_key():
        return False
    
    print("✓ All dependencies and API key are ready")
    
    # Step 2: Data Preprocessing
    print("\n2. Data Preprocessing...")
    try:
        preprocessor = AvenDataPreprocessor('firecrawl/documents_1.json')
        processed_data = preprocessor.process_data(min_chunk_size=25, max_chunk_size=50, overlap=5)
        preprocessor.save_processed_data('aven_processed_data.json')
        
        summary = preprocessor.generate_summary()
        print(f"✓ Processed {summary['total_chunks']} chunks with {summary['total_words']:,} total words")
        print("Categories found:")
        for category, count in summary['categories'].items():
            print(f"  - {category}: {count} chunks")
        
    except Exception as e:
        print(f"✗ Error in data preprocessing: {e}")
        return False
    
    # Step 3: Generate Embeddings
    print("\n3. Generating Embeddings with Gemini...")
    try:
        generator = GeminiEmbeddingGenerator(model="models/embedding-001")
        data_with_embeddings = generator.process_data_with_embeddings(processed_data, batch_size=50)
        generator.save_embeddings(data_with_embeddings, 'embeddings_output/aven_embeddings_data.json')
        
        summary = generator.generate_summary(data_with_embeddings)
        print(f"✓ Generated embeddings for {summary['items_with_embeddings']} items")
        print(f"✓ Success rate: {summary['embedding_success_rate']:.2%}")
        print(f"✓ Embedding dimension: {summary['embedding_dimension']}")
        
    except Exception as e:
        print(f"✗ Error in embedding generation: {e}")
        return False
    
    # Step 4: Store embeddings in separate folder (ChromaDB temporarily disabled)
    print("\n4. Storing embeddings in separate folder...")
    try:
        # Save embeddings to separate folder
        embeddings_file = "embeddings_output/aven_embeddings_detailed.json"
        generator.save_embeddings(data_with_embeddings, embeddings_file)
        print(f"✓ Saved detailed embeddings to {embeddings_file}")
        
        # Create a summary file
        summary_file = "embeddings_output/embeddings_summary.json"
        summary = generator.generate_summary(data_with_embeddings)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved embeddings summary to {summary_file}")
        
        # Display summary
        print(f"\n📊 Embeddings Summary:")
        print(f"   Total items: {summary['total_items']}")
        print(f"   Items with embeddings: {summary['items_with_embeddings']}")
        print(f"   Success rate: {summary['embedding_success_rate']:.2%}")
        print(f"   Embedding dimension: {summary['embedding_dimension']}")
        print(f"   Model used: {summary['model_used']}")
        
        print(f"\n📁 Embeddings stored in: embeddings_output/")
        
    except Exception as e:
        print(f"✗ Error in embeddings storage: {e}")
        return False
    
    # Step 5: Store in ChromaDB
    print("\n5. Storing in ChromaDB...")
    try:
        # Initialize ChromaDB integration
        chroma_client = AvenChromaDBIntegration()
        
        # Create or get collection
        collection = chroma_client.create_collection("aven_financial_products")
        
        # Insert data into ChromaDB
        chroma_client.insert_data_into_chroma(collection, data_with_embeddings, batch_size=10)
        
        # Get collection statistics
        stats = chroma_client.get_collection_stats(collection)
        print(f"✓ Successfully stored {stats.get('total_items', 0)} items in ChromaDB")
        print(f"✓ Collection: {stats.get('collection_name', 'aven_financial_products')}")
        
        # Test a simple query
        test_query = "credit card fees"
        test_results = chroma_client.query_collection(collection, test_query, n_results=3)
        if test_results and 'documents' in test_results:
            print(f"✓ Test query successful - found {len(test_results['documents'][0])} results")
        
    except Exception as e:
        print(f"✗ Error in ChromaDB storage: {e}")
        return False
    
    print("✓ Pipeline completed successfully!")
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nOutput files created:")
    print("  - aven_processed_data.json (cleaned and chunked Aven data)")
    print("  - embeddings_output/aven_embeddings_detailed.json (detailed embeddings)")
    print("  - embeddings_output/embeddings_summary.json (embeddings summary)")
    print("  - ChromaDB collection: aven_financial_products")
    
    print("\nNext steps for LLM training/fine-tuning:")
    print("  1. Use the ChromaDB collection for RAG (Retrieval-Augmented Generation)")
    print("  2. Export data for fine-tuning with your preferred LLM framework")
    print("  3. Use the embeddings for semantic search on Aven financial products")
    print("  4. Integrate with your AI voice assistant for financial product queries")
    print("  5. Query ChromaDB for financial product information")
    
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Aven.com Data Processing Pipeline")
        print("\nUsage:")
        print("  python main_pipeline.py          # Run the complete pipeline")
        print("  python main_pipeline.py --help   # Show this help")
        print("\nPrerequisites:")
        print("  1. Set GOOGLE_API_KEY environment variable")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Ensure firecrawl/documents_1.json exists")
        print("\nPipeline Steps:")
        print("  1. Data Preprocessing - Filter and clean Aven.com content")
        print("  2. Embedding Generation - Create Gemini embeddings")
        print("  3. ChromaDB Storage - Store in vector database")
        print("  4. Testing - Verify financial product queries")
        return
    
    success = run_pipeline()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 