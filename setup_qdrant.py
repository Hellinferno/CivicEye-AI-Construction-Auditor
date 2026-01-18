import sys
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

# NOTE: Run Qdrant with Docker before running this script:
# docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

def setup_qdrant():
    print("Setting up Qdrant schema...")
    
    # 1. Connect to Qdrant
    # If using Qdrant Cloud, replace with URL and API Key
    try:
        client = QdrantClient("localhost", port=6333)
        # Check connection
        client.get_collections()
        print("Connected to Qdrant at localhost:6333")
    except Exception as e:
        print(f"❌ Could not connect to Qdrant at localhost:6333. Error: {e}")
        print("\nPlease ensure Qdrant is running. Run:")
        print("docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
        return

    collection_name = "civic_audit_evidence"

    # 2. Get Vector Dimensions
    # Text: all-MiniLM-L6-v2 is a standard, efficient model.
    text_model_name = 'all-MiniLM-L6-v2'
    try:
        print(f"Loading text model '{text_model_name}' to verify dimensions...")
        text_model = SentenceTransformer(text_model_name)
        text_dim = text_model.get_sentence_embedding_dimension()
    except Exception as e:
        print(f"Failed to load sentence transformer: {e}")
        text_dim = 384 # Fallback
    
    # Image: We'll assume CLIP ViT-B/32 or similar which is 512.
    # If you use a different model, update this.
    image_dim = 512
    
    print(f"Configuration: Text Dim={text_dim}, Image Dim={image_dim}")

    # 3. Create Collection
    if client.collection_exists(collection_name):
        print(f"Collection '{collection_name}' already exists. Deleting to start fresh...")
        client.delete_collection(collection_name)

    print(f"Creating collection '{collection_name}' with Named Vectors...")
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "contract_text": models.VectorParams(size=text_dim, distance=models.Distance.COSINE),
                "site_visuals": models.VectorParams(size=image_dim, distance=models.Distance.COSINE),
            }
        )
        print(f"✅ Collection '{collection_name}' created successfully.")
    except Exception as e:
        print(f"❌ Failed to create collection: {e}")

if __name__ == "__main__":
    setup_qdrant()
