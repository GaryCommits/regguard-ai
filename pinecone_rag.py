import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

load_dotenv()

# Temporary hardcoded key (only for this test — we remove later)
PINECONE_API_KEY = "pcsk_E7R5F_F2hJixMsq6DxHuWSDTLhANvs7ngLCXnSheEnjtSh1UKgb2mnLC46eNVWapUJSvt"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("eu-ai-act")

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def add_reg_text(text_chunks):
    vectors = []
    for i, chunk in enumerate(text_chunks):
        embedding = embedder.encode(chunk).tolist()
        vectors.append((f"chunk_{i}", embedding, {"text": chunk}))
    index.upsert(vectors=vectors)
    print(f"✅ {len(text_chunks)} EU AI Act chunks loaded into Pinecone")

def query_reg(query_text, top_k=3):
    embedding = embedder.encode(query_text).tolist()
    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    context = "\n\n".join([match["metadata"]["text"] for match in results["matches"]])
    return context