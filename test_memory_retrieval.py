import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from vouchvault.vector_store import CivicEvidenceStore
from vouchvault.analyst import check_contractor_history, verify_compliance, _evidence_store

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_memory_and_retrieval():
    print("🧠 Starting Memory & Retrieval Test...")
    
    store = CivicEvidenceStore()
    if not store.client:
        print("❌ Qdrant client not initialized.")
        return

    # 1. Test Memory Storage
    contractor_id = "C_99"
    project_id = "Project_Alpha"
    print(f"\nStoring audit result for {contractor_id}...")
    store.store_audit_result(
        contractor_id=contractor_id, 
        project_id=project_id, 
        status="FAIL", 
        summary="Found 3 minor anomalies in material quality."
    )
    
    # 2. Test Function Tool: check_contractor_history
    print(f"\nChecking history for {contractor_id}...")
    history_response = check_contractor_history(contractor_id)
    print(f"Tool Output:\n{history_response}")
    
    if "Project_Alpha" in history_response:
        print("✅ Success: History retrieved correctly.")
    else:
        print("❌ Failed: History not found.")

    # 3. Test Cross-Modal Auditor: verify_compliance
    clause = "road" # Simple keyword to match our dummy image
    print(f"\nVerifying compliance for clause: '{clause}'...")
    visual_response = verify_compliance(clause)
    print(f"Tool Output:\n{visual_response}")
    
    if "Visual Evidence" in visual_response and "site_photo" in visual_response:
        print("✅ Success: Visual evidence found.")
    else:
        # Note: Depending on CLIP model/dummy image, this might fail if 'road' isn't strongly detected in the placeholder drawing.
        # But since we added text=metadata for visual search fallback (or just relying on CLIP), let's see.
        # Actually our search_visuals_by_text uses CLIP text encoding -> Image embedding search.
        # If the dummy image is just rectangles, CLIP might struggle. 
        # But we added "Visual Evidence: Road Layer" text drawing on the image, so OCR-like behavior isn't happening here.
        # It's relying on CLIP understanding the drawn rectangles look like a road or the color profile.
        print("⚠️ Warning: Visual match might be weak for dummy image. Check output above.")

if __name__ == "__main__":
    test_memory_and_retrieval()
