"""
Test utilities and sample test cases
"""
import pytest
from src.agent import CustomerSupportAgent, Message
from datetime import datetime


@pytest.fixture
def agent():
    """Create agent instance for testing"""
    return CustomerSupportAgent()


@pytest.fixture
def sample_message():
    """Create sample customer message"""
    return Message(
        content="I forgot my password",
        sender_id="user_123",
        platform="whatsapp",
        channel="whatsapp",
        timestamp=datetime.utcnow()
    )


def test_intent_classification(agent):
    """Test intent classification"""
    test_cases = [
        ("I forgot my password", "account"),
        ("How much does this cost?", "billing"),
        ("My app keeps crashing", "technical"),
        ("Where's my order?", "shipping"),
        ("Hi there", "general"),
    ]
    
    for message, expected_intent in test_cases:
        intent = agent._classify_intent(message)
        assert intent in ["account", "billing", "technical", "shipping", "product", "complaint", "general"]


def test_should_escalate(agent):
    """Test escalation detection"""
    escalation_messages = [
        "I want to speak to a manager",
        "This is urgent!",
        "I'm very angry with your service",
        "I need a lawyer",
    ]
    
    for msg in escalation_messages:
        should_escalate = agent._should_escalate(msg, False)
        assert should_escalate is True


def test_conversation_storage(agent, sample_message):
    """Test conversation history storage"""
    user_id = sample_message.sender_id
    response = "Here's your answer"
    
    agent._store_conversation(user_id, sample_message, response)
    summary = agent.get_conversation_summary(user_id)
    
    assert summary is not None
    assert len(summary["messages"]) > 0
    assert summary["messages"][0]["user"] == sample_message.content


def test_response_generation(agent):
    """Test response generation"""
    message_content = "I need help resetting my password"
    intent = "account"
    knowledge_results = [
        {
            "id": "faq_001",
            "title": "How do I reset my password?",
            "content": "To reset: click forgot password...",
            "score": 4.5
        }
    ]
    context = {}
    
    response = agent._generate_response(
        message_content,
        intent,
        knowledge_results,
        context
    )
    
    assert response is not None
    assert len(response) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
