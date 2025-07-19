#!/usr/bin/env python3
"""
Debug script to test each pipeline step individually
"""

import json
from data_preprocessor import AvenDataPreprocessor
from gemini_embedding_generator import GeminiEmbeddingGenerator

def test_pipeline_steps():
    """Test each pipeline step individually"""
    
    print("=" * 60)
    print("PIPELINE STEP-BY-STEP DEBUG")
    print("=" * 60)
    
    # Step 1: Data Loading
    print("\n1. Testing Data Loading...")
    try:
        preprocessor = AvenDataPreprocessor('firecrawl/documents_1.json')
        raw_data = preprocessor.load_data()
        print(f"   ✅ Loaded {len(raw_data)} items")
    except Exception as e:
        print(f"   ❌ Error loading data: {e}")
        return False
    
    # Step 2: Data Filtering
    print("\n2. Testing Data Filtering...")
    try:
        filtered_data = preprocessor.filter_relevant_content(raw_data)
        print(f"   ✅ Filtered to {len(filtered_data)} relevant items")
    except Exception as e:
        print(f"   ❌ Error filtering data: {e}")
        return False
    
    # Step 3: Data Processing (this is where it might be stuck)
    print("\n3. Testing Data Processing...")
    try:
        print("   Starting data processing...")
        processed_data = preprocessor.process_data(min_chunk_size=25, max_chunk_size=50, overlap=5)
        print(f"   ✅ Processed {len(processed_data)} chunks")
        
        # Show some details
        if processed_data:
            print(f"   Sample chunk: {processed_data[0]['content'][:100]}...")
            print(f"   Sample metadata: {processed_data[0]['metadata']['category']}")
        
    except Exception as e:
        print(f"   ❌ Error in data processing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Save Processed Data
    print("\n4. Testing Save Processed Data...")
    try:
        preprocessor.save_processed_data('aven_processed_data.json')
        print("   ✅ Saved processed data")
    except Exception as e:
        print(f"   ❌ Error saving processed data: {e}")
        return False
    
    # Step 5: Embedding Generation (if we get here)
    print("\n5. Testing Embedding Generation...")
    try:
        print("   Initializing embedding generator...")
        generator = GeminiEmbeddingGenerator(model="models/embedding-001")
        print("   ✅ Embedding generator initialized")
        
        print("   Generating embeddings...")
        data_with_embeddings = generator.process_data_with_embeddings(processed_data, batch_size=50)
        print(f"   ✅ Generated embeddings for {len(data_with_embeddings)} items")
        
    except Exception as e:
        print(f"   ❌ Error in embedding generation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 All pipeline steps completed successfully!")
    return True

if __name__ == "__main__":
    success = test_pipeline_steps()
    
    if success:
        print("\n✅ Pipeline debug completed - all steps working!")
    else:
        print("\n❌ Pipeline debug failed - check the error above.") 