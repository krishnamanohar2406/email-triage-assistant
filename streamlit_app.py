"""
Streamlit Web UI for Intelligent Email Triage System
Beautiful, user-friendly interface for email management
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import check_api_keys, DATE_RANGES
from gmail_connector import GmailConnector
from email_analyzer import EmailAnalyzer, EmailAction, EmailCategory
from scaledown_service import ScaleDownService

# Page configuration
st.set_page_config(
    page_title="Email Triage System",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
# Custom CSS (Clean Classic Dark Theme)
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [class*="css"]  {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Background */
.stApp {
    background-color: #0f172a;
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ===== HEADINGS ===== */

h1 {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin-bottom: 0.3rem !important;
}

h2 {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}

h3 {
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    color: #f1f5f9 !important;
}

h4 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}

/* ===== CARDS ===== */

.stat-card {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 1rem;
    transition: 0.2s ease;
}

.stat-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 0 18px rgba(59,130,246,0.15);
}

/* ===== EMAIL RESULT CARDS ===== */

.email-card {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    transition: 0.2s ease;
}

.email-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 0 18px rgba(59,130,246,0.15);
}

/* Priority Styles */

.email-card.urgent {
    border-left: 5px solid #ef4444;
    background: rgba(239,68,68,0.08);
}

.email-card.important {
    border-left: 5px solid #f59e0b;
    background: rgba(245,158,11,0.08);
}

.email-card.spam {
    border-left: 5px solid #64748b;
    background: rgba(100,116,139,0.08);
}

/* ===== SUCCESS BOX ===== */

.success-box {
    background: #052e1f;
    border: 1px solid #065f46;
    padding: 20px;
    border-radius: 12px;
    margin-top: 1rem;
}

/* ===== BUTTONS ===== */

.stButton > button {
    background: #3b82f6;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #2563eb;
    box-shadow: 0 0 12px rgba(59,130,246,0.4);
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: #2563eb;
}

/* ===== METRICS ===== */

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* Divider */
hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)





# Initialize session state
if 'gmail_connected' not in st.session_state:
    st.session_state.gmail_connected = False
if 'gmail_client' not in st.session_state:
    st.session_state.gmail_client = None
if 'emails' not in st.session_state:
    st.session_state.emails = []
if 'analyses' not in st.session_state:
    st.session_state.analyses = []
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'actions_executed' not in st.session_state:
    st.session_state.actions_executed = False


def main_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1>📧 Intelligent Email Triage System</h1>
        <p style="font-size: 1.1rem; color: #666;">
            AI-powered email management with ScaleDown compression
        </p>
    </div>
    """, unsafe_allow_html=True)


def sidebar_config():
    """Configure sidebar"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Email+Triage", use_container_width=True)
        
        st.markdown("### ⚙️ Configuration")
        
        # Check API keys
        if check_api_keys():
            st.success("✅ API Keys Configured")
        else:
            st.error("❌ API Keys Missing")
            st.info("Please configure API keys in .env file")
            st.stop()
        
        st.markdown("---")
        
        # Gmail connection status
        st.markdown("### 🔌 Connection Status")
        if st.session_state.gmail_connected:
            st.success("✅ Connected to Gmail")
            if st.button("🔌 Disconnect"):
                if st.session_state.gmail_client:
                    st.session_state.gmail_client.disconnect()
                st.session_state.gmail_connected = False
                st.session_state.gmail_client = None
                st.session_state.emails = []
                st.session_state.analyses = []
                st.rerun()
        else:
            st.warning("⚠️ Not Connected")
        
        st.markdown("---")
        
        # Statistics
        if st.session_state.analyzer and st.session_state.analyses:
            st.markdown("### 📊 Session Stats")
            stats = st.session_state.analyzer.scaledown.get_statistics()
            st.metric("Emails Analyzed", len(st.session_state.analyses))
            st.metric("Tokens Saved", f"{stats['total_tokens_saved']:,}")
            st.metric("Avg Savings", f"{stats['average_savings']:.0f} tokens")
        
        st.markdown("---")
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Intelligent Email Triage System**
            
            Uses:
            - 🗜️ ScaleDown (80% compression)
            - 🤖 Gemini AI (deep analysis)
            - 📊 Smart categorization
            
            Built for ScaleDown AI Challenge
            """)


