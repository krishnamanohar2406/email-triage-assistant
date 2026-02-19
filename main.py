"""
Email Triage System - Main Application
Intelligent email management with AI-powered analysis and actions
"""

import sys
from typing import List, Dict

from config import check_api_keys, DATE_RANGES
from gmail_connector import GmailConnector
from email_analyzer import EmailAnalyzer, EmailAction
from scaledown_service import ScaleDownService


def print_header():
    """Print application header"""
    print("=" * 70)
    print("📧 INTELLIGENT EMAIL TRIAGE SYSTEM")
    print("=" * 70)
    print("AI-powered email analysis with ScaleDown compression")
    print("Automatically categorize, prioritize, and organize your inbox")
    print("=" * 70)


def get_login_choice() -> str:
    """Get user's login choice"""
    print("\n🔐 Choose Mode:")
    print("1. Login with Gmail (analyze your real inbox)")
    print("2. See Demo (sample emails)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    return choice


def demo_mode():
    """Run demo mode with sample emails"""
    print("\n" + "=" * 70)
    print("🎭 DEMO MODE - See How The System Works")
    print("=" * 70)
    
    # Sample emails
    sample_emails = [
        {
            'msg_id': '1',
            'sender': 'ops-team@company.com',
            'subject': 'URGENT: Production Server Down - Critical',
            'date': 'Today 09:30 AM',
            'body': '''Our main production server (prod-db-01) has gone offline at 09:15 AM. 
            All services are affected and customers are reporting errors. 
            This is a P0 incident affecting thousands of users.
            Need immediate assistance from the DevOps team to diagnose and resolve.
            Current impact: 100% service outage.'''
        },
        {
            'msg_id': '2',
            'sender': 'newsletter@techinsights.com',
            'subject': 'Weekly Tech Digest - AI Trends & Updates',
            'date': 'Today 08:00 AM',
            'body': '''Here are this week's top technology stories:
            - New AI models released by major tech companies
            - Cloud computing cost optimization strategies
            - Cybersecurity best practices for 2025
            Click here to read the full newsletter.
            Unsubscribe | Manage Preferences'''
        },
        {
            'msg_id': '3',
            'sender': 'deals@megastore.com',
            'subject': '🎉 MEGA SALE! 90% OFF - Click NOW!!!',
            'date': 'Today 07:45 AM',
            'body': '''🔥🔥🔥 DON'T MISS OUT!!! 🔥🔥🔥
            BIGGEST SALE OF THE YEAR!!!!
            90% OFF EVERYTHING!!
            WIN $10,000 PRIZE!!!
            CLICK HERE NOW BEFORE IT'S GONE!!!
            Limited time offer! Act fast! Buy now!'''
        }
    ]
    
    # Analyze each sample
    analyzer = EmailAnalyzer()
    
    for i, email_data in enumerate(sample_emails, 1):
        result = analyzer.analyze(email_data)
        print_analysis_summary(i, len(sample_emails), email_data, result)
    
    print("\n" + "=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)
    print("\n💡 To use with your real inbox, choose option 1 and login with Gmail")


def gmail_mode():
    """Run with real Gmail login"""
    print("\n" + "=" * 70)
    print("📧 GMAIL LOGIN")
    print("=" * 70)
    
    print("\n⚠️  Important: Gmail Security")
    print("   You need an 'App Password' (not your regular password)")
    print("   Steps:")
    print("   1. Enable 2-Step Verification")
    print("   2. Go to: https://myaccount.google.com/apppasswords")
    print("   3. Generate App Password")
    print("   4. Use that password here\n")
    
    email_address = input("Gmail address: ").strip()
    password = input("App Password: ").strip()
    
    if not email_address or not password:
        print("\n❌ Email and password required!")
        return
    
    # Connect to Gmail
    gmail = GmailConnector(email_address, password)
    
    if not gmail.connect():
        return
    
    # Select date range
    date_range = select_date_range()
    
    # Fetch emails
    emails = gmail.fetch_emails(date_range)
    
    if not emails:
        gmail.disconnect()
        return
    
    # Analyze emails
    print("\n" + "=" * 70)
    print("🔍 AI ANALYSIS IN PROGRESS")
    print("=" * 70)
    
    analyzer = EmailAnalyzer()
    analysis_results = []
    
    for i, email_data in enumerate(emails, 1):
        result = analyzer.analyze(email_data)
        analysis_results.append({
            'email': email_data,
            'analysis': result
        })
        print_analysis_summary(i, len(emails), email_data, result)
    
    # Show summary and get confirmation
    show_action_summary(analysis_results)
    
    # Ask for confirmation
    if confirm_actions():
        execute_actions(gmail, analysis_results)
    else:
        print("\n❌ Actions cancelled. No changes made to your mailbox.")
    
    # Show statistics
    show_session_statistics(analyzer.scaledown)
    
    # Disconnect
    gmail.disconnect()


def select_date_range() -> str:
    """Let user select email date range"""
    print("\n📅 Select Email Range:")
    options = list(DATE_RANGES.items())
    
    for i, (key, label) in enumerate(options, 1):
        print(f"{i}. {label}")
    
    choice = input(f"\nEnter choice (1-{len(options)}): ").strip()
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(options):
            selected = options[index][0]
            print(f"✓ Selected: {DATE_RANGES[selected]}")
            return selected
    except:
        pass
    
    # Default
    print(f"✓ Using default: {DATE_RANGES['latest7']}")
    return "latest7"


def print_analysis_summary(current: int, total: int, email_data: Dict, analysis):
    """Print summary of email analysis"""
    print(f"\n{'─'*70}")
    print(f"📧 Email {current}/{total}")
    print(f"From: {email_data['sender']}")
    print(f"Subject: {email_data['subject']}")
    print(f"\n📊 AI Analysis:")
    print(f"   Category: {analysis.category.value}")
    print(f"   Priority: {analysis.priority_score}/10")
    print(f"   Action: {analysis.action.value}")
    print(f"   Summary: {analysis.summary}")
    print(f"   Reasoning: {analysis.reasoning}")
    if analysis.key_points:
        print(f"   Key Points: {', '.join(analysis.key_points)}")


def show_action_summary(results: List[Dict]):
    """Show summary of all actions to be performed"""
    print("\n" + "=" * 70)
    print("📋 ACTION SUMMARY")
    print("=" * 70)
    
    # Count actions
    action_counts = {}
    for result in results:
        action = result['analysis'].action
        action_counts[action] = action_counts.get(action, 0) + 1
    
    print("\nActions to perform:")
    for action, count in action_counts.items():
        icon = {
            EmailAction.STAR: "⭐",
            EmailAction.MOVE_TO_SPAM: "🗑️",
            EmailAction.ARCHIVE: "📦",
            EmailAction.MARK_READ: "📖",
            EmailAction.NOTHING: "➖"
        }.get(action, "")
        
        print(f"  {icon} {action.value}: {count} email(s)")
    
    # List emails by action
    for action in EmailAction:
        emails_with_action = [r for r in results if r['analysis'].action == action]
        
        if emails_with_action and action != EmailAction.NOTHING:
            print(f"\n{action.value}:")
            for r in emails_with_action:
                print(f"  • {r['email']['subject'][:60]}")


def confirm_actions() -> bool:
    """Ask user to confirm actions"""
    print("\n" + "=" * 70)
    print("⚠️  CONFIRMATION REQUIRED")
    print("=" * 70)
    print("\nThese actions will be applied to your Gmail inbox.")
    print("Review the actions above carefully.")
    
    response = input("\n✅ Type 'OK' to proceed with these actions: ").strip()
    
    return response.upper() == "OK"


def execute_actions(gmail: GmailConnector, results: List[Dict]):
    """Execute approved actions on emails"""
    print("\n" + "=" * 70)
    print("🔄 EXECUTING ACTIONS")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        email_data = result['email']
        analysis = result['analysis']
        action = analysis.action
        msg_id = email_data['msg_id']
        
        print(f"\n[{i}/{len(results)}] {email_data['subject'][:50]}...")
        print(f"   Action: {action.value}")
        
        if action == EmailAction.STAR:
            if gmail.star_email(msg_id):
                print(f"   ✓ Starred")
        
        elif action == EmailAction.MOVE_TO_SPAM:
            if gmail.move_to_spam(msg_id):
                print(f"   ✓ Moved to spam")
        
        elif action == EmailAction.ARCHIVE:
            if gmail.archive_email(msg_id):
                print(f"   ✓ Archived")
        
        elif action == EmailAction.MARK_READ:
            if gmail.mark_as_read(msg_id):
                print(f"   ✓ Marked as read")
        
        else:
            print(f"   ➖ No action taken")
    
    print("\n" + "=" * 70)
    print("✅ ALL ACTIONS COMPLETED!")
    print("=" * 70)


def show_session_statistics(scaledown: ScaleDownService):
    """Show compression statistics"""
    stats = scaledown.get_statistics()
    
    print("\n" + "=" * 70)
    print("📊 SESSION STATISTICS")
    print("=" * 70)
    print(f"\nScaleDown Compression:")
    print(f"  Total compressions: {stats['total_compressions']}")
    print(f"  Total tokens saved: {stats['total_tokens_saved']}")
    print(f"  Average savings: {stats['average_savings']:.0f} tokens per email")
    print(f"\n💰 Cost Savings: ~{stats['total_tokens_saved'] * 0.0000005:.4f} USD")
    print(f"   (Based on typical LLM pricing)")


def main():
    """Main application entry point"""
    
    # Print header
    print_header()
    
    # Check API keys
    if not check_api_keys():
        print("\n❌ API keys not configured!")
        print("\nPlease create a .env file with:")
        print("  SCALEDOWN_API_KEY=your_key")
        print("  GEMINI_API_KEY=your_key")
        return 1
    
    print("\n✓ API keys configured")
    
    # Get user choice
    choice = get_login_choice()
    
    if choice == "2":
        demo_mode()
    elif choice == "1":
        gmail_mode()
    else:
        print("\n❌ Invalid choice")
        return 1
    
    print("\n" + "=" * 70)
    print("👋 Thank you for using Email Triage System!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
