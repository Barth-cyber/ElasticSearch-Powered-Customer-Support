"""
Sample knowledge base data for customer support
"""

KNOWLEDGE_BASE = [
    {
        "id": "faq_001",
        "title": "How do I reset my password?",
        "content": "To reset your password: 1) Click 'Forgot Password' on the login page, 2) Enter your email address, 3) Check your email for reset link, 4) Click the link and create a new password, 5) Use your new password to log in.",
        "category": "account",
        "priority": 1,
        "tags": ["password", "account", "login", "reset"]
    },
    {
        "id": "faq_002",
        "title": "What payment methods do you accept?",
        "content": "We accept all major credit cards (Visa, Mastercard, American Express), PayPal, Apple Pay, Google Pay, and bank transfers. All payments are processed securely through encrypted connections.",
        "category": "billing",
        "priority": 1,
        "tags": ["payment", "billing", "methods", "card"]
    },
    {
        "id": "faq_003",
        "title": "What is your refund policy?",
        "content": "We offer a 30-day money-back guarantee. If you're not satisfied with your purchase, contact our support team within 30 days with your order number, and we'll process a full refund to your original payment method within 5-7 business days.",
        "category": "billing",
        "priority": 1,
        "tags": ["refund", "money-back", "policy", "return"]
    },
    {
        "id": "faq_004",
        "title": "How long does shipping take?",
        "content": "Shipping times vary: Standard Shipping (5-7 business days), Express Shipping (2-3 business days), Overnight Shipping (1 business day). Orders are processed within 24 hours. Free shipping is available on orders over $50.",
        "category": "shipping",
        "priority": 2,
        "tags": ["shipping", "delivery", "speed", "time"]
    },
    {
        "id": "faq_005",
        "title": "Can I track my order?",
        "content": "Yes, you can track your order in real-time. Log into your account, go to 'My Orders', and click 'Track' next to your order. You'll receive tracking updates via email automatically.",
        "category": "shipping",
        "priority": 2,
        "tags": ["track", "order", "delivery", "status"]
    },
    {
        "id": "faq_006",
        "title": "What should I do if I received a damaged product?",
        "content": "If you receive a damaged product: 1) Take photos of the damage, 2) Contact support with your order number and photos, 3) We'll arrange a replacement or refund, 4) Return shipping is covered by us.",
        "category": "product",
        "priority": 1,
        "tags": ["damaged", "defective", "problem", "issue"]
    },
    {
        "id": "faq_007",
        "title": "Do you offer bulk discounts?",
        "content": "Yes! We offer volume discounts: 10-49 units (10% off), 50-99 units (15% off), 100+ units (20% off). Contact our sales team for bulk orders at sales@company.com or call 1-800-XXX-XXXX.",
        "category": "billing",
        "priority": 3,
        "tags": ["discount", "bulk", "wholesale", "pricing"]
    },
    {
        "id": "faq_008",
        "title": "How do I contact customer support?",
        "content": "You can reach us through multiple channels: Email: support@company.com, Phone: 1-800-XXX-XXXX (Mon-Fri 9AM-6PM EST), Live Chat: Available on our website 24/7, Social Media: @ourcompany on all platforms.",
        "category": "general",
        "priority": 1,
        "tags": ["support", "contact", "help", "reach"]
    },
    {
        "id": "faq_009",
        "title": "What warranty do you provide?",
        "content": "All products come with a 1-year manufacturer's warranty covering defects in materials and workmanship. Extended warranties (2-5 years) are available at purchase. Warranty does not cover accidental damage or normal wear.",
        "category": "product",
        "priority": 2,
        "tags": ["warranty", "guarantee", "coverage", "protection"]
    },
    {
        "id": "faq_010",
        "title": "Can I change my order after placing it?",
        "content": "Orders can be modified within 1 hour of placement before processing begins. To change your order, contact support immediately with your order number. If already processed, you can cancel and place a new order.",
        "category": "order",
        "priority": 2,
        "tags": ["order", "change", "modify", "cancel"]
    },
    {
        "id": "technical_001",
        "title": "The app keeps crashing on my device",
        "content": "Try these troubleshooting steps: 1) Force close the app and restart, 2) Clear app cache (Settings > Apps > Clear Cache), 3) Ensure you have the latest version from app store, 4) Free up phone storage space, 5) Restart your device. If problems persist, uninstall and reinstall the app.",
        "category": "technical",
        "priority": 1,
        "tags": ["crash", "app", "bug", "error", "fix"]
    },
    {
        "id": "technical_002",
        "title": "I'm getting a login error",
        "content": "If you can't log in: 1) Verify your internet connection is stable, 2) Check that Caps Lock is off, 3) Try resetting your password, 4) Clear your browser cookies/cache, 5) Try a different browser or device. Contact support if the issue persists.",
        "category": "technical",
        "priority": 1,
        "tags": ["login", "error", "authentication", "access"]
    },
    {
        "id": "technical_003",
        "title": "How do I enable two-factor authentication?",
        "content": "To enable 2FA: 1) Go to Account Settings, 2) Select Security, 3) Click 'Enable Two-Factor Authentication', 4) Choose email or SMS, 5) Enter the code sent to verify. We recommend 2FA for enhanced security.",
        "category": "account",
        "priority": 2,
        "tags": ["2fa", "security", "authentication", "protection"]
    }
]

# Index this data into Elasticsearch when initializing
