"""
Simple mock Elasticsearch client for local/demo mode.
Stores documents in memory and provides a basic semantic_search fallback.
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MockElasticsearchClient:
    def __init__(self):
        self.index_name = "mock-kb"
        self._docs: Dict[str, Dict[str, Any]] = {}
        logger.info("Using MockElasticsearchClient (in-memory)")

    def create_index_with_elser(self) -> bool:
        # No-op for mock
        logger.info("Mock: create_index_with_elser called")
        return True

    def index_document(self, doc_id: str, document: Dict[str, Any]) -> bool:
        doc = document.copy()
        if "created_at" not in doc:
            doc["created_at"] = datetime.utcnow().isoformat()
        self._docs[doc_id] = doc
        logger.debug(f"Mock: Indexed document {doc_id}")
        return True

    def semantic_search(self, query: str, size: int = 5) -> List[Dict[str, Any]]:
        # Very small heuristic: rank by number of query tokens found in title+content
        q = (query or "").lower()
        tokens = [t for t in q.split() if t]
        results: List[Dict[str, Any]] = []

        for doc_id, src in self._docs.items():
            text = f"{src.get('title','')} {src.get('content','')}`".lower()
            score = 0
            for t in tokens:
                if t in text:
                    score += 1
            if score > 0:
                results.append({
                    "id": doc_id,
                    "score": float(score),
                    **src
                })

        # fallback: if no token matches, do substring match
        if not results:
            for doc_id, src in self._docs.items():
                text = f"{src.get('title','')} {src.get('content','')}`".lower()
                if q in text:
                    results.append({
                        "id": doc_id,
                        "score": 0.5,
                        **src
                    })

        # sort and limit
        results.sort(key=lambda r: r.get("score", 0), reverse=True)
        return results[:size]

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self._docs.get(doc_id)

    def health_check(self) -> bool:
        # Mock is always healthy
        return True

    def delete_index(self) -> bool:
        self._docs = {}
        logger.info("Mock: index cleared")
        return True
