"""
Setup script for initializing the knowledge base
"""
import logging
from src.elasticsearch_client import ElasticsearchClient
from data.knowledge_base import KNOWLEDGE_BASE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_knowledge_base():
    """Initialize and populate the knowledge base"""
    try:
        logger.info("Initializing Elasticsearch Agent Builder...")
        
        # Create client
        es_client = ElasticsearchClient()
        
        # Health check
        if not es_client.health_check():
            logger.error("Elasticsearch is not available")
            return False
        
        # Create index with ELSER
        if not es_client.create_index_with_elser():
            logger.error("Failed to create index")
            return False
        
        # Index knowledge base documents
        logger.info(f"Indexing {len(KNOWLEDGE_BASE)} documents...")
        for i, doc in enumerate(KNOWLEDGE_BASE, 1):
            success = es_client.index_document(doc.get("id"), doc)
            if success:
                logger.info(f"✓ Indexed document {i}/{len(KNOWLEDGE_BASE)}: {doc.get('title')}")
            else:
                logger.error(f"✗ Failed to index document: {doc.get('id')}")
        
        logger.info("✓ Knowledge base setup complete!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Setup failed: {e}")
        return False


if __name__ == "__main__":
    setup_knowledge_base()
