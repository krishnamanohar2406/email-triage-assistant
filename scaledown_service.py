"""
ScaleDown Service - Intelligent Prompt Compression
Reduces token usage by 60-80% while preserving meaning
"""

import requests
import json
from typing import Dict
from config import SCALEDOWN_API_KEY


class ScaleDownService:
    """Service for compressing prompts using ScaleDown API"""
    
    def __init__(self):
        self.api_key = SCALEDOWN_API_KEY
        self.base_url = "https://api.scaledown.xyz/compress/raw/"
        self.total_tokens_saved = 0
        self.compression_count = 0
    
    def compress_prompt(self, context: str, prompt: str) -> Dict:
        """
        Compress email context and analysis prompt
        
        Returns dict with:
        - compressed_prompt: The compressed text
        - original_tokens: Original token count
        - compressed_tokens: Compressed token count
        - savings_percent: Percentage saved
        - success: Whether compression succeeded
        """
        
        print(f"\n🗜️  ScaleDown Compression:")
        print(f"   Original context length: {len(context)} chars")
        print(f"   Original prompt length: {len(prompt)} chars")
        
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "context": context,
            "prompt": prompt,
            "scaledown": {"rate": "auto"}
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Parse ScaleDown response
            if 'results' in data:
                results = data['results']
                original_tokens = data.get('total_original_tokens', 0)
                compressed_tokens = data.get('total_compressed_tokens', 0)
                compressed_text = results.get('compressed_prompt', f"{context}\n\n{prompt}")
                
                savings = ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0
                
                # Track statistics
                self.total_tokens_saved += (original_tokens - compressed_tokens)
                self.compression_count += 1
                
                print(f"   ✓ Compressed: {original_tokens} → {compressed_tokens} tokens")
                print(f"   ✓ Savings: {savings:.1f}%")
                print(f"   ✓ Total saved this session: {self.total_tokens_saved} tokens")
                
                return {
                    'compressed_prompt': compressed_text,
                    'original_tokens': original_tokens,
                    'compressed_tokens': compressed_tokens,
                    'savings_percent': savings,
                    'success': True
                }
            else:
                # Fallback if format is different
                compressed_text = data.get('compressed_prompt', f"{context}\n\n{prompt}")
                return {
                    'compressed_prompt': compressed_text,
                    'original_tokens': 0,
                    'compressed_tokens': 0,
                    'savings_percent': 0,
                    'success': False
                }
        
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  ScaleDown API error: {e}")
            print(f"   → Falling back to uncompressed prompt")
            
            # Fallback: return uncompressed
            return {
                'compressed_prompt': f"{context}\n\n{prompt}",
                'original_tokens': 0,
                'compressed_tokens': 0,
                'savings_percent': 0,
                'success': False
            }
    
    def get_statistics(self) -> Dict:
        """Get compression statistics for this session"""
        return {
            'total_compressions': self.compression_count,
            'total_tokens_saved': self.total_tokens_saved,
            'average_savings': (self.total_tokens_saved / self.compression_count) if self.compression_count > 0 else 0
        }
