# 🏗️ CivicEye: AI Construction Auditor

> **Multimodal Evidence-Based Auditing System** for Civic Infrastructure Projects

[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-blue)](https://qdrant.tech/)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%201.5-orange)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)

## ✨ Features

| Capability | Description |
|------------|-------------|
| **Multimodal Retrieval** | Named vectors for contracts (text) & site photos (images) |
| **Long-Term Memory** | Stores contractor audit history across projects |
| **VLM Analysis** | Gemini Vision analyzes site photos against contract clauses |
| **Evidence-Based** | Every audit decision cites specific documents/photos |

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Qdrant (Docker)
docker run -d -p 6333:6333 qdrant/qdrant

# 3. Configure API Key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 4. Setup & Ingest
python setup_qdrant.py
python generate_dummy_data.py
python ingest_data.py

# 5. Launch Dashboard
streamlit run dashboard.py
```

## 🛠️ Agent Tools

| Tool | Purpose |
|------|---------|
| `consult_knowledge_base(query)` | Search contracts & visuals |
| `check_contractor_history(id)` | Retrieve past audit records |
| `verify_compliance(clause)` | Text-to-image evidence search |
| `audit_visual_evidence(clause, image)` | VLM compliance verification |

## 📁 Project Structure

```
├── dashboard.py           # Streamlit UI
├── setup_qdrant.py        # Initialize vector DB
├── ingest_data.py         # PDF/Image ingestion
├── generate_dummy_data.py # Demo data generator
├── vouchvault/
│   ├── analyst.py         # Agent + Tools
│   ├── vector_store.py    # Qdrant integration
│   └── config.py          # Settings
└── data/
    ├── contracts/         # PDF contracts
    └── site_photos/       # Site images
```

## 🧪 Running Tests

```bash
pytest -q
python test_qdrant_integration.py
python test_memory_retrieval.py
python test_vlm_tool.py
```

## 🏆 Built For

**Convolve 4.0 Hackathon** - Demonstrating:
- ✅ Effective Multimodal Retrieval
- ✅ Memory Beyond Single Prompt
- ✅ Evidence-Based Outputs with Societal Impact
