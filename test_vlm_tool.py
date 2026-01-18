import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import google.generativeai as genai
from vouchvault.config import API_KEY
from vouchvault.analyst import audit_visual_evidence

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure GenAI
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: API Key not found!")

def test_vlm_tool():
    print("🧠 Starting VLM Tool Verification...")
    
    # 1. Define inputs
    # We use the dummy image created earlier
    image_source = "site_photo_01.jpg"
    clause_text = "The road surface must be free of major cracks and at least 12ft wide."
    
    print(f"Clause: {clause_text}")
    print(f"Image: {image_source}")
    
    # 2. Call the tool directly
    print("\nCalling VLM...")
    result = audit_visual_evidence(clause_text, image_source)
    
    print(f"\n--- VLM Result ---\n{result}")
    
    if "Error" not in result:
        print("✅ Success: VLM tool executed without errors.")
    else:
        print("❌ Failed: VLM tool reported an error.")

if __name__ == "__main__":
    test_vlm_tool()
