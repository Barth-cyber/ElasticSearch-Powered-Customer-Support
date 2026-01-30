"""Test webhook handlers"""
from src.webhook_handlers import PlatformMessageExtractor


def test_whatsapp_message_extraction():
    """Test WhatsApp message extraction"""
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "1234567890",
                        "text": {"body": "Hello"},
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
    
    result = PlatformMessageExtractor.extract_whatsapp_message(payload)
    assert result is not None
    assert result["sender_id"] == "1234567890"
    assert result["content"] == "Hello"
    assert result["platform"] == "whatsapp"


def test_facebook_message_extraction():
    """Test Facebook message extraction"""
    payload = {
        "entry": [{
            "messaging": [{
                "sender": {"id": "user123"},
                "message": {"text": "Hi there"},
                "timestamp": "1234567890"
            }]
        }]
    }
    
    result = PlatformMessageExtractor.extract_facebook_message(payload)
    assert result is not None
    assert result["sender_id"] == "user123"
    assert result["content"] == "Hi there"
    assert result["platform"] == "facebook"


if __name__ == "__main__":
    test_whatsapp_message_extraction()
    test_facebook_message_extraction()
    print("All webhook tests passed!")
