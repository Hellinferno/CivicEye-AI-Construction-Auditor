import logging
import uuid
from typing import List, Dict, Optional, Union
from qdrant_client import QdrantClient, models as q_models
from sentence_transformers import SentenceTransformer
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CivicEvidenceStore:
    """
    Manages the 'civic_audit_evidence' collection in Qdrant.
    Supports Named Vectors for Multimodal Retrieval:
    - 'contract_text': For semantic search over textual documents.
    - 'site_visuals': For visual similarity search over site photos.
    """
    
    def __init__(self, collection_name: str = "civic_audit_evidence", host: str = "localhost", port: int = 6333):
        self.collection_name = collection_name
        self.host = host
        self.port = port
        self.client = None
        self.text_model = None
        self.vision_model = None
        
        # Lazy connect
        self._connect()

    def _connect(self):
        """Establishes connection to Qdrant."""
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            # Verify connection
            self.client.get_collections()
            logger.info(f"✅ Connected to Qdrant at {self.host}:{self.port}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to connect to Qdrant: {e}. Vector capabilities will be disabled.")
            self.client = None

    def _load_text_model(self):
        """Lazy load the text embedding model."""
        if not self.text_model:
            logger.info("Loading text embedding model (all-MiniLM-L6-v2)...")
            try:
                self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                logger.error(f"Failed to load text model: {e}")

    def _load_vision_model(self):
        """Lazy load the vision embedding model."""
        if not self.vision_model:
            logger.info("Loading vision embedding model (clip-ViT-B-32)...")
            try:
                self.vision_model = SentenceTransformer('clip-ViT-B-32')
            except Exception as e:
                logger.error(f"Failed to load vision model: {e}")

    def _generate_id(self, doc_id: str) -> str:
        """Generates a UUID from a string ID."""
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))

    def add_evidence(self, doc_id: str, text: str, image_path: Optional[str] = None, metadata: Dict = None):
        """
        Upserts a document with named vectors.
        """
        if not self.client:
            logger.error("Qdrant client not connected.")
            return

        vectors = {}
        
        # 1. Text Vector
        if text:
            self._load_text_model()
            if self.text_model:
                vectors["contract_text"] = self.text_model.encode(text).tolist()
        
        # 2. Image Vector
        if image_path:
            self._load_vision_model()
            if self.vision_model:
                try:
                    img = Image.open(image_path)
                    vectors["site_visuals"] = self.vision_model.encode(img).tolist()
                except Exception as e:
                    logger.error(f"Failed to encode image {image_path}: {e}")

        if not vectors:
            logger.warning("No vectors generated. Skipping upsert.")
            return

        point_id = self._generate_id(doc_id)
        
        # Merge text into metadata for retrieval
        payload = metadata or {"original_id": doc_id}
        if text:
            payload["text"] = text

        point = q_models.PointStruct(
            id=point_id,
            vector=vectors,
            payload=payload
        )
        
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point],
                wait=True
            )
            logger.info(f"✅ Document '{doc_id}' stored/updated successfully.")
        except Exception as e:
            logger.error(f"Failed to upsert to Qdrant: {e}")

    def search_similar_contracts(self, query_text: str, limit: int = 3) -> List[Dict]:
        """Search for similar text contracts."""
        if not self.client: return []
        
        self._load_text_model()
        if not self.text_model: return []
        
        query_vector = self.text_model.encode(query_text).tolist()
        
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                using="contract_text",
                limit=limit,
                with_payload=True
            ).points
            return [hit.payload for hit in results]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_visuals_by_image(self, query_image_path: str, limit: int = 3) -> List[Dict]:
        """Search for similar visual evidence using an image."""
        if not self.client: return []
        
        self._load_vision_model()
        if not self.vision_model: return []
        
        try:
            img = Image.open(query_image_path)
            query_vector = self.vision_model.encode(img).tolist()
            
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                using="site_visuals",
                limit=limit,
                with_payload=True
            ).points
            return [hit.payload for hit in results]
        except Exception as e:
            logger.error(f"Visual search failed: {e}")
            return []

    # Optional: Cross-modal search (Text to Image) if vision model supports it (CLIP does)
    def search_visuals_by_text(self, query_text: str, limit: int = 3) -> List[Dict]:
        """Search for visuals using a text description (requires CLiP)."""
        if not self.client: return []
        
        # For CLIP, text and image embeddings are in the same space.
        # But we saved images using `site_visuals`.
        # If we used CLIP for `site_visuals`, we can use CLIP text encoding here.
        
        self._load_vision_model()
        if not self.vision_model: return []
        
        try:
            query_vector = self.vision_model.encode(query_text).tolist()
            
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                using="site_visuals",
                limit=limit,
                with_payload=True
            ).points
            return [hit.payload for hit in results]
        except Exception as e:
            logger.error(f"Text-to-visual search failed: {e}")
            return []

    def store_audit_result(self, contractor_id: str, project_id: str, status: str, summary: str):
        """
        Stores an audit result in the memory (Long-term Memory).
        Uses 'contract_text' vector for semantic search over history.
        """
        if not self.client: return

        # Generate ID
        audit_id = f"audit_{contractor_id}_{uuid.uuid4().hex[:8]}"
        
        # Embed summary for semantic retrieval
        self._load_text_model()
        vectors = {}
        if self.text_model:
             vectors["contract_text"] = self.text_model.encode(summary).tolist()
        
        # Payload
        payload = {
            "type": "audit_history",
            "contractor_id": contractor_id,
            "project_id": project_id,
            "status": status,
            "summary": summary,
            "timestamp": "2026-01-19T00:00:00" # In real app, use current time
        }

        point = q_models.PointStruct(
            id=self._generate_id(audit_id),
            vector=vectors,
            payload=payload
        )
        
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point],
                wait=True
            )
            logger.info(f"✅ Audit result stored for Contractor {contractor_id}.")
        except Exception as e:
            logger.error(f"Failed to store audit result: {e}")

    def get_contractor_history(self, contractor_id: str) -> List[Dict]:
        """
        Retrieves past audit history for a specific contractor.
        """
        if not self.client: return []
        
        try:
            # Scroll with filter
            filtr = q_models.Filter(
                must=[
                    q_models.FieldCondition(key="type", match=q_models.MatchValue(value="audit_history")),
                    q_models.FieldCondition(key="contractor_id", match=q_models.MatchValue(value=contractor_id))
                ]
            )
            
            results, _ = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=filtr,
                limit=10
            )
            return [res.payload for res in results]
        except Exception as e:
            logger.error(f"Failed to get contractor history: {e}")
            return []
