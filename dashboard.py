import streamlit as st
import os
import shutil
from vouchvault.analyst import AnalystAgent
from vouchvault.vector_store import CivicEvidenceStore
from ingest_data import ingest  # We'll reuse our ingestion logic

# Page Config
st.set_page_config(page_title="CivicEye: AI Auditor", page_icon="🏗️", layout="wide")

st.title("🏗️ CivicEye: AI Construction Auditor")
st.markdown("Multimodal Evidence-Based Auditing System")

# Function to handle file uploads
def save_uploaded_file(uploaded_file, directory):
    if uploaded_file is not None:
        path = os.path.join(directory, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return path
    return None

# Sidebar - Ingestion
with st.sidebar:
    st.header("📂 Evidence Ingestion")
    
    # Upload Contract
    uploaded_pdf = st.file_uploader("Upload Tender Contract (PDF)", type="pdf")
    if uploaded_pdf:
        save_path = save_uploaded_file(uploaded_pdf, os.path.join("data", "contracts"))
        st.success(f"Saved: {uploaded_pdf.name}")
        
    # Upload Site Photos
    uploaded_photos = st.file_uploader("Upload Site Photos (Images)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if uploaded_photos:
        for photo in uploaded_photos:
            save_uploaded_file(photo, os.path.join("data", "site_photos"))
        st.success(f"Saved {len(uploaded_photos)} photos.")
        
    # Trigger Ingestion
    if st.button("🚀 Process & Ingest Evidence"):
        with st.spinner("Chunking text & Embedding images..."):
            # Import and run ingestion function
            # Note: We need to adapt ingest_data logic slightly to be callable cleanly or just run it as subprocess
            # For simplicity, we assume ingest_data.py has an ingest() function we imported
            try:
                ingest()
                st.success("Ingestion Complete! Knowledge Base Updated.")
            except Exception as e:
                st.error(f"Ingestion Failed: {e}")

# Chat Interface
st.header("💬 Ask the Auditor")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting from Agent
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am CivicEye. I can audit contracts and verify site photos. Ask me about compliance."})

if "agent" not in st.session_state:
    st.session_state.agent = AnalystAgent()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Check if there's an image to display in this message context
        # This is a simple hack: if the message contains "VLM Analysis for 'filename'", we show that image
        if "VLM Analysis for '" in message["content"]:
            try:
                # Extract filename
                start_str = "VLM Analysis for '"
                start_idx = message["content"].find(start_str) + len(start_str)
                end_idx = message["content"].find("'", start_idx)
                filename = message["content"][start_idx:end_idx]
                
                img_path = os.path.join("data", "site_photos", filename)
                if os.path.exists(img_path):
                    st.image(img_path, caption=f"Evidence: {filename}", width=400)
            except:
                pass

# User Input
if prompt := st.chat_input("Ex: 'Does the site photo show the correct road width?'"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing evidence..."):
            response = st.session_state.agent.analyze(prompt)
            st.markdown(response.text)
            
            # Display cited image if any
            if "VLM Analysis for '" in response.text:
                try:
                    start_str = "VLM Analysis for '"
                    start_idx = response.text.find(start_str) + len(start_str)
                    end_idx = response.text.find("'", start_idx)
                    filename = response.text[start_idx:end_idx]
                    img_path = os.path.join("data", "site_photos", filename)
                    if os.path.exists(img_path):
                        st.image(img_path, caption=f"Evidence: {filename}", width=400)
                except:
                    pass
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
