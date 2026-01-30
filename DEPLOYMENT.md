# Elasticsearch Agent Builder - Deployment Guide

## Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose OR
- Python 3.9+ with pip
- Elasticsearch 8.0+ running

### Option 1: Docker Compose (Fastest)

```bash
# 1. Clone or extract the project
cd elasticsearch-agent-builder

# 2. Start the stack
docker-compose up

# 3. Wait for Elasticsearch to be healthy (30 seconds)
# 4. Application available at: http://localhost:8000
# 5. API Docs at: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your Elasticsearch details

# 4. Start Elasticsearch (if not already running)
# Option A: Docker
docker run -d --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Option B: Local installation
# https://www.elastic.co/downloads/elasticsearch

# 5. Run the application
uvicorn src.main:app --reload

# 6. Access at: http://localhost:8000
```

---

## Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Test Agent
```bash
curl -X POST http://localhost:8000/api/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "How do I reset my password?",
    "sender_id": "test_user_1",
    "platform": "api",
    "channel": "test"
  }'
```

### 3. Interactive Docs
Open browser: `http://localhost:8000/docs`

---

## Configuration

### Environment Variables (.env)

```env
# Elasticsearch Connection
ES_HOST=https://localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=changeme
ES_INDEX_NAME=customer-support-kb
ES_VERIFY_CERTS=False
# Alternative: Use API Key
# ES_API_KEY=your_api_key_here

# Agent Configuration
AGENT_MODEL=gpt-3.5-turbo
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=1000

# Application
DEBUG=False
LOG_LEVEL=INFO
PORT=8000
HOST=0.0.0.0

# Social Platform APIs (Optional - for webhooks)
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_ID=your_phone_id
INSTAGRAM_TOKEN=your_instagram_token
INSTAGRAM_BUSINESS_ID=your_business_id
FACEBOOK_TOKEN=your_facebook_token
FACEBOOK_PAGE_ID=your_page_id
X_BEARER_TOKEN=your_x_token
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
WEBHOOK_VERIFY_TOKEN=verify_token_123
```

---

## Production Deployment

### Step 1: Prepare Docker Image

```bash
# Build image
docker build -t elasticsearch-agent:1.0.0 .

# Tag for registry
docker tag elasticsearch-agent:1.0.0 your-registry/elasticsearch-agent:1.0.0

# Push to registry
docker push your-registry/elasticsearch-agent:1.0.0
```

### Step 2: Deploy to Cloud

#### AWS Fargate
```bash
# 1. Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY
docker push your-registry/elasticsearch-agent:1.0.0

# 2. Create ECS task definition
# 3. Create Fargate service
# 4. Configure load balancer
```

#### Heroku
```bash
# 1. Login
heroku login

# 2. Create app
heroku create your-app-name

# 3. Add Elasticsearch addon
heroku addons:create heroku-elasticsearch:basic

# 4. Deploy
git push heroku main
```

#### DigitalOcean App Platform
```bash
# Push to GitHub, connect to App Platform, auto-deploy
git push origin main
```

### Step 3: Configure HTTPS

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Step 4: Setup Monitoring

#### Using DataDog
```python
# Add to requirements.txt
datadog
```

#### Using New Relic
```python
# Add to requirements.txt
newrelic
```

#### Using Prometheus
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'elasticsearch-agent'
    static_configs:
      - targets: ['localhost:8000']
```

### Step 5: Configure Webhooks

#### WhatsApp Setup
1. Go to Meta Business Platform
2. Create Webhook URL: `https://your-domain.com/webhooks/whatsapp`
3. Set Verify Token from `.env`
4. Subscribe to messages webhook
5. Add Webhook Token to `.env`

#### Facebook Setup
1. Go to Facebook Developers
2. Create app and page
3. Add Product: Messenger
4. Setup Webhook: `https://your-domain.com/webhooks/facebook`
5. Subscribe to messages
6. Add tokens to `.env`

#### Similar for Instagram, X, LinkedIn...

---

## Performance Optimization

