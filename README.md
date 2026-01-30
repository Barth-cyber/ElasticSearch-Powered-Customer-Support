# Elasticsearch Agent Builder

## Overview
A sophisticated AI-powered omnichannel customer support agent that uses Elasticsearch and ELSER (Elastic Learned Sparse Encoder and Retriever) to understand and respond to customer queries across multiple social media platforms (WhatsApp, Facebook, Instagram, X/Twitter, LinkedIn).

## Architecture

```
┌─────────────────────────────────────────────┐
│          Customer Channels                   │
│  WhatsApp • Facebook • Instagram • X • LinkedIn
└────────────┬────────────────────────────────┘
             │ (Webhooks)
             ▼
┌─────────────────────────────────────────────┐
│    FastAPI Backend (Python)                 │
│  - Message Processing                       │
│  - Webhook Handlers                         │
│  - Agent Orchestration                      │
└────────────┬────────────────────────────────┘
             │ (Query + Context)
             ▼
┌─────────────────────────────────────────────┐
│    Elasticsearch + ELSER AI                 │
│  - Semantic Search                          │
│  - Intent Classification                    │
│  - Knowledge Retrieval                      │
└────────────┬────────────────────────────────┘
             │ (Search Results)
             ▼
┌─────────────────────────────────────────────┐
│    Knowledge Base                           │
│  - FAQs                                     │
│  - Product Info                             │
│  - Policies & Terms                         │
│  - Troubleshooting Guides                   │
└─────────────────────────────────────────────┘
```

## Features

✅ **Multi-Step AI Agent**
- Intent classification
- Semantic search via ELSER
- Conversation context tracking
- Confidence-based escalation

✅ **Omnichannel Support**
- WhatsApp integration
- Facebook Messenger
- Instagram Direct Messages
- X/Twitter mentions
- LinkedIn messages

✅ **Intelligent Routing**
- Automatic escalation detection
- Confidence scoring
- Source attribution
- Conversation history

✅ **Knowledge Management**
- Semantic search with ELSER
- Multi-category support
- Priority-based retrieval
- Real-time indexing

## Project Structure

```
elasticsearch-agent-builder/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── agent.py                # AI agent logic
│   ├── elasticsearch_client.py  # Elasticsearch integration
│   └── webhook_handlers.py      # Social platform webhooks
├── data/
│   └── knowledge_base.py        # Sample knowledge base data
├── tests/
│   ├── __init__.py
│   ├── test_agent.py            # Agent tests
│   └── test_webhooks.py         # Webhook tests
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image
├── docker-compose.yml           # Docker compose setup
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional)
- Elasticsearch 8.0+

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/elasticsearch-agent-builder.git
cd elasticsearch-agent-builder
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Start Elasticsearch**
```bash
# Option 1: Using Docker
docker run -d --name elasticsearch -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Option 2: Using Docker Compose
docker-compose up -d
```

### Docker Setup

```bash
# Start with Docker Compose
docker-compose up

# The agent will be available at http://localhost:8000
```

## Running the Application

### Development
```bash
# Using FastAPI directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m src.main
```

### Production
```bash
# Using Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

## API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /status` - System status
- `GET /` - Root endpoint

### Knowledge Base
- `POST /api/knowledge-base/index` - Index a document
- `GET /api/knowledge-base/search?query=...` - Search knowledge base
- `GET /api/knowledge-base/document/{doc_id}` - Get specific document

### Agent
- `POST /api/agent/message` - Process customer message
- `GET /api/agent/conversation/{user_id}` - Get conversation history

### Webhooks
- `POST /webhooks/whatsapp` - WhatsApp webhook
- `POST /webhooks/facebook` - Facebook webhook
- `POST /webhooks/instagram` - Instagram webhook
- `POST /webhooks/x` - X/Twitter webhook
- `POST /webhooks/linkedin` - LinkedIn webhook

## API Examples

### Process a Message
```bash
curl -X POST http://localhost:8000/api/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "How do I reset my password?",
    "sender_id": "user_123",
    "platform": "whatsapp",
    "channel": "whatsapp"
  }'
```

