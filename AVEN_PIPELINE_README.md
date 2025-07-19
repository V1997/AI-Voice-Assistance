# Aven.com Data Processing Pipeline

This pipeline processes Firecrawl-extracted Aven.com data, generates embeddings using Google's Gemini model, and stores them in ChromaDB for LLM training and fine-tuning.

## Overview

The pipeline transforms raw Firecrawl JSON data into a searchable vector database containing Aven's financial product information, including:
- Home equity credit card features
- Fee structures and rates
- Legal documents and terms
- Educational content
- Support information

## Pipeline Architecture

```
Firecrawl JSON → Data Preprocessing → Gemini Embeddings → ChromaDB Storage → LLM Integration
```

### Step 1: Data Preprocessing
- Filters out irrelevant content (Alberta, CenturyLink, empty pages)
- Cleans and normalizes text content
- Categorizes content (education, legal_document, support, etc.)
- Extracts financial information (fees, rates, contact info)
- Chunks content into small, precise segments (25-50 words) for exact answers

### Step 2: Embedding Generation
- Uses Google's Gemini embedding-001 model
- Generates vector embeddings for each text chunk
- Handles rate limiting and error recovery
- Preserves metadata with embeddings

### Step 3: ChromaDB Cloud Storage
- Stores embeddings and metadata in ChromaDB Cloud
- Enables semantic search on financial products
- Provides filtering by content type
- Exports data for further use

## Prerequisites

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Get your API keys and add them to your `.env` file:

```env
# Google API key for Gemini embeddings
GOOGLE_API_KEY=your-google-api-key-here

# ChromaDB Cloud API key
CHROMADB_API_KEY=your-chromadb-api-key-here
```

