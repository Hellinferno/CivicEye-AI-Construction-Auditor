import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

DATA_DIR = os.path.join(os.getcwd(), 'data')
CONTRACTS_DIR = os.path.join(DATA_DIR, 'contracts')
PHOTOS_DIR = os.path.join(DATA_DIR, 'site_photos')

def setup_directories():
    os.makedirs(CONTRACTS_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)
    print(f"Created directories: {CONTRACTS_DIR}, {PHOTOS_DIR}")

def create_dummy_contract(filename="contract_road_repair.pdf"):
    filepath = os.path.join(CONTRACTS_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Contract Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "MUNICIPAL CORPORATION - ROAD REPAIR CONTRACT")
    
    # Contract Body
    c.setFont("Helvetica", 12)
    text_lines = [
        "Contract ID: 2025-RR-001",
        "Vendor: TechSolutions Inc (Wait, they do roads too?)",
        "Date: November 1st, 2025",
        "Scope of Work: Repair of Main Street (Sector 4 to Sector 9).",
        "",
        "Specification Highlights:",
        "1. Material: High-grade bitumen with 5% polymer.",
        "2. Required Thickness: 50mm compacted layer.",
        "3. Cement Requirements: The contractor shall provide 500 bags of Portland Cement.",
        "4. Completion Timeline: 45 days from issuance.",
        "",
        "Payment Terms:",
        "- 30% Advance",
        "- 70% Post-Completion Audit",
        "",
        "Signatories:",
        "City Engineer: ____________________",
        "Vendor Rep: ____________________"
    ]
    
    y = height - 120
    for line in text_lines:
        c.drawString(72, y, line)
        y -= 15
        
    c.save()
    print(f"Created PDF: {filepath}")

def create_dummy_site_photo(filename="site_photo_01.jpg", text="Site Inspection: Main Street"):
    filepath = os.path.join(PHOTOS_DIR, filename)
    
    # Create a blank image (simulating a photo)
    img = Image.new('RGB', (800, 600), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    
    # Draw some "shapes" to simulate content lol
    d.rectangle([50, 400, 750, 600], fill=(50, 50, 50)) # "Road"
    d.rectangle([100, 300, 200, 500], fill=(200, 150, 100)) # "Construction Material"
    
    # Add text overlay (to ensure Semantic Image Search has something distinct if models are basic, 
    # though CLIP should pick up the 'road' vibes from the gray rectangle if we're lucky, 
    # but let's be real, this is a placeholder)
    try:
        # Default font
        font = ImageFont.load_default()
        d.text((50, 50), text, fill=(255, 255, 255))
        d.text((50, 70), "Visual Evidence: Road Layer", fill=(255, 255, 255))
    except Exception:
        pass

    img.save(filepath)
    print(f"Created Image: {filepath}")

if __name__ == "__main__":
    setup_directories()
    create_dummy_contract()
    create_dummy_site_photo()
