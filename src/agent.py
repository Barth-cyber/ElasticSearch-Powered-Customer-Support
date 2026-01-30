"""
Multi-step AI Agent for customer support
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from src.elasticsearch_client import ElasticsearchClient
from src.config import AGENT_CONFIG

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Customer message"""
    content: str
    sender_id: str
    platform: str
    channel: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class AgentResponse:
    """Agent response"""
    content: str
    confidence: float
    sources: List[str]
    requires_escalation: bool
    action_type: str  # 'reply', 'escalate', 'follow_up'
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class CustomerSupportAgent:
    """Multi-step AI agent for customer support"""

    def __init__(self):
        """Initialize the agent"""
        self.es_client = ElasticsearchClient()
        self.conversation_history = {}  # Store conversation context per user
        self.escalation_keywords = [
            "escalate", "manager", "complaint", "urgent", "angry", 
            "refund", "legal", "lawsuit", "speak to", "supervisor",
            "lawyer", "very angry", "frustrated", "furious"
        ]

    def process_message(self, message: Message) -> AgentResponse:
        """
        Process customer message through multi-step pipeline
        
        Steps:
        1. Intent classification
        2. Knowledge retrieval via semantic search
        3. Response generation
        4. Quality assessment
        5. Escalation check
        """
        logger.info(f"Processing message from {message.sender_id} on {message.platform}")

        # Step 1: Intent Classification
        intent = self._classify_intent(message.content)
        logger.debug(f"Detected intent: {intent}")

        # Step 2: Knowledge Retrieval
        knowledge_results = self.es_client.semantic_search(message.content, size=5)
        if not knowledge_results:
            logger.warning("No relevant knowledge found")
            return self._escalation_response(message, "No matching knowledge base entry")

        # Step 3: Context and Conversation History
        conversation_context = self._get_conversation_context(message.sender_id)

        # Step 4: Response Generation
        response_content = self._generate_response(
            message.content,
            intent,
            knowledge_results,
            conversation_context
        )

        # Step 5: Quality Assessment
        confidence, requires_escalation = self._assess_quality(
            response_content,
            message.content,
            knowledge_results
        )

        # Step 6: Escalation Check
        if self._should_escalate(message.content, requires_escalation):
            return self._escalation_response(message, response_content)

        # Store conversation
        self._store_conversation(message.sender_id, message, response_content)

        # Extract sources
        sources = [result.get("title", f"Document {result.get('id')}") 
                  for result in knowledge_results[:3]]

        return AgentResponse(
            content=response_content,
            confidence=confidence,
            sources=sources,
            requires_escalation=False,
            action_type="reply",
            metadata={
                "intent": intent,
                "platform": message.platform,
                "channel": message.channel,
                "timestamp": message.timestamp.isoformat()
            }
        )

    def _classify_intent(self, message: str) -> str:
        """Classify customer intent"""
        message_lower = message.lower()
        
        intents = {
            "billing": ["price", "cost", "bill", "invoice", "payment", "charge", "refund"],
            "technical": ["error", "bug", "crash", "not working", "broken", "issue", "problem"],
            "account": ["account", "login", "password", "reset", "verify", "2fa"],
            "shipping": ["shipping", "delivery", "track", "order", "package"],
            "product": ["product", "feature", "how to", "guide", "tutorial"],
            "complaint": ["bad", "poor", "terrible", "worst", "angry", "frustrated"],
            "general": ["hello", "hi", "thanks", "thank you", "ok", "okay"]
        }
        
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return "general"

    def _get_conversation_context(self, user_id: str) -> Dict[str, Any]:
        """Retrieve conversation context for user"""
        return self.conversation_history.get(user_id, {
            "messages": [],
            "intent_history": [],
            "escalations": 0,
            "first_contact": datetime.utcnow().isoformat()
        })

    def _generate_response(
        self,
        user_message: str,
        intent: str,
        knowledge_results: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> str:
        """Generate response based on knowledge base and context"""
        
        if not knowledge_results:
            return "I apologize, but I couldn't find information about your inquiry. Let me connect you with a specialist."
        
        best_match = knowledge_results[0]
        confidence = best_match.get("score", 0)
        
        # Response templates based on confidence
        if confidence > 3.0:
            # High confidence
            response = f"I found information that might help: {best_match.get('content', '')}\n\n"
            if len(knowledge_results) > 1:
                response += f"You might also find this helpful: {knowledge_results[1].get('title', '')}"
        elif confidence > 1.0:
            # Medium confidence
            response = f"Based on what you're asking about: {best_match.get('content', '')}\n\n"
            response += "If this doesn't fully answer your question, could you provide more details?"
        else:
            # Low confidence
            response = f"Thank you for reaching out. Here's what I found: {best_match.get('content', '')}\n\n"
            response += "If you need further assistance, I can escalate this to our support team."
        
        # Add context-specific adjustments
        if context.get("escalations", 0) > 0:
            response += "\n\nI apologize for any previous inconvenience. I'm here to help resolve this."
        
        return response

    def _assess_quality(
        self,
        response: str,
        user_message: str,
        knowledge_results: List[Dict[str, Any]]
    ) -> tuple:
        """Assess response quality"""
        
        confidence = 0.5  # Default
        requires_escalation = False
        
        if not knowledge_results:
            confidence = 0.2
            requires_escalation = True
        else:
            top_score = knowledge_results[0].get("score", 0)
            if top_score > 3.0:
                confidence = 0.9
            elif top_score > 1.0:
                confidence = 0.6
            else:
                confidence = 0.3
                requires_escalation = True
        
        # Check response length
        if len(response) < 20:
            confidence *= 0.8
            requires_escalation = True
        
        return min(confidence, 1.0), requires_escalation

    def _should_escalate(self, message: str, quality_flag: bool) -> bool:
        """Determine if message should be escalated"""
        
        # Check escalation keywords
        for keyword in self.escalation_keywords:
            if keyword.lower() in message.lower():
                return True
        
        # Escalate if quality assessment flagged it
        if quality_flag:
            return True
        
        return False

    def _escalation_response(self, message: Message, reason: str) -> AgentResponse:
        """Generate escalation response"""
        return AgentResponse(
            content=f"{reason}\n\nI'm connecting you with a human specialist who can better assist you. Thank you for your patience!",
            confidence=0.5,
            sources=["Human Escalation"],
            requires_escalation=True,
            action_type="escalate",
            metadata={
                "reason": reason,
                "platform": message.platform,
                "channel": message.channel,
                "timestamp": message.timestamp.isoformat()
            }
        )

    def _store_conversation(self, user_id: str, message: Message, response: str):
        """Store conversation for future context"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = {
                "messages": [],
                "intent_history": [],
                "escalations": 0,
                "first_contact": datetime.utcnow().isoformat()
            }
        
        self.conversation_history[user_id]["messages"].append({
            "user": message.content,
            "bot": response,
            "timestamp": message.timestamp.isoformat()
        })

    def get_conversation_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of user conversation"""
        return self.conversation_history.get(user_id)