### 1. Enable Caching
```python
# In config.py
CACHE_TTL = 3600  # 1 hour
CACHE_MAX_SIZE = 1000
```

### 2. Connection Pooling
```python
# Already configured in elasticsearch_client.py
# Default: 10 connections
```

### 3. Load Balancing
```yaml
# docker-compose.yml
services:
  agent1:
    build: .
  agent2:
    build: .
  agent3:
    build: .
  
  nginx:
    image: nginx
    ports:
      - "8000:8000"
    # upstream configuration...
```

### 4. Database Indexing
```python
# Automatic in ELSER setup
# Already optimized with sparse vectors
```

---

## Monitoring & Logging

### View Logs
```bash
# Docker
docker-compose logs -f agent

# Local
tail -f app.log
```

### Metrics to Monitor
- Request latency (p50, p95, p99)
- Error rate
- Elasticsearch health
- Conversation escalation rate
- Intent classification accuracy

### Setup Alerts
```yaml
# Example: Alert if error rate > 1%
alerts:
  - name: high_error_rate
    condition: error_rate > 0.01
    action: notify_slack
```

---

## Scaling

### Horizontal Scaling
```bash
# Docker Compose - add replicas
docker-compose up -d --scale agent=3

# Kubernetes
kubectl scale deployment elasticsearch-agent --replicas=3
```

### Vertical Scaling
```bash
# Increase resources
docker-compose.yml:
  services:
    agent:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

---

## Backup & Recovery

### Backup Elasticsearch Index
```bash
# Snapshot
curl -X PUT "localhost:9200/_snapshot/backup" -H 'Content-Type: application/json' -d '{
  "type": "fs",
  "settings": {
    "location": "/var/backups"
  }
}'

# Create snapshot
curl -X PUT "localhost:9200/_snapshot/backup/snapshot_1"
```

### Restore
```bash
curl -X POST "localhost:9200/_snapshot/backup/snapshot_1/_restore"
```

---

## Troubleshooting

### Issue: Can't connect to Elasticsearch
```
Solution:
1. Check ES_HOST in .env
2. Verify Elasticsearch is running
3. Check firewall rules
4. Verify credentials
```

### Issue: Slow response times
```
Solution:
1. Check ELSER model is loaded
2. Monitor ES cluster health
3. Add more replicas
4. Increase timeout settings
```

### Issue: High memory usage
```
Solution:
1. Reduce CACHE_MAX_SIZE
2. Limit conversation history
3. Add more worker processes
4. Monitor for memory leaks
```

---

## Security Considerations

### 1. API Authentication
```python
# Add to main.py
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/api/agent/message")
async def process_message(payload: dict, credentials: HTTPAuthCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    # ... rest of code
```

### 2. Rate Limiting
```python
# Add to requirements.txt
slowapi

# In main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/agent/message")
@limiter.limit("100/minute")
async def process_message(payload: dict):
    # ...
```

### 3. Input Validation
- Already implemented with Pydantic
- CORS configured
- SQL injection not applicable
- XSS protection via JSON encoding

### 4. Environment Secrets
```bash
# Use environment variables or secrets manager
# Never commit .env to git
# Rotate credentials regularly
# Use short-lived tokens
```

---

## Maintenance

### Weekly
- Check error logs
- Monitor performance metrics
- Verify backups

### Monthly
- Update dependencies
- Security patches
- Database maintenance
- Conversation cleanup

### Quarterly
- Load testing
- Disaster recovery drill
- Performance optimization review
- Security audit

---

## Support

For issues or questions:
- GitHub Issues: [link]
- Documentation: See README.md
- Email: support@company.com

---

## Checklist for Production

- [ ] Environment variables configured
- [ ] HTTPS certificate installed
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Error alerts configured
- [ ] Rate limiting enabled
- [ ] API authentication added
- [ ] Webhook tokens rotated
- [ ] Elasticsearch backed up
- [ ] Load testing completed
- [ ] Disaster recovery tested
- [ ] Team trained on operations

---

Successfully deployed! 🚀
