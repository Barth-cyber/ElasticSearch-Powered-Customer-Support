"""
FastAPI application for Elasticsearch Customer Support Agent
"""
import logging
import os
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any

from src.config import APP_CONFIG, PLATFORM_CONFIG
from src.elasticsearch_client import ElasticsearchClient as RealElasticsearchClient
try:
    from src.mock_elasticsearch_client import MockElasticsearchClient
except Exception:
    MockElasticsearchClient = None
from src.agent import CustomerSupportAgent, Message
from src.webhook_handlers import (
    WebhookValidator,
    PlatformMessageExtractor,
    PlatformResponseSender
)

# Setup logging
logging.basicConfig(
    level=APP_CONFIG.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Elasticsearch Customer Support Agent",
    description="AI-powered omnichannel customer support using Elasticsearch and ELSER",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
es_client = None
agent = None


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup with fallback to mock client"""
    global es_client, agent

    logger.info("🚀 Starting Elasticsearch Customer Support Agent...")

    use_mock = os.getenv("USE_MOCK_ES", "False").lower() == "true"

    try:
        if use_mock and MockElasticsearchClient is not None:
            es_client = MockElasticsearchClient()
            logger.info("Using mock Elasticsearch client (env USE_MOCK_ES=True)")
        else:
            try:
                es_client = RealElasticsearchClient()
                if not es_client.health_check():
                    raise Exception("Elasticsearch health check failed")
                logger.info("Connected to real Elasticsearch")
            except Exception as exc:
                logger.warning(f"Real Elasticsearch not available: {exc}")
                if MockElasticsearchClient is not None:
                    es_client = MockElasticsearchClient()
                    logger.info("Falling back to mock Elasticsearch client")
                else:
                    raise

        # Ensure index exists (mock will no-op)
        es_client.create_index_with_elser()

        # Initialize agent and inject chosen es_client
        agent = CustomerSupportAgent()
        try:
            # override agent's internal ES client if it was created inside agent
            agent.es_client = es_client
        except Exception:
            logger.warning("Unable to set agent.es_client override")

        logger.info("✓ All components initialized successfully")
    except Exception as e:
        logger.error(f"✗ Startup failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("⏹️ Shutting down...")


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "elasticsearch": "connected" if es_client and es_client.health_check() else "disconnected",
        "agent": "ready" if agent else "not initialized"
    }


@app.get("/status")
async def status() -> Dict[str, Any]:
    """Get system status"""
    return {
        "service": "Elasticsearch Customer Support Agent",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/api/knowledge-base/index")
async def index_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Index a document to the knowledge base"""
    try:
        doc_id = document.get("id", f"doc_{datetime.utcnow().timestamp()}")
        success = es_client.index_document(doc_id, document)
        
        return {
            "success": success,
            "document_id": doc_id,
            "message": "Document indexed successfully" if success else "Failed to index document"
        }
    except Exception as e:
        logger.error(f"Error indexing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-base/search")
async def search_knowledge_base(
    query: str = Query(..., description="Search query"),
    limit: int = Query(5, description="Max results")
) -> Dict[str, Any]:
    """Search the knowledge base"""
    try:
        results = es_client.semantic_search(query, size=limit)
        return {
            "query": query,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-base/document/{doc_id}")
async def get_knowledge_document(doc_id: str) -> Dict[str, Any]:
    """Get a specific document from knowledge base"""
    try:
        document = es_client.get_document(doc_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": doc_id,
            "document": document
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/message")
async def process_message(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Process a customer message through the agent"""
    try:
        message = Message(
            content=payload.get("content"),
            sender_id=payload.get("sender_id"),
            platform=payload.get("platform", "api"),
            channel=payload.get("channel", "api")
        )
        
        if not message.content or not message.sender_id:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: content, sender_id"
            )
        
        response = agent.process_message(message)
        
        return {
            "success": True,
            "response": response.content,
            "confidence": response.confidence,
            "sources": response.sources,
            "requires_escalation": response.requires_escalation,
            "action": response.action_type,
            "metadata": response.metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agent/conversation/{user_id}")
async def get_conversation(user_id: str) -> Dict[str, Any]:
    """Get conversation history for a user"""
    try:
        conversation = agent.get_conversation_summary(user_id)
        if not conversation:
            return {
                "user_id": user_id,
                "messages": [],
                "message": "No conversation history found"
            }
        
        return {
            "user_id": user_id,
            **conversation
        }
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request) -> JSONResponse:
    """WhatsApp webhook endpoint"""
    try:
        payload = await request.json()
        message_data = PlatformMessageExtractor.extract_whatsapp_message(payload)
        if not message_data:
            return JSONResponse({"success": True})
        
        message = Message(
            content=message_data["content"],
            sender_id=message_data["sender_id"],
            platform="whatsapp",
            channel="whatsapp"
        )
        
        response = agent.process_message(message)
        await PlatformResponseSender.send_whatsapp_message(
            message_data["sender_id"],
            response.content
        )
        
        return JSONResponse({"success": True})
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/webhooks/facebook")
async def facebook_webhook(request: Request) -> JSONResponse:
    """Facebook webhook endpoint"""
    try:
        payload = await request.json()
        message_data = PlatformMessageExtractor.extract_facebook_message(payload)
        if not message_data:
            return JSONResponse({"success": True})
        
        message = Message(
            content=message_data["content"],
            sender_id=message_data["sender_id"],
            platform="facebook",
            channel="facebook"
        )
        
        response = agent.process_message(message)
        await PlatformResponseSender.send_facebook_message(
            message_data["sender_id"],
            response.content
        )
        
        return JSONResponse({"success": True})
    except Exception as e:
        logger.error(f"Facebook webhook error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/webhooks/instagram")
async def instagram_webhook(request: Request) -> JSONResponse:
    """Instagram webhook endpoint"""
    try:
        payload = await request.json()
        message_data = PlatformMessageExtractor.extract_instagram_message(payload)
        if not message_data:
            return JSONResponse({"success": True})
        
        message = Message(
            content=message_data["content"],
            sender_id=message_data["sender_id"],
            platform="instagram",
            channel="instagram"
        )
        
        response = agent.process_message(message)
        await PlatformResponseSender.send_instagram_message(
            message_data["sender_id"],
            response.content
        )
        
        return JSONResponse({"success": True})
    except Exception as e:
        logger.error(f"Instagram webhook error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/webhooks/x")
async def x_webhook(request: Request) -> JSONResponse:
    """X (Twitter) webhook endpoint"""
    try:
        payload = await request.json()
        message_data = PlatformMessageExtractor.extract_x_message(payload)
        if not message_data:
            return JSONResponse({"success": True})
        
        message = Message(
            content=message_data["content"],
            sender_id=message_data["sender_id"],
            platform="x",
            channel="x"
        )
        
        response = agent.process_message(message)
        await PlatformResponseSender.send_x_message(
            message_data["sender_id"],
            response.content
        )
        
        return JSONResponse({"success": True})
    except Exception as e:
        logger.error(f"X webhook error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/webhooks/linkedin")
async def linkedin_webhook(request: Request) -> JSONResponse:
    """LinkedIn webhook endpoint"""
    try:
        payload = await request.json()
        message_data = PlatformMessageExtractor.extract_linkedin_message(payload)
        if not message_data:
            return JSONResponse({"success": True})
        
        message = Message(
            content=message_data["content"],
            sender_id=message_data["sender_id"],
            platform="linkedin",
            channel="linkedin"
        )
        
        response = agent.process_message(message)
        await PlatformResponseSender.send_linkedin_message(
            message_data["sender_id"],
            response.content
        )
        
        return JSONResponse({"success": True})
    except Exception as e:
        logger.error(f"LinkedIn webhook error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "service": "Elasticsearch Customer Support Agent",
        "documentation": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=APP_CONFIG.HOST,
        port=APP_CONFIG.PORT,
        reload=APP_CONFIG.DEBUG
    )
