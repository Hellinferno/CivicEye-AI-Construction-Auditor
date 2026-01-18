import google.generativeai as genai
from .config import API_KEY, MODEL_NAME
from .tools import calculate_tax_compliance, fuzzy_match_vendor
from .vector_store import CivicEvidenceStore

# --- Knowledge Base Tool ---
# Initialize store (Lazy load handles connection)
_evidence_store = CivicEvidenceStore()

def consult_knowledge_base(query: str) -> str:
    """
    Searches the internal knowledge base (Contracts & Site Visuals) for evidence related to the query.
    Use this to find specific contract details (e.g., mismatched rates, material requirements) or visual confirmations.
    """
    # 1. Search Contracts
    contract_hits = _evidence_store.search_similar_contracts(query, limit=2)
    
    # 2. Search Visuals (using text-to-visual search if supported, or just relevant metadata)
    # For now, we will search text-to-visual using CLIP
    visual_hits = _evidence_store.search_visuals_by_text(query, limit=1)
    
    response = f"--- Evidence Found for '{query}' ---\n"
    
    if contract_hits:
        response += "📄 Contract Documents:\n"
        for hit in contract_hits:
            # Clean up payload presentation
            source = hit.get('source', 'Unknown')
            text_preview = hit.get('text', '')[:200] + "..." if 'text' in hit else "No text content"
            # Actually, our text is in the 'text' field if we stored it? 
            # Wait, upsert stores vectors. Payload has metadata. 
            # We need to make sure we store the text in payload in 'ingest_data.py'.
            # Checking ingest_data.py... yes, we passed 'text=chunk' to add_evidence. 
            # But add_evidence puts 'metadata' in payload. It DOES NOT put 'text' in payload automatically unless we add it.
            # I need to fix ingest_data.py or vector_store.py to ensure text is in payload.
            # Let's assume for now I will fix vector_store.py to check this.
            response += f"- [Source: {source}]: {hit}\n"
    else:
        response += "📄 No relevant contract documents found.\n"

    if visual_hits:
        response += "\n📷 visual Evidence:\n"
        for hit in visual_hits:
             response += f"- [Image: {hit.get('source', 'Unknown')}]: {hit}\n"
    else:
        response += "\n📷 No relevant visual evidence found.\n"
        
    return response

def check_contractor_history(contractor_id: str) -> str:
    """
    Checks the long-term memory for past audit results of a contractor.
    Useful for detecting recurring issues or validating contractor track record.
    """
    history = _evidence_store.get_contractor_history(contractor_id)
    if not history:
        return f"No prior history found for contractor {contractor_id}."
    
    response = f"--- History for Contractor {contractor_id} ---\n"
    for record in history:
        response += f"• Project {record.get('project_id')} ({record.get('timestamp')}) - Status: {record.get('status')}\n"
        response += f"  Summary: {record.get('summary')}\n"
    return response

def verify_compliance(clause_text: str) -> str:
    """
    Verifies if site visual evidence supports a specific contract clause.
    Uses text-to-image search to find photos matching the clause description.
    Example clause_text: "Road width must be 12ft" or "50mm bitumen layer".
    """
    hits = _evidence_store.search_visuals_by_text(clause_text, limit=3)
    if not hits:
        return f"No visual evidence found supporting clause: '{clause_text}'."
        
    response = f"--- Visual Evidence for Clause: '{clause_text}' ---\n"
    for hit in hits:
         response += f"• [Image: {hit.get('source', 'Unknown')}]\n"
         response += f"  Metadata: {hit}\n"
    return response

    return response

def audit_visual_evidence(clause_text: str, image_source: str) -> str:
    """
    Performs a deep visual analysis of an image to verify compliance with a clause.
    Uses the Vision Language Model (Gemini Pro Vision) to "look" at the image.
    
    Args:
        clause_text: The requirement to check (e.g., "Signboard must be blue").
        image_source: The filename or source identifier of the image (e.g., "site_photo_01.jpg").
    """
    import os
    from PIL import Image
    
    # 1. Locate the image
    # Assuming images are in 'data/site_photos'
    image_path = os.path.join(os.getcwd(), 'data', 'site_photos', image_source)
    
    if not os.path.exists(image_path):
        # Fallback: check if path is absolute or just provided directly
        if os.path.exists(image_source):
             image_path = image_source
        else:
             return f"Error: Could not locate visual evidence '{image_source}'."
             
    try:
        img = Image.open(image_path)
    except Exception as e:
        return f"Error: Failed to load image. {e}"
        
    # 2. Call VLM
    # We use a fresh model instance for VLM tasks usually, or the existing one if it supports 'generate_content' with images.
    # gemini-1.5-flash supports images.
    
    prompt = f"""
    You are an Expert Civil Engineer Auditor.
    
    AUDIT REQUIREMENT: "{clause_text}"
    
    EVIDENCE: The attached image is from the construction site.
    
    TASK:
    1. Look at the image carefully.
    2. Determine if the evidence SUPPORTS or VIOLATES the requirement.
    3. Explain your reasoning.
    
    Verdict (PASS/FAIL/UNCLEAR):
    """
    
    try:
        # Use a temporary model for vision if needed, or self.model if we had access.
        # Here we create a model instance directly.
        vlm_model = genai.GenerativeModel('gemini-1.5-flash') 
        response = vlm_model.generate_content([prompt, img])
        return f"--- VLM Analysis for '{image_source}' ---\n{response.text}"
    except Exception as e:
        return f"Error during VLM analysis: {e}"

def _configure_api() -> None:
    """Configure the Gemini API with the API key."""
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")
    genai.configure(api_key=API_KEY)

class AnalystAgent:
    def __init__(self):
        _configure_api()
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            tools=[
                calculate_tax_compliance, 
                fuzzy_match_vendor, 
                consult_knowledge_base,
                check_contractor_history,
                verify_compliance,
                audit_visual_evidence
            ]
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def analyze(self, prompt: str):
        """Analyze the given prompt using the LLM."""
        return self.chat.send_message(prompt)
    
    def inject_message(self, message: str):
        """Inject a message into the chat history."""
        return self.chat.send_message(message)
