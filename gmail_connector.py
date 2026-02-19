"""
Gmail Connector - Handle Gmail IMAP connections and email operations
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from config import GMAIL_IMAP_SERVER, MAX_EMAIL_BODY_LENGTH


class GmailConnector:
    """Manages Gmail IMAP connection and email operations"""
    
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.imap = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish connection to Gmail IMAP server"""
        
        print(f"\n🔌 Connecting to Gmail...")
        print(f"   Server: {GMAIL_IMAP_SERVER}")
        print(f"   Email: {self.email_address}")
        
        try:
            self.imap = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER)
            self.imap.login(self.email_address, self.password)
            self.connected = True
            
            print(f"   ✓ Connection successful!")
            return True
            
        except imaplib.IMAP4.error as e:
            print(f"   ❌ Login failed: {e}")
            print(f"\n💡 Gmail Security Tips:")
            print(f"   1. You MUST use an App Password (not your regular password)")
            print(f"   2. Enable 2-Step Verification first")
            print(f"   3. Generate App Password at: https://myaccount.google.com/apppasswords")
            return False
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
            return False
    
    def fetch_emails(self, date_range: str = "latest7") -> List[Dict]:
        """
        Fetch emails based on date range
        
        Args:
            date_range: "latest7", "today", "yesterday", "7days", "15days"
        
        Returns:
            List of email dicts
        """
        
        if not self.connected:
            print(f"❌ Not connected to Gmail")
            return []
        
        print(f"\n📬 Fetching emails...")
        print(f"   Range: {date_range}")
        
        try:
            # Select inbox
            self.imap.select("INBOX")
            
            # Build search criteria
            search_criteria = self._build_search_criteria(date_range)
            print(f"   Search: {search_criteria}")
            
            # Search emails
            if date_range == "latest7":
                status, messages = self.imap.search(None, "ALL")
                email_ids = messages[0].split()
                
                if not email_ids or email_ids == [b'']:
                    print(f"   📭 No emails found")
                    return []
                
                # Get last 7
                recent_ids = email_ids[-7:] if len(email_ids) >= 7 else email_ids
                print(f"   ✓ Found {len(recent_ids)} emails")
                
            else:
                status, messages = self.imap.search(None, search_criteria)
                recent_ids = messages[0].split()
                
                if not recent_ids or recent_ids == [b'']:
                    print(f"   📭 No emails found in this range")
                    return []
                
                print(f"   ✓ Found {len(recent_ids)} emails")
            
            # Fetch email details
            emails = []
            for email_id in reversed(recent_ids):  # Most recent first
                email_data = self._fetch_email_details(email_id)
                if email_data:
                    emails.append(email_data)
            
            print(f"   ✓ Successfully fetched {len(emails)} emails")
            return emails
            
        except Exception as e:
            print(f"   ❌ Error fetching emails: {e}")
            return []
    
    def _build_search_criteria(self, date_range: str) -> str:
        """Build IMAP search criteria based on date range"""
        
        today = datetime.now()
        
        if date_range == "today":
            since_date = today.strftime("%d-%b-%Y")
            return f'(SINCE "{since_date}" UNSEEN)'
        
        elif date_range == "yesterday":
            yesterday = today - timedelta(days=1)
            since_date = yesterday.strftime("%d-%b-%Y")
            before_date = today.strftime("%d-%b-%Y")
            return f'(SINCE "{since_date}" BEFORE "{before_date}")'
        
        elif date_range == "7days":
            since_date = (today - timedelta(days=7)).strftime("%d-%b-%Y")
            return f'(SINCE "{since_date}")'
        
        elif date_range == "15days":
            since_date = (today - timedelta(days=15)).strftime("%d-%b-%Y")
            return f'(SINCE "{since_date}")'
        
        else:
            return "ALL"
    
    def _fetch_email_details(self, email_id) -> Optional[Dict]:
        """Fetch full email details"""
        
        try:
            status, msg_data = self.imap.fetch(email_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode headers
                    subject = self._decode_header(msg.get("Subject", ""))
                    sender = self._decode_header(msg.get("From", ""))
                    date = msg.get("Date", "")
                    
                    # Get body
                    body = self._extract_body(msg)
                    
                    return {
                        'msg_id': email_id.decode(),
                        'subject': subject,
                        'sender': sender,
                        'date': date,
                        'body': body
                    }
            
            return None
            
        except Exception as e:
            print(f"   ⚠️  Error fetching email {email_id}: {e}")
            return None
    
    def _decode_header(self, header: str) -> str:
        """Decode email header"""
        if not header:
            return ""
        
        decoded_parts = decode_header(header)
        decoded_str = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_str += part.decode(encoding or "utf-8", errors="ignore")
            else:
                decoded_str += str(part)
        
        return decoded_str
    
    def _extract_body(self, msg) -> str:
        """Extract email body text"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                
                if content_type == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        body = payload.decode(errors="ignore")
                        break
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")
            except:
                body = str(msg.get_payload())
        
        # Limit body length
        return body[:MAX_EMAIL_BODY_LENGTH]
    
    def star_email(self, msg_id: str) -> bool:
        """Star/flag an important email"""
        try:
            self.imap.store(msg_id, '+FLAGS', '\\Flagged')
            return True
        except Exception as e:
            print(f"   ❌ Failed to star email: {e}")
            return False
    
    def move_to_spam(self, msg_id: str) -> bool:
        """Move email to spam folder"""
        try:
            self.imap.store(msg_id, '+X-GM-LABELS', '\\Spam')
            return True
        except Exception as e:
            print(f"   ❌ Failed to move to spam: {e}")
            return False
    
    def archive_email(self, msg_id: str) -> bool:
        """Archive email (remove from inbox)"""
        try:
            self.imap.store(msg_id, '+X-GM-LABELS', '\\Archive')
            return True
        except Exception as e:
            print(f"   ❌ Failed to archive: {e}")
            return False
    
    def mark_as_read(self, msg_id: str) -> bool:
        """Mark email as read"""
        try:
            self.imap.store(msg_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            print(f"   ❌ Failed to mark as read: {e}")
            return False
    
    def disconnect(self):
        """Close Gmail connection"""
        if self.imap and self.connected:
            try:
                self.imap.close()
                self.imap.logout()
                print(f"\n👋 Disconnected from Gmail")
            except:
                pass
