"""
Gemini AI Service - Email Content Understanding and Analysis
Uses Google's Gemini AI to deeply understand email content
"""

import requests
import json
from typing import Optional, Dict
from config import GEMINI_API_KEY, ANALYSIS_TEMPERATURE, MAX_TOKENS_ANALYSIS


class GeminiService:
    """Service for AI-powered email analysis using Gemini"""
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.models = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
    
    def analyze_email(self, email_content: str) -> Optional[Dict]:
        """
        Analyze email content with deep understanding
        
        Args:
            email_content: The complete prompt (already compressed by ScaleDown)
        
        Returns:
            Dict with analysis or None if failed
        """
        
        print(f"\n🤖 Gemini AI Analysis:")
        print(f"   Sending to AI for deep content analysis...")
        
        # Try each model until one works
        for model_name in self.models:
            print(f"   Trying model: {model_name}")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            data = {
                "contents": [{
                    "parts": [{"text": email_content}]
                }],
                "generationConfig": {
                    "temperature": ANALYSIS_TEMPERATURE,
                    "maxOutputTokens": MAX_TOKENS_ANALYSIS,
                    "responseMimeType": "application/json"  # Force JSON output
                }
            }
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'candidates' in result and len(result['candidates']) > 0:
                        ai_text = result['candidates'][0]['content']['parts'][0]['text']
                        
                        print(f"   ✓ AI analysis received ({len(ai_text)} chars)")
                        
                        # Parse JSON response
                        try:
                            analysis = json.loads(ai_text)
                            print(f"   ✓ Parsed successfully")
                            return analysis
                        except json.JSONDecodeError as e:
                            print(f"   ⚠️  JSON parse error: {e}")
                            print(f"   Raw response: {ai_text[:200]}...")
                            continue
                    
                elif response.status_code == 404:
                    print(f"   ⚠️  Model not found, trying next...")
                    continue
                else:
                    print(f"   ⚠️  HTTP {response.status_code}, trying next...")
                    continue
                    
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                continue
        
        print(f"   ❌ All models failed")
        return None
    
    def generate_response_draft(self, email_context: str) -> Optional[str]:
        """Generate a draft response for an email"""
        
        print(f"\n✍️  Generating draft response...")
        
        for model_name in self.models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            data = {
                "contents": [{
                    "parts": [{"text": email_context}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 300
                }
            }
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'candidates' in result and len(result['candidates']) > 0:
                        draft = result['candidates'][0]['content']['parts'][0]['text']
                        print(f"   ✓ Draft generated")
                        return draft.strip()
                        
            except Exception:
                continue
        
        return None