**Get Google API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)
**Get ChromaDB API key from:** [ChromaDB Cloud](https://cloud.chromadb.com/)

### 3. Verify Input Data
Ensure your `firecrawl/documents_1.json` file exists and contains the scraped Aven.com data.

## Quick Start

Run the complete pipeline with one command:

```bash
python main_pipeline.py
```

This will:
- Process and filter the raw data
- Generate Gemini embeddings
- Store everything in ChromaDB
- Test the system with financial queries
- Export the results

## Step-by-Step Execution

If you prefer to run each step individually:

### Step 1: Data Preprocessing
```bash
python data_preprocessor.py
```
**Output:** `aven_processed_data.json`

### Step 2: Generate Embeddings
```bash
python gemini_embedding_generator.py
```
**Output:** `aven_embeddings_data.json`

### Step 3: Store in ChromaDB Cloud
```bash
python chromadb_integration.py
```
**Output:** `aven_chroma_export.json` (exported from ChromaDB Cloud)

## Output Files

After running the pipeline, you'll have:

1. **`aven_processed_data.json`** - Cleaned and chunked Aven.com data
2. **`aven_embeddings_data.json`** - Data with Gemini embeddings
3. **`aven_chroma_export.json`** - Exported ChromaDB Cloud collection

## Data Analysis Results

Based on your Firecrawl data, the pipeline will process:

### Content Categories
- **Education**: Aven credit card features and how it works
- **Legal Documents**: AutoPay agreement, privacy policy, CFPB booklets
- **Support**: Customer service information
- **Product Info**: General product details

### Financial Information Extracted
- **Fees**: 2.5% cash out fee, $29 late fee
- **Rates**: 2% cash back, variable interest rates
- **Contact**: support@aven.com, 1.877.761.1080
- **Terms**: Home equity, HELOC, credit card, balance transfer

## Using the Vector Database

### Query Examples
```python
from chromadb_integration import AvenChromaDBIntegration

# Initialize
chroma_integration = AvenChromaDBIntegration()
collection = chroma_integration.create_collection("aven_financial_products")

# Search for similar content
results = chroma_integration.query_collection(
    collection, 
    "What are the fees for Aven credit card?", 
    n_results=5
)

# Filter by category
results = chroma_integration.query_collection(
    collection,
    "How do monthly payments work?",
    n_results=3,
    where_filter={"category": "education"}
)
```

### Metadata Available
Each document in ChromaDB includes:
- `url` - Original page URL
- `title` - Page title
- `category` - Content type (education, legal_document, support, etc.)
- `chunk_index` - Position within the original page
- `word_count` - Number of words in the chunk
- `embedding_model` - Gemini embedding-001
- `embedding_dimension` - Size of embedding vector
- `fees_mentioned` - Extracted fee information
- `percentages_mentioned` - Extracted rate information
- `financial_terms` - Detected financial product terms

## Configuration Options

### Data Preprocessing
In `data_preprocessor.py`:
- `max_chunk_size` - Maximum words per chunk (default: 800)
- `overlap` - Overlap between chunks (default: 150)

### Embedding Generation
In `gemini_embedding_generator.py`:
- `model` - Gemini embedding model (default: "models/embedding-001")

- `batch_size` - Number of texts to process together (default: 50)

### ChromaDB Storage
In `chromadb_integration.py`:
- `persist_directory` - Where to store ChromaDB data (default: "./aven_chroma_db")
- `collection_name` - Name of the collection (default: "aven_financial_products")

## Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   Error: GOOGLE_API_KEY environment variable not set
   ```
   **Solution:** Set your Google API key as shown in Prerequisites.

2. **Missing Dependencies**
   ```
   ImportError: No module named 'google.generativeai'
   ```
   **Solution:** Run `pip install -r requirements.txt`

3. **Rate Limiting**
   ```
   Error generating batch embeddings: Rate limit exceeded
   ```
   **Solution:** Reduce batch size or increase delays between requests.

4. **Empty Content**
   ```
   No processed data found
   ```
   **Solution:** Check that your Firecrawl data contains valid Aven.com content.

### Performance Tips

- **Small Datasets:** Use batch size of 20 for optimal performance
- **Rate Limiting:** Increase delays between API calls if needed
- **Storage:** Ensure sufficient disk space for ChromaDB persistence

## Next Steps for LLM Training

### 1. Retrieval-Augmented Generation (RAG)
Use the ChromaDB collection to provide context to your LLM:
```python
# Get relevant documents for a query
query = "What are Aven's credit card fees?"
results = collection.query(query_texts=[query], n_results=5)

# Use retrieved documents as context for LLM
context = "\n".join(results['documents'][0])
```

### 2. Fine-tuning Data Preparation
Export the processed data for fine-tuning:
```python
# Export for fine-tuning
with open('aven_embeddings_data.json', 'r') as f:
    data = json.load(f)

# Convert to training format
training_data = []
for item in data:
    training_data.append({
        'text': item['content'],
        'metadata': item['metadata'],
        'embedding': item['embedding']
    })
```

### 3. AI Voice Assistant Integration
Use embeddings for voice assistant queries:
```python
# Voice query processing
voice_query = "What are the fees for the Aven credit card?"
results = chroma_integration.query_collection(collection, voice_query, n_results=3)

# Generate voice response using retrieved context
response = generate_voice_response(results['documents'][0])
```

## File Structure

```
├── firecrawl/
│   └── documents_1.json              # Raw Firecrawl data
├── data_preprocessor.py              # Data cleaning and filtering
├── gemini_embedding_generator.py     # Gemini embedding generation
├── chromadb_integration.py           # ChromaDB operations
├── main_pipeline.py                  # Complete pipeline orchestration
├── requirements.txt                  # Python dependencies
├── AVEN_PIPELINE_README.md           # This file
├── aven_processed_data.json          # Cleaned data (generated)
├── aven_embeddings_data.json         # Data with embeddings (generated)
└── aven_chroma_export.json           # Exported ChromaDB Cloud data (generated)
```

## Expected Results

After running the pipeline, you should have:
- **100-200 precise text chunks** (25-50 words each) from relevant Aven.com content
- **Gemini embeddings** for exact semantic search
- **ChromaDB collection** with precise financial product knowledge
- **Tested queries** showing exact results for financial questions

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API key and dependencies
3. Check the console output for specific error messages
4. Ensure your Firecrawl data contains valid Aven.com content

## License

This pipeline is designed for processing publicly available website data for educational and research purposes. Ensure compliance with website terms of service and data usage policies. 