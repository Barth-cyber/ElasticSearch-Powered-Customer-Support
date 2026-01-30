"""
API Testing and Demo Script
Demonstrates all API endpoints and functionality
"""
import json
import asyncio
from datetime import datetime


def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_demo_endpoint(method, endpoint, description):
    """Print endpoint demo info"""
    print(f"[{method:6}] {endpoint:40} - {description}")


async def demo_api():
    """Demonstrate all API endpoints"""
    
    print_section("ELASTICSEARCH CUSTOMER SUPPORT AGENT - API DEMO")
    
    print("""
    This demo shows how to interact with the Elasticsearch Customer Support Agent.
    
    Architecture:
    - FastAPI backend for request handling
    - Elasticsearch + ELSER for semantic search
    - Multi-step AI agent for intelligent responses
    - Omnichannel webhook support
    
    """)
    
    print_section("1. HEALTH & STATUS ENDPOINTS")
    print_demo_endpoint("GET", "/health", "Check system health")
    print_demo_endpoint("GET", "/status", "Get system status")
    print_demo_endpoint("GET", "/", "Root endpoint")
    
    print("""
    Example: curl http://localhost:8000/health
    Response:
    {
      "status": "healthy",
      "elasticsearch": "connected",
      "agent": "ready"
    }
    """)
    
    print_section("2. KNOWLEDGE BASE MANAGEMENT")
    print_demo_endpoint("POST", "/api/knowledge-base/index", "Index a document")
    print_demo_endpoint("GET", "/api/knowledge-base/search", "Search knowledge base")
    print_demo_endpoint("GET", "/api/knowledge-base/document/{id}", "Get specific document")
    
    print("""
    Index a Document:
    curl -X POST http://localhost:8000/api/knowledge-base/index \\
      -H "Content-Type: application/json" \\
      -d '{
        "id": "doc_001",
        "title": "Password Reset Guide",
        "content": "To reset your password...",
        "category": "account",
        "priority": 1
      }'
    
    Search Knowledge Base:
    curl "http://localhost:8000/api/knowledge-base/search?query=password%20reset&limit=5"
    
    Response:
    {
      "query": "password reset",
      "results_count": 2,
      "results": [
        {
          "id": "doc_001",
          "score": 4.5,
          "title": "Password Reset Guide",
          "content": "...",
          "category": "account"
        }
      ]
    }
    """)
    
    print_section("3. AGENT MESSAGE PROCESSING")
    print_demo_endpoint("POST", "/api/agent/message", "Process customer message")
    print_demo_endpoint("GET", "/api/agent/conversation/{user_id}", "Get conversation history")
    
    print("""
    Process Message:
    curl -X POST http://localhost:8000/api/agent/message \\
      -H "Content-Type: application/json" \\
      -d '{
        "content": "I forgot my password, can you help?",
        "sender_id": "user_123",
        "platform": "whatsapp",
        "channel": "whatsapp"
      }'
    
    Response:
    {
      "success": true,
      "response": "To reset your password: 1) Click 'Forgot Password'...",
      "confidence": 0.95,
      "sources": ["Password Reset Guide"],
      "requires_escalation": false,
      "action": "reply",
      "metadata": {
        "intent": "account",
        "platform": "whatsapp",
        "channel": "whatsapp",
        "timestamp": "2026-01-30T10:00:00"
      }
    }
    
    Get Conversation History:
    curl "http://localhost:8000/api/agent/conversation/user_123"
    """)
    
    print_section("4. WEBHOOK ENDPOINTS")
    print_demo_endpoint("POST", "/webhooks/whatsapp", "WhatsApp messages")
    print_demo_endpoint("POST", "/webhooks/facebook", "Facebook messages")
    print_demo_endpoint("POST", "/webhooks/instagram", "Instagram messages")
    print_demo_endpoint("POST", "/webhooks/x", "X/Twitter messages")
    print_demo_endpoint("POST", "/webhooks/linkedin", "LinkedIn messages")
    
    print("""
    WhatsApp Webhook Example Payload:
    {
      "entry": [{
        "changes": [{
          "value": {
            "messages": [{
              "from": "1234567890",
              "text": {"body": "How do I reset my password?"},
              "type": "text",
              "timestamp": "1234567890"
            }],
            "contacts": [{
              "profile": {"name": "John"}
            }]
          }
        }]
      }]
    }
    """)
    
    print_section("5. AGENT MULTI-STEP LOGIC")
    print("""
    The agent processes messages through these steps:
    
    1. INTENT CLASSIFICATION
       - Analyzes customer message
       - Classifies into categories: account, billing, technical, shipping, etc.
    
    2. SEMANTIC SEARCH
       - Uses Elasticsearch ELSER for semantic understanding
       - Retrieves relevant knowledge base documents
       - Provides confidence scoring
    
    3. CONTEXT RETRIEVAL
       - Pulls conversation history
       - Maintains user session state
       - Tracks previous escalations
    
    4. RESPONSE GENERATION
       - Generates contextual response based on:
         * Retrieved knowledge
         * Customer intent
         * Conversation history
         * Confidence levels
    
    5. QUALITY ASSESSMENT
       - Evaluates response quality
       - Calculates confidence score
       - Determines escalation flag
    
    6. ESCALATION CHECK
       - Monitors for escalation keywords
       - Checks quality assessment flags
       - Routes to human agent if needed
    
    7. RESPONSE DELIVERY
       - Sends via original platform
       - Stores conversation record
       - Tracks metrics
    """)
    
    print_section("6. RESPONSE EXAMPLES")
    
    print("""
    HIGH CONFIDENCE RESPONSE (score > 3.0):
    "I found exactly what you're looking for: [Detailed answer]
    This should completely resolve your issue. Let me know if you need anything else!"
    
    MEDIUM CONFIDENCE RESPONSE (score 1.0-3.0):
    "Based on your question: [Answer]
    If this doesn't fully address your issue, could you provide more details?"
    
    LOW CONFIDENCE RESPONSE (score < 1.0):
    "Thank you for reaching out. Here's what I found: [Answer]
    If you need further assistance, I can escalate this to our support team."
    
    ESCALATION RESPONSE:
    "I'm connecting you with a human specialist who can better assist you.
    Thank you for your patience!"
    """)
    
    print_section("7. INTENT EXAMPLES")
    
    examples = {
        "account": ["How do I reset my password?", "I can't log in", "Enable 2FA"],
        "billing": ["How much does this cost?", "I need a refund", "What's your pricing?"],
        "technical": ["The app keeps crashing", "I'm getting an error", "This feature isn't working"],
        "shipping": ["Where's my order?", "How long for delivery?", "Can I track my package?"],
        "product": ["How do I use this?", "What are the features?", "Is it compatible with...?"],
    }
    
    for intent, queries in examples.items():
        print(f"\n  {intent.upper()}:")
        for query in queries:
            print(f"    • {query}")
    
    print_section("8. ESCALATION TRIGGERS")
    
    triggers = [
        "I want to speak to a manager",
        "This is urgent",
        "I'm very angry",
        "I need legal assistance",
        "I want a refund NOW",
        "This is unacceptable",
        "I need to escalate",
    ]
    
    for trigger in triggers:
        print(f"  • {trigger}")
    
    print_section("9. GETTING STARTED")
    
    print("""
    1. Start the application:
       uvicorn src.main:app --reload
    
    2. Access interactive API docs:
       http://localhost:8000/docs
    
    3. Run tests:
       pytest tests/ -v
    
    4. Index knowledge base:
       python setup.py
    
    5. Try a test message:
       curl -X POST http://localhost:8000/api/agent/message \\
         -H "Content-Type: application/json" \\
         -d '{
           "content": "I forgot my password",
           "sender_id": "test_user",
           "platform": "api",
           "channel": "api"
         }'
    """)
    
    print_section("10. CONFIGURATION")
    
    print("""
    Environment Variables (.env):
    
    # Elasticsearch
    ES_HOST=https://localhost:9200
    ES_USERNAME=elastic
    ES_PASSWORD=changeme
    ES_INDEX_NAME=customer-support-kb
    ES_VERIFY_CERTS=False
    
    # Agent
    AGENT_MODEL=gpt-3.5-turbo
    AGENT_TEMPERATURE=0.7
    AGENT_MAX_TOKENS=1000
    
    # Application
    DEBUG=False
    LOG_LEVEL=INFO
    PORT=8000
    HOST=0.0.0.0
    """)
    
    print_section("SUMMARY")
    
    print("""
    ✓ Multi-step AI agent for intelligent customer support
    ✓ Elasticsearch with ELSER for semantic search
    ✓ Omnichannel webhook support (5 platforms)
    ✓ Intent classification and escalation detection
    ✓ Conversation history and context awareness
    ✓ RESTful API with comprehensive endpoints
    ✓ Production-ready with Docker support
    ✓ Fully tested and validated
    
    For more information, see README.md
    """)


if __name__ == "__main__":
    asyncio.run(demo_api())
