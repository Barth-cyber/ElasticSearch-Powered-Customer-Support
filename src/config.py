"""
Configuration management for the Elasticsearch Agent Builder
"""
import os
from dotenv import load_dotenv

load_dotenv()


class ElasticsearchConfig:
    """Elasticsearch connection configuration"""
    HOST = os.getenv("ES_HOST", "https://localhost:9200")
    USERNAME = os.getenv("ES_USERNAME", "elastic")
    PASSWORD = os.getenv("ES_PASSWORD", "changeme")
    INDEX_NAME = os.getenv("ES_INDEX_NAME", "customer-support-kb")
    API_KEY = os.getenv("ES_API_KEY", None)
    VERIFY_CERTS = os.getenv("ES_VERIFY_CERTS", "False").lower() == "true"


class AgentConfig:
    """AI Agent configuration"""
    MODEL = os.getenv("AGENT_MODEL", "gpt-3.5-turbo")
    TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "1000"))
    SYSTEM_PROMPT = """You are a professional customer support agent helping customers through multiple channels (WhatsApp, Instagram, Facebook, X, LinkedIn). 
    Be friendly, professional, and concise. Always try to resolve issues efficiently.
    If you don't have information, offer to escalate to a human agent."""


class AppConfig:
    """Application configuration"""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")


class PlatformConfig:
    """Social platform API credentials"""
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
    INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN", "")
    INSTAGRAM_BUSINESS_ID = os.getenv("INSTAGRAM_BUSINESS_ID", "")
    FACEBOOK_TOKEN = os.getenv("FACEBOOK_TOKEN", "")
    FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
    X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "verify_token_123")


# Export all configurations
ES_CONFIG = ElasticsearchConfig()
AGENT_CONFIG = AgentConfig()
APP_CONFIG = AppConfig()
PLATFORM_CONFIG = PlatformConfig()