### Index Knowledge Document
```bash
curl -X POST http://localhost:8000/api/knowledge-base/index \
  -H "Content-Type: application/json" \
  -d '{
    "id": "doc_001",
    "title": "Password Reset",
    "content": "To reset your password...",
    "category": "account",
    "priority": 1
  }'
```

### Search Knowledge Base
```bash
curl "http://localhost:8000/api/knowledge-base/search?query=reset%20password&limit=5"
```

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_agent.py -v
pytest tests/test_webhooks.py -v
```

### Test Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

## Configuration

Configure via `.env` file:

```env
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

# Platform APIs
WHATSAPP_TOKEN=your_token
FACEBOOK_TOKEN=your_token
INSTAGRAM_TOKEN=your_token
X_BEARER_TOKEN=your_token
LINKEDIN_ACCESS_TOKEN=your_token
```

## How It Works

### Message Processing Flow

1. **Ingestion**: Message received via webhook
2. **Extraction**: Parse platform-specific format
3. **Intent Classification**: Determine customer intent
4. **Knowledge Retrieval**: Search knowledge base with ELSER
5. **Response Generation**: Generate contextual response
6. **Quality Assessment**: Evaluate confidence level
7. **Escalation Check**: Determine if human intervention needed
8. **Response Delivery**: Send via original platform

### Multi-Step Agent Logic

```python
# Step 1: Intent Classification
intent = agent._classify_intent(message.content)

# Step 2: Semantic Search
results = es_client.semantic_search(message.content)

# Step 3: Context Retrieval
context = agent._get_conversation_context(user_id)

# Step 4: Response Generation
response = agent._generate_response(
    message.content,
    intent,
    results,
    context
)

# Step 5: Quality Assessment
confidence, escalate = agent._assess_quality(
    response,
    message.content,
    results
)

# Step 6: Escalation Decision
if agent._should_escalate(message.content, escalate):
    return escalation_response()
```

## Elasticsearch ELSER Integration

ELSER provides semantic search capabilities:

- **Sparse Vector Embeddings**: Efficient semantic search
- **Hybrid Retrieval**: Combines sparse and dense vectors
- **Multi-language Support**: Supports 11+ languages
- **Low Latency**: Sub-millisecond search times

### Index Mapping with ELSER

```python
{
    "mappings": {
        "properties": {
            "content": {"type": "text"},
            "ml.inference.content_expanded": {
                "type": "sparse_vector"
            }
        }
    }
}
```

## Knowledge Base Structure

Each document includes:
- `id`: Unique identifier
- `title`: Document title
- `content`: Full content
- `category`: Category (account, billing, shipping, etc.)
- `priority`: Importance level
- `tags`: Search tags

## Platform Integration

### WhatsApp
- Cloud API integration
- Webhook-based messaging
- Automatic message delivery

### Facebook Messenger
- Graph API integration
- Conversation threading
- Read receipts

### Instagram
- Direct message support
- Story replies
- Feed comments

### X/Twitter
- Direct messages
- Mentions & replies
- Conversation threading

### LinkedIn
- InMail messaging
- Connection messages
- Business profile support

## Deployment

### Heroku
```bash
# Create Procfile
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app" > Procfile

# Deploy
heroku create your-app-name
heroku addons:create heroku-elasticsearch:basic
git push heroku main
```

### AWS
```bash
# Build and push Docker image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t elasticsearch-agent .
docker tag elasticsearch-agent:latest $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/elasticsearch-agent:latest
docker push $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/elasticsearch-agent:latest

# Deploy using ECS, EKS, or Fargate
```

## Monitoring & Logging

- Structured logging with timestamps
- Error tracking and reporting
- Performance metrics
- Conversation analytics

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/elasticsearch-agent-builder/issues)
- Email: support@company.com
- Documentation: [Full docs](https://docs.company.com)

## Roadmap

- [ ] Multi-language support
- [ ] Advanced NLP with BERT
- [ ] Sentiment analysis
- [ ] Custom training data support
- [ ] A/B testing framework
- [ ] Analytics dashboard
- [ ] Admin panel
- [ ] Webhook retry logic

## Authors

- Your Name - Initial work

## Acknowledgments

- Elasticsearch documentation
- FastAPI community
- Contributors and testers
