"""
Email Analyzer - Intelligent Email Content Analysis
Deeply understands email content and context to make smart decisions
"""

import json
from typing import Dict
from dataclasses import dataclass
from enum import Enum

from scaledown_service import ScaleDownService
from gemini_service import GeminiService


class EmailCategory(Enum):
    """Email categories based on content analysis"""
    URGENT = "🚨 Urgent"
    IMPORTANT = "⭐ Important"
    NORMAL = "📧 Normal"
    LOW_PRIORITY = "📋 Low Priority"
    NEWSLETTER = "📰 Newsletter"
    SPAM = "🗑️ Spam"
    PROMOTIONAL = "🎁 Promotional"


class EmailAction(Enum):
    """Actions to perform based on email analysis"""
    STAR = "Star (Important)"
    MOVE_TO_SPAM = "Move to Spam"
    ARCHIVE = "Archive"
    MARK_READ = "Mark as Read"
    NOTHING = "No Action"


@dataclass
class EmailAnalysisResult:
    """Result of email analysis"""
    category: EmailCategory
    action: EmailAction
    priority_score: int  # 1-10
    summary: str
    reasoning: str
    key_points: list
    sentiment: str
    requires_response: bool


class EmailAnalyzer:
    """Analyzes email content using AI to understand context and intent"""
    
    def __init__(self):
        self.scaledown = ScaleDownService()
        self.gemini = GeminiService()
    
    def analyze(self, email_data: Dict) -> EmailAnalysisResult:
        """
        Deeply analyze email content to understand what it's about
        
        Args:
            email_data: Dict with 'sender', 'subject', 'body', 'date'
        
        Returns:
            EmailAnalysisResult with comprehensive analysis
        """
        
        print(f"\n{'='*70}")
        print(f"📧 ANALYZING EMAIL")
        print(f"{'='*70}")
        print(f"From: {email_data['sender']}")
        print(f"Subject: {email_data['subject']}")
        print(f"Date: {email_data['date']}")
        
        # Step 1: Build context for AI
        email_context = self._build_analysis_context(email_data)
        
        # Step 2: Build analysis prompt
        analysis_prompt = self._build_analysis_prompt()
        
        # Step 3: Compress using ScaleDown
        compression_result = self.scaledown.compress_prompt(email_context, analysis_prompt)
        compressed_prompt = compression_result['compressed_prompt']
        
        # Step 4: Get AI analysis
        ai_response = self.gemini.analyze_email(compressed_prompt)
        
        # Step 5: Parse and validate response
        if ai_response:
            return self._parse_ai_response(ai_response)
        else:
            print(f"   ⚠️  AI analysis failed, using fallback categorization")
            return self._fallback_analysis(email_data)
    
    def _build_analysis_context(self, email_data: Dict) -> str:
        """Build detailed email context for AI understanding"""
        
        return f"""
EMAIL TO DEEPLY ANALYZE AND UNDERSTAND:

Sender: {email_data['sender']}
Subject: {email_data['subject']}
Received: {email_data['date']}

Email Body:
{email_data['body']}

---

Please read and fully understand this email's content, context, and intent.
"""
    
    def _build_analysis_prompt(self) -> str:
        """Build comprehensive analysis prompt for AI"""
        
        return """
TASK: Analyze this email deeply and understand:
1. What is the sender trying to communicate?
2. What is the main purpose/intent of this email?
3. Does it require urgent action or response?
4. Is this legitimate communication or spam/promotional?
5. What is the emotional tone and importance level?

CATEGORIES:
- URGENT: Critical issues, emergencies, immediate deadlines, system failures
- IMPORTANT: From boss/clients, meetings, projects, work-related with deadlines
- NORMAL: Regular communication, updates, FYI messages
- LOW_PRIORITY: Can wait, informational only
- NEWSLETTER: Digest emails, regular subscriptions, news updates
- SPAM: Unsolicited, suspicious, phishing, scams
- PROMOTIONAL: Marketing, sales, offers, advertisements

ACTIONS:
- STAR: For urgent or important emails that need attention
- MOVE_TO_SPAM: For spam, scams, unsolicited emails
- ARCHIVE: For newsletters, promotions, low priority
- MARK_READ: For informational emails that don't need action
- NOTHING: For normal emails to keep in inbox

ANALYSIS RULES:
1. Read the CONTENT, not just keywords
2. Understand the CONTEXT and sender relationship
3. Consider the URGENCY and importance
4. Identify if it's LEGITIMATE or spam
5. Be smart about categorization

Respond in JSON format with your analysis:
{
  "category": "CATEGORY_NAME",
  "action": "ACTION_NAME",
  "priority_score": 1-10,
  "summary": "Brief summary of what this email is about",
  "reasoning": "Explain why you chose this category and action based on content",
  "key_points": ["main point 1", "main point 2", "main point 3"],
  "sentiment": "positive|negative|neutral|urgent",
  "requires_response": true|false
}

Think carefully and analyze the actual content and meaning.
"""
    
    def _parse_ai_response(self, ai_response: Dict) -> EmailAnalysisResult:
        """Parse AI response into structured result"""
        
        try:
            category_str = ai_response.get("category", "NORMAL")
            action_str = ai_response.get("action", "NOTHING")
            
            # Map to enums
            category = EmailCategory[category_str]
            action = EmailAction[action_str]
            
            result = EmailAnalysisResult(
                category=category,
                action=action,
                priority_score=ai_response.get("priority_score", 5),
                summary=ai_response.get("summary", "No summary provided"),
                reasoning=ai_response.get("reasoning", "No reasoning provided"),
                key_points=ai_response.get("key_points", []),
                sentiment=ai_response.get("sentiment", "neutral"),
                requires_response=ai_response.get("requires_response", False)
            )
            
            print(f"\n📊 Analysis Result:")
            print(f"   Category: {result.category.value}")
            print(f"   Action: {result.action.value}")
            print(f"   Priority: {result.priority_score}/10")
            print(f"   Sentiment: {result.sentiment}")
            print(f"   Summary: {result.summary}")
            print(f"   Reasoning: {result.reasoning}")
            
            return result
            
        except (KeyError, ValueError) as e:
            print(f"   ⚠️  Error parsing AI response: {e}")
            print(f"   Response was: {ai_response}")
            return self._create_default_result()
    
    def _fallback_analysis(self, email_data: Dict) -> EmailAnalysisResult:
        """Fallback analysis when AI fails"""
        
        # Simple keyword-based fallback
        subject_lower = email_data['subject'].lower()
        body_lower = email_data['body'].lower()
        
        # Check for obvious spam indicators
        spam_keywords = ['win', 'prize', 'click here', 'free money', '!!!', '$$$']
        if any(keyword in subject_lower or keyword in body_lower for keyword in spam_keywords):
            return EmailAnalysisResult(
                category=EmailCategory.SPAM,
                action=EmailAction.MOVE_TO_SPAM,
                priority_score=1,
                summary="Detected as spam based on content",
                reasoning="Contains spam indicators",
                key_points=["Spam detected"],
                sentiment="negative",
                requires_response=False
            )
        
        # Check for urgency
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        if any(keyword in subject_lower for keyword in urgent_keywords):
            return EmailAnalysisResult(
                category=EmailCategory.URGENT,
                action=EmailAction.STAR,
                priority_score=9,
                summary="Urgent email requiring attention",
                reasoning="Subject indicates urgency",
                key_points=["Urgent matter"],
                sentiment="urgent",
                requires_response=True
            )
        
        # Default: normal email
        return self._create_default_result()
    
    def _create_default_result(self) -> EmailAnalysisResult:
        """Create default analysis result"""
        return EmailAnalysisResult(
            category=EmailCategory.NORMAL,
            action=EmailAction.NOTHING,
            priority_score=5,
            summary="Regular email",
            reasoning="Could not determine specific category",
            key_points=["Regular communication"],
            sentiment="neutral",
            requires_response=False
        )
