"""
Elasticsearch client and ELSER integration
"""
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from src.config import ES_CONFIG

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Elasticsearch client with ELSER support"""

    def __init__(self):
        """Initialize Elasticsearch client"""
        try:
            if ES_CONFIG.API_KEY:
                self.client = Elasticsearch(
                    [ES_CONFIG.HOST],
                    api_key=ES_CONFIG.API_KEY,
                    verify_certs=ES_CONFIG.VERIFY_CERTS
                )
            else:
                self.client = Elasticsearch(
                    [ES_CONFIG.HOST],
                    basic_auth=(ES_CONFIG.USERNAME, ES_CONFIG.PASSWORD),
                    verify_certs=ES_CONFIG.VERIFY_CERTS
                )
            logger.info("✓ Connected to Elasticsearch")
        except Exception as e:
            logger.error(f"✗ Failed to connect to Elasticsearch: {e}")
            raise

    def create_index_with_elser(self) -> bool:
        """Create knowledge base index with ELSER pipeline"""
        try:
            # Create ingest pipeline for ELSER
            pipeline_definition = {
                "processors": [
                    {
                        "inference": {
                            "model_id": ".elser_model_2",
                            "input_output": [
                                {
                                    "input_field": "content",
                                    "output_field": "ml.inference.content_expanded"
                                }
                            ]
                        }
                    }
                ]
            }

            self.client.ingest.put_pipeline(
                id="elser-pipeline",
                definition=pipeline_definition
            )
            logger.info("✓ ELSER pipeline created")

            # Create index with ELSER mapping
            if self.client.indices.exists(index=ES_CONFIG.INDEX_NAME):
                logger.info(f"Index {ES_CONFIG.INDEX_NAME} already exists")
                return True

            index_definition = {
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "category": {"type": "keyword"},
                        "priority": {"type": "integer"},
                        "created_at": {"type": "date"},
                        "ml": {
                            "properties": {
                                "inference": {
                                    "properties": {
                                        "content_expanded": {
                                            "type": "sparse_vector"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "index.default_pipeline": "elser-pipeline"
                }
            }

            self.client.indices.create(
                index=ES_CONFIG.INDEX_NAME,
                **index_definition
            )
            logger.info(f"✓ Index {ES_CONFIG.INDEX_NAME} created with ELSER")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to create index: {e}")
            return False

    def index_document(self, doc_id: str, document: Dict[str, Any]) -> bool:
        """Index a document in Elasticsearch"""
        try:
            self.client.index(
                index=ES_CONFIG.INDEX_NAME,
                id=doc_id,
                document=document
            )
            logger.debug(f"✓ Document {doc_id} indexed")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to index document: {e}")
            return False

    def semantic_search(self, query: str, size: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search using ELSER"""
        try:
            search_query = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "text_expansion": {
                                    "ml.inference.content_expanded": {
                                        "model_id": ".elser_model_2",
                                        "model_text": query
                                    }
                                }
                            },
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["title^2", "content"],
                                    "fuzziness": "AUTO"
                                }
                            }
                        ]
                    }
                },
                "size": size
            }

            response = self.client.search(index=ES_CONFIG.INDEX_NAME, **search_query)
            
            results = []
            for hit in response.get("hits", {}).get("hits", []):
                results.append({
                    "id": hit["_id"],
                    "score": hit["_score"],
                    **hit["_source"]
                })
            
            logger.debug(f"✓ Semantic search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"✗ Semantic search failed: {e}")
            return []

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific document"""
        try:
            response = self.client.get(index=ES_CONFIG.INDEX_NAME, id=doc_id)
            return response.get("_source")
        except NotFoundError:
            logger.warning(f"Document {doc_id} not found")
            return None
        except Exception as e:
            logger.error(f"✗ Failed to retrieve document: {e}")
            return None

    def health_check(self) -> bool:
        """Check Elasticsearch cluster health"""
        try:
            info = self.client.info()
            version = info.get("version", {}).get("number", "unknown")
            logger.info(f"✓ Elasticsearch health check passed (v{version})")
            return True
        except Exception as e:
            logger.error(f"✗ Elasticsearch health check failed: {e}")
            return False

    def delete_index(self) -> bool:
        """Delete the knowledge base index"""
        try:
            if self.client.indices.exists(index=ES_CONFIG.INDEX_NAME):
                self.client.indices.delete(index=ES_CONFIG.INDEX_NAME)
                logger.info(f"✓ Index {ES_CONFIG.INDEX_NAME} deleted")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to delete index: {e}")
            return False
