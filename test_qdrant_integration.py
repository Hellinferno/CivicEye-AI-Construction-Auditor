import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from vouchvault.vector_store import CivicEvidenceStore

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_integration():
    print("Starting Qdrant Integration Test...")
    
    store = CivicEvidenceStore()
    
    if not store.client:
        print("Qdrant client not initialized. Is Docker running?")
        return

    # 1. Add Dummy Evidence
    doc_id = "test_contract_001"
    text_content = "The contractor shall provide 500 bags of cement for the foundation work."
    
    print(f"Adding evidence: '{text_content}'")
    store.add_evidence(doc_id=doc_id, text=text_content)
    
    # 2. Search Text
    query = "cement requirements"
    print(f"Searching for: '{query}'")
    results = store.search_similar_contracts(query)
    
    print(f"Found {len(results)} results.")
    
    # DEBUG: Check if point exists by ID
    point_id = store._generate_id(doc_id)
    print(f"DEBUG: Checking for Point ID: {point_id}")
    try:
        points = store.client.retrieve(
            collection_name=store.collection_name,
            ids=[point_id]
        )
        if points:
            print(f"DEBUG: Point found directly! Payload: {points[0].payload}")
        else:
            print("DEBUG: Point NOT found by ID.")
    except Exception as e:
        print(f"DEBUG: Retrieve failed: {e}")

    for res in results:
        print(f" - Result Payload: {res}")
        if res.get('original_id') == doc_id:
             print("Success: Found the added document!")
             return

    print("Failed: Did not find the added document in search.")

if __name__ == "__main__":
    test_integration()