def login_page():
    """Gmail login page"""
    st.markdown("## 🔐 Gmail Login")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>📧 Connect Your Gmail</h3>
            <p>Securely analyze your inbox with AI-powered intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("gmail_login"):
            email = st.text_input("📧 Gmail Address", placeholder="you@gmail.com")
            password = st.text_input("🔑 App Password", type="password", 
                                     placeholder="xxxx xxxx xxxx xxxx")
            
            st.info("💡 You need a Gmail App Password, not your regular password")
            
            submitted = st.form_submit_button("🔌 Connect to Gmail", use_container_width=True)
            
            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    with st.spinner("Connecting to Gmail..."):
                        gmail = GmailConnector(email, password)
                        if gmail.connect():
                            st.session_state.gmail_connected = True
                            st.session_state.gmail_client = gmail
                            st.session_state.analyzer = EmailAnalyzer()
                            st.success("✅ Connected successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Connection failed. Check your credentials.")
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h4>🔒 Security Guide</h4>
            <ol>
                <li>Enable 2-Step Verification</li>
                <li>Visit <a href="https://myaccount.google.com/apppasswords" target="_blank">App Passwords</a></li>
                <li>Generate new password</li>
                <li>Use it here</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stat-card" style="margin-top: 1rem;">
            <h4>🎭 Try Demo</h4>
            <p>Don't want to login? Try the demo mode with sample emails</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎭 Run Demo Mode", use_container_width=True):
            st.session_state.demo_mode = True
            st.rerun()


def fetch_emails_page():
    st.markdown("## 📬 Fetch & Analyze Emails")
    st.markdown("Configure your analysis and let AI handle your inbox intelligently.")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>📅 Date Range</h3>
        </div>
        """, unsafe_allow_html=True)

        date_options = list(DATE_RANGES.values())
        date_keys = list(DATE_RANGES.keys())

        selected_label = st.selectbox(
            "Choose range:",
            date_options,
            index=0
        )

        selected_key = date_keys[date_options.index(selected_label)]

    with col2:
        st.markdown("""
        <div class="stat-card">
            <h3>🔍 Analysis Mode</h3>
        </div>
        """, unsafe_allow_html=True)

        auto_execute = st.checkbox("Auto-execute actions")
        if auto_execute:
            st.warning("Actions will directly modify your inbox.")
        else:
            st.info("Preview mode — no changes applied.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_center = st.columns([1,2,1])
    with col_center[1]:
        if st.button("📬 Fetch & Analyze Emails", use_container_width=True):
            fetch_and_analyze(selected_key, auto_execute)



def fetch_and_analyze(date_range: str, auto_execute: bool):
    """Fetch and analyze emails"""
    
    # Fetch emails
    with st.spinner(f"📬 Fetching emails ({DATE_RANGES[date_range]})..."):
        emails = st.session_state.gmail_client.fetch_emails(date_range)
        
        if not emails:
            st.warning("📭 No emails found in this range")
            return
        
        st.session_state.emails = emails
        st.success(f"✓ Found {len(emails)} emails")
    
    # Analyze emails
    st.markdown("---")
    st.markdown("### 🔍 AI Analysis in Progress")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    analyses = []
    
    for i, email_data in enumerate(emails):
        status_text.text(f"Analyzing email {i+1}/{len(emails)}: {email_data['subject'][:50]}...")
        progress_bar.progress((i + 1) / len(emails))
        
        with st.expander(f"📧 Email {i+1}: {email_data['subject']}", expanded=(i == 0)):
            # Show original content
            st.markdown("**📄 Original Email:**")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("From", "")
                st.markdown(f"_{email_data['sender']}_")
            with col2:
                st.markdown(f"**Subject:** {email_data['subject']}")
                with st.expander("View full body"):
                    st.text_area("Email Body", email_data['body'], height=150, disabled=True, 
                                label_visibility="collapsed", key=f"email_body_{i}")
            
            st.markdown("---")
            
            # Build context for compression
            email_context = f"""
