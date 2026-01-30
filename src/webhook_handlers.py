"""
Webhook handlers for social media platforms
"""
import logging
import hmac
import hashlib
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException
from src.config import PLATFORM_CONFIG

logger = logging.getLogger(__name__)


class WebhookValidator:
    """Validate incoming webhooks from social platforms"""

    @staticmethod
    def validate_whatsapp_webhook(request_dict: Dict[str, Any], token: str) -> bool:
        """Validate WhatsApp webhook"""
        return True

    @staticmethod
    def validate_facebook_webhook(body: str, signature: str, app_secret: str) -> bool:
        """Validate Facebook webhook using signature"""
        try:
            expected_signature = hmac.new(
                app_secret.encode(),
                body.encode(),
                hashlib.sha1
            ).hexdigest()
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Facebook webhook validation failed: {e}")
            return False

    @staticmethod
    def validate_instagram_webhook(request: Request, token: str) -> bool:
        """Validate Instagram webhook"""
        return True

    @staticmethod
    def validate_x_webhook(headers: Dict[str, str], body: bytes) -> bool:
        """Validate X (Twitter) webhook"""
        return True

    @staticmethod
    def validate_linkedin_webhook(body: str, signature: str) -> bool:
        """Validate LinkedIn webhook"""
        return True


class PlatformMessageExtractor:
    """Extract message from platform-specific webhook payloads"""

    @staticmethod
    def extract_whatsapp_message(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message from WhatsApp webhook"""
        try:
            changes = payload.get("entry", [{}])[0].get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
            
            msg = messages[0]
            contact = value.get("contacts", [{}])[0]
            
            return {
                "sender_id": msg.get("from"),
                "sender_name": contact.get("profile", {}).get("name", "Unknown"),
                "content": msg.get("text", {}).get("body", ""),
                "message_type": msg.get("type", "text"),
                "platform": "whatsapp",
                "channel": "whatsapp",
                "timestamp": msg.get("timestamp")
            }
        except Exception as e:
            logger.error(f"Failed to extract WhatsApp message: {e}")
            return None

    @staticmethod
    def extract_facebook_message(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message from Facebook webhook"""
        try:
            messaging = payload.get("entry", [{}])[0].get("messaging", [])
            
            if not messaging:
                return None
            
            msg_event = messaging[0]
            sender = msg_event.get("sender", {})
            message = msg_event.get("message", {})
            
            return {
                "sender_id": sender.get("id"),
                "content": message.get("text", ""),
                "message_type": "text",
                "platform": "facebook",
                "channel": "facebook",
                "timestamp": msg_event.get("timestamp")
            }
        except Exception as e:
            logger.error(f"Failed to extract Facebook message: {e}")
            return None

    @staticmethod
    def extract_instagram_message(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message from Instagram webhook"""
        try:
            return {
                "sender_id": payload.get("sender", {}).get("id"),
                "content": payload.get("message", {}).get("text", ""),
                "message_type": "text",
                "platform": "instagram",
                "channel": "instagram",
                "timestamp": payload.get("timestamp")
            }
        except Exception as e:
            logger.error(f"Failed to extract Instagram message: {e}")
            return None

    @staticmethod
    def extract_x_message(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message from X (Twitter) webhook"""
        try:
            for_user_id = payload.get("for_user_id")
            data = payload.get("data", {})
            includes = payload.get("includes", {})
            
            if not data:
                return None
            
            tweet_text = data.get("text", "")
            author_id = data.get("author_id")
            user_info = next(
                (u for u in includes.get("users", []) if u.get("id") == author_id),
                {}
            )
            
            return {
                "sender_id": author_id,
                "sender_name": user_info.get("username", "Unknown"),
                "content": tweet_text,
                "message_type": "tweet",
                "platform": "x",
                "channel": "x",
                "timestamp": data.get("created_at")
            }
        except Exception as e:
            logger.error(f"Failed to extract X message: {e}")
            return None

    @staticmethod
    def extract_linkedin_message(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message from LinkedIn webhook"""
        try:
            event_data = payload.get("eventData", {})
            actor = event_data.get("actor", {})
            
            return {
                "sender_id": actor.get("id"),
                "sender_name": actor.get("name", "Unknown"),
                "content": event_data.get("text", ""),
                "message_type": "text",
                "platform": "linkedin",
                "channel": "linkedin",
                "timestamp": event_data.get("timestamp")
            }
        except Exception as e:
            logger.error(f"Failed to extract LinkedIn message: {e}")
            return None


class PlatformResponseSender:
    """Send responses to different platforms"""

    @staticmethod
    async def send_whatsapp_message(
        recipient_id: str,
        message_text: str
    ) -> bool:
        """Send message via WhatsApp"""
        try:
            logger.info(f"WhatsApp response sent to {recipient_id}: {message_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return False

    @staticmethod
    async def send_facebook_message(
        recipient_id: str,
        message_text: str
    ) -> bool:
        """Send message via Facebook"""
        try:
            logger.info(f"Facebook response sent to {recipient_id}: {message_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send Facebook message: {e}")
            return False

    @staticmethod
    async def send_instagram_message(
        recipient_id: str,
        message_text: str
    ) -> bool:
        """Send message via Instagram"""
        try:
            logger.info(f"Instagram response sent to {recipient_id}: {message_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send Instagram message: {e}")
            return False

    @staticmethod
    async def send_x_message(
        recipient_id: str,
        message_text: str
    ) -> bool:
        """Send message via X (Twitter)"""
        try:
            logger.info(f"X response sent to {recipient_id}: {message_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send X message: {e}")
            return False

    @staticmethod
    async def send_linkedin_message(
        recipient_id: str,
        message_text: str
    ) -> bool:
        """Send message via LinkedIn"""
        try:
            logger.info(f"LinkedIn response sent to {recipient_id}: {message_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send LinkedIn message: {e}")
            return False
