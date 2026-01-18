import os
import glob
from pypdf import PdfReader
from PIL import Image

# Import our store
from vouchvault.vector_store import CivicEvidenceStore

DATA_DIR = os.path.join(os.getcwd(), 'data')
CONTRACTS_DIR = os.path.join(DATA_DIR, 'contracts')
PHOTOS_DIR = os.path.join(DATA_DIR, 'site_photos')

def ingest():
    print("🚀 Starting Data Ingestion...")
    store = CivicEvidenceStore()
    
    if not store.client:
        print("❌ Cannot proceed without Qdrant.")
        return

    # 1. Ingest Contracts (PDFs)
    pdf_files = glob.glob(os.path.join(CONTRACTS_DIR, "*.pdf"))
    print(f"📄 Found {len(pdf_files)} contracts.")
    
    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Simple chunking (per contract for now, or split by paragraph)
            # ideally we split by section, but full text is fine for 384 dim if small
            doc_id = os.path.basename(pdf_path)
            
            print(f"   Splitting '{doc_id}' ({len(text)} chars)...")
            
            # Basic chunking: 500 chars with overlap
            chunk_size = 500
            overlap = 50
            
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                chunk_id = f"{doc_id}_chunk_{i}"
                
                print(f"   -> Indexing chunk {chunk_id}")
                store.add_evidence(
                    doc_id=chunk_id,
                    text=chunk,
                    metadata={"source": doc_id, "type": "contract_pdf"}
                )
                
        except Exception as e:
            print(f"❌ Failed to process {pdf_path}: {e}")

    # 2. Ingest Site Photos
    image_files = glob.glob(os.path.join(PHOTOS_DIR, "*.jpg"))
    print(f"📷 Found {len(image_files)} site photos.")
    
    for img_path in image_files:
        img_id = os.path.basename(img_path)
        print(f"   -> Indexing Image {img_id}")
        store.add_evidence(
             doc_id=img_id,
             text="", # No text for image-only
             image_path=img_path,
             metadata={
                 "type": "evidence", 
                 "project_id": "P1", 
                 "contractor_id": "C_99",
                 "source": img_id
             }
        )

    print("✅ Ingestion Complete.")

if __name__ == "__main__":
    ingest()