EMAIL TO ANALYZE:
From: {email_data['sender']}
Subject: {email_data['subject']}
Body: {email_data['body'][:500]}
"""
            
            # Show compression in real-time
            st.markdown("**🗜️ ScaleDown Compression:**")
            
            # Create columns for before/after
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                original_length = len(email_context)
                st.metric("Original", f"{original_length} chars")
            
            # Do compression
            compression_result = st.session_state.analyzer.scaledown.compress_prompt(
                email_context, 
                st.session_state.analyzer._build_analysis_prompt()
            )
            
            compressed_text = compression_result['compressed_prompt']
            compressed_length = len(compressed_text)
            savings_pct = compression_result['savings_percent']
            
            with col2:
                st.metric("Compressed", f"{compressed_length} chars", 
                         delta=f"-{original_length - compressed_length}")
            
            with col3:
                st.metric("Savings", f"{savings_pct:.1f}%",
                         delta=f"{compression_result['original_tokens'] - compression_result['compressed_tokens']} tokens")
            
            # Show compressed content
            with st.expander("🔍 View Compressed Content"):
                st.markdown("**Compressed Email Context:**")
                st.text_area("", compressed_text, height=200, disabled=True, 
                            label_visibility="collapsed", key=f"compressed_text_{i}")
                st.caption(f"Token reduction: {compression_result['original_tokens']} → {compression_result['compressed_tokens']}")
            
            st.markdown("---")
            st.markdown("**🤖 AI Analysis:**")
            
            # Get AI analysis (using already compressed prompt)
            with st.spinner("Analyzing with Gemini AI..."):
                ai_response = st.session_state.analyzer.gemini.analyze_email(compressed_text)
                
                if ai_response:
                    result = st.session_state.analyzer._parse_ai_response(ai_response)
                else:
                    result = st.session_state.analyzer._fallback_analysis(email_data)
            
            analyses.append({
                'email': email_data,
                'analysis': result,
                'compression': compression_result
            })
            
            # Show analysis result
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Category:** {result.category.value}")
                st.markdown(f"**Summary:** {result.summary}")
                st.markdown(f"**Reasoning:** _{result.reasoning}_")
                if result.key_points:
                    st.markdown(f"**Key Points:** {', '.join(result.key_points)}")
            with col2:
                st.metric("Priority", f"{result.priority_score}/10")
                st.markdown(f"**Action:**")
                st.markdown(f"_{result.action.value}_")
    
    status_text.text("✅ Analysis complete!")
    st.session_state.analyses = analyses
    


def results_page():
    """Display analysis results"""
    st.markdown("## 📊 Analysis Results")
    
    if not st.session_state.analyses:
        st.info("No analysis results yet. Fetch emails first.")
        return
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    analyses = st.session_state.analyses
    
    urgent_count = sum(1 for a in analyses if a['analysis'].priority_score >= 8)
    spam_count = sum(1 for a in analyses if a['analysis'].action == EmailAction.MOVE_TO_SPAM)
    star_count = sum(1 for a in analyses if a['analysis'].action == EmailAction.STAR)
    archive_count = sum(1 for a in analyses if a['analysis'].action == EmailAction.ARCHIVE)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #ff4444;">🚨 {urgent_count}</h2>
            <p>Urgent Emails</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #ff9800;">⭐ {star_count}</h2>
            <p>To Star</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #000;">🗑️ {spam_count}</h2>
            <p>Spam Detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #2196F3;">📦 {archive_count}</h2>
            <p>To Archive</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        filter_category = st.multiselect(
            "Filter by Category",
            [cat.value for cat in EmailCategory],
            default=[]
        )
    
    with col2:
        filter_action = st.multiselect(
            "Filter by Action",
            [act.value for act in EmailAction],
            default=[]
        )
    
    # Display emails
    st.markdown("---")
    
    for i, result in enumerate(analyses):
        email_data = result['email']
        analysis = result['analysis']
        compression = result.get('compression', None)
        
        # Apply filters
        if filter_category and analysis.category.value not in filter_category:
            continue
        if filter_action and analysis.action.value not in filter_action:
            continue
        
        # Determine card class
        card_class = "email-card"
        if analysis.priority_score >= 8:
            card_class += " urgent"
        elif analysis.priority_score >= 6:
            card_class += " important"
        elif analysis.action == EmailAction.MOVE_TO_SPAM:
            card_class += " spam"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h4>{email_data['subject']}</h4>
            <p><strong>From:</strong> {email_data['sender']}</p>
            <p><strong>Category:</strong> {analysis.category.value} | 
               <strong>Priority:</strong> {analysis.priority_score}/10 | 
               <strong>Action:</strong> {analysis.action.value}</p>
            <p><strong>Summary:</strong> {analysis.summary}</p>
            <p style="color: #666;"><em>{analysis.reasoning}</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show compression stats if available
        if compression:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Original Tokens", compression['original_tokens'])
            with col2:
                st.metric("Compressed Tokens", compression['compressed_tokens'])
            with col3:
                st.metric("Tokens Saved", compression['original_tokens'] - compression['compressed_tokens'])
            with col4:
                st.metric("Savings", f"{compression['savings_percent']:.1f}%")
    
    # Action buttons
    st.markdown("---")
    
    if not st.session_state.actions_executed:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("✅ Execute All Actions", use_container_width=True, type="primary"):
                execute_actions()
    else:
        st.markdown("""
        <div class="success-box">
            <h3>✅ Actions Executed Successfully!</h3>
            <p>All approved actions have been applied to your Gmail inbox.</p>
        </div>
        """, unsafe_allow_html=True)


def execute_actions():
    """Execute approved actions"""
    with st.spinner("🔄 Executing actions..."):
        for result in st.session_state.analyses:
            email_data = result['email']
            analysis = result['analysis']
            action = analysis.action
            msg_id = email_data['msg_id']
            
            if action == EmailAction.STAR:
                st.session_state.gmail_client.star_email(msg_id)
            elif action == EmailAction.MOVE_TO_SPAM:
                st.session_state.gmail_client.move_to_spam(msg_id)
            elif action == EmailAction.ARCHIVE:
                st.session_state.gmail_client.archive_email(msg_id)
            elif action == EmailAction.MARK_READ:
                st.session_state.gmail_client.mark_as_read(msg_id)
        
        st.session_state.actions_executed = True
        st.success("✅ All actions completed!")
        st.rerun()


def demo_mode():
    """Demo mode with sample emails"""
    st.markdown("## 🎭 Demo Mode")
    
    st.info("👋 This is demo mode with sample emails. No Gmail connection required!")
    
    # Sample emails
    sample_emails = [
        {
            'msg_id': '1',
            'sender': 'ops@company.com',
            'subject': 'URGENT: Production Server Down',
            'date': 'Today',
            'body': 'Critical production issue affecting all users...'
        },
        {
            'msg_id': '2',
            'sender': 'newsletter@tech.com',
            'subject': 'Weekly Tech Digest',
            'date': 'Today',
            'body': 'Here are this week\'s top stories...'
        },
        {
            'msg_id': '3',
            'sender': 'spam@deals.com',
            'subject': '🎉 WIN $10,000 NOW!!!',
            'date': 'Today',
            'body': 'Click here immediately! Limited time!!!'
        }
    ]
    
    st.session_state.emails = sample_emails
    
    # Analyze
    if st.button("🔍 Analyze Sample Emails"):
        with st.spinner("Analyzing..."):
            st.session_state.analyzer = EmailAnalyzer()
            analyses = []
            
            for email_data in sample_emails:
                result = st.session_state.analyzer.analyze(email_data)
                analyses.append({
                    'email': email_data,
                    'analysis': result
                })
            
            st.session_state.analyses = analyses
            st.success("✅ Analysis complete!")
            st.rerun()


def main():
    """Main application"""
    main_header()
    sidebar_config()
    
    # Check for demo mode
    if 'demo_mode' in st.session_state and st.session_state.demo_mode:
        demo_mode()
        if st.session_state.analyses:
            results_page()
        return
    
    # Main flow
    if not st.session_state.gmail_connected:
        login_page()
    else:
        # Tabs
        fetch_emails_page()

        # Show results directly below fetch section
        if st.session_state.analyses:
            st.markdown("---")
            results_page()


if __name__ == "__main__":
    main()