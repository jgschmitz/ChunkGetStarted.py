# ChunkGetStarted.py
1️⃣ Extracting text from PDFs <br>
2️⃣ Chunking the text into meaningful sections <br>
3️⃣ Generating sentence embeddings for each chunk <br>
4️⃣ Storing &amp; indexing the embeddings for fast retrieval <br>

🚀 Step 1: Install Required Libraries
Run this in your terminal:
```
pip install pypdf langchain sentence-transformers pymongo
```
pypdf → Extracts text from PDFs
langchain.text_splitter → Chunks text into sentences
sentence-transformers → Converts text into embeddings
pymongo → Stores embeddings in MongoDB
🚀 Step 2: Extract Text from PDFs
We use pypdf to read the text from each PDF file.
```
import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file"""
    reader = PdfReader(pdf_path)
    text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Example: Extract text from a sample PDF
pdf_path = "example.pdf"  # Replace with a real file path
extracted_text = extract_text_from_pdf(pdf_path)
print("✅ Extracted Text:", extracted_text[:500])  # Show first 500 characters
```
🚀 Step 3: Chunk the Text into Sentences
Now, we use LangChain’s RecursiveCharacterTextSplitter to break large text into smaller, meaningful sentence-sized chunks.
```
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    """Chunk extracted text into overlapping segments"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)

# Example: Chunk extracted text
chunks = chunk_text(extracted_text)
print("✅ Sample Chunk:", chunks[0])  # Show first chunk
```
🚀 Step 4: Generate Sentence Embeddings
We use Sentence Transformers to convert each chunk into an embedding vector.

# Load a sentence embedding model
```
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, fast & good accuracy

def generate_embedding(text):
    """Generate a sentence embedding"""
    return model.encode(text).tolist()
```

# Example: Convert a chunk into an embedding
```
embedding = generate_embedding(chunks[0])
print("✅ Sample Embedding:", embedding[:5])  # Show first 5 dimensions
```
🚀 Step 5: Store Embeddings in MongoDB
We store each chunk + embedding inside MongoDB Atlas so we can perform vector searches later.
```
from pymongo import MongoClient

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["pdf_embeddings"]  # Database
collection = db["chunks"]  # Collection

def insert_into_mongodb(chunks):
    """Insert text chunks and their embeddings into MongoDB"""
    documents = [{"text": chunk, "embedding": generate_embedding(chunk)} for chunk in chunks]
    collection.insert_many(documents)
    print(f"✅ Inserted {len(documents)} chunks into MongoDB!")

# Example: Insert the extracted chunks
insert_into_mongodb(chunks)
🚀 Step 6: Run a Vector Search in MongoDB
```
Now that embeddings are stored in MongoDB, we can run a similarity search.
```
def search_similar_chunks(query):
    """Search for similar text chunks using MongoDB Atlas Vector Search"""
    query_embedding = generate_embedding(query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 10,
                "limit": 5
            }
        }
    ])

    return list(results)
```

# Example: Search with a user query
```
query = "What is the document saying about healthcare policies?"
matching_chunks = search_similar_chunks(query)

for doc in matching_chunks:
    print(f"🔹 Found Chunk: {doc['text']}")
```

