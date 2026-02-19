# 📧 Email Triage Assistant

**AI-Powered Email Management System with ScaleDown Compression**

An intelligent email triage system that automatically categorizes emails, recommends actions, and generates draft responses while saving up to 80% on LLM token costs using ScaleDown compression.

---

## 🎯 Features

✅ **Automatic Email Categorization**
- 🚨 Urgent
- ⭐ Important  
- 📧 Normal
- 📋 Low Priority
- 📰 Newsletter
- 🗑️ Spam
- 🎁 Promotional

✅ **Smart Action Recommendations**
- Respond Now
- Respond Today
- Read Later
- Archive
- Delete
- Unsubscribe

✅ **AI Capabilities**
- Priority scoring (1-10)
- Sentiment analysis
- Automatic summaries
- Keyword extraction
- Draft response generation

✅ **Cost Optimization**
- ScaleDown compression (up to 80% token reduction)
- Significant cost savings on LLM API calls

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Email     │ --> │  ScaleDown   │ --> │     LLM     │ --> │ Categorized  │
│   Input     │     │ Compression  │     │  Analysis   │     │   + Draft    │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                           ⬇                                           ⬇
                    Saves 80% tokens!                         Ready to send!
```

**How it works:**

1. **Email Input**: Receive email content
2. **ScaleDown Compression**: Compress email context (save tokens!)
3. **LLM Analysis**: Categorize and analyze with AI
4. **Smart Output**: Get category, action, summary, and draft response

---

## 🚀 Quick Start

### 1️⃣ Get API Keys

**ScaleDown API Key** (Required)
- Visit: https://blog.scaledown.ai/blog/getting-started
- Contact sales team for API access

**LLM API Key** (Choose one)
- **Gemini** (Recommended - Free tier): https://aistudio.google.com/app/apikey
- **OpenAI** (Paid): https://platform.openai.com/api-keys

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables

Create a `.env` file:

```bash
SCALEDOWN_API_KEY=your_scaledown_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Or export directly:

```bash
export SCALEDOWN_API_KEY='your-scaledown-key'
export GEMINI_API_KEY='your-gemini-key'
```

### 4️⃣ Run the Application

**Option A: Web UI (Recommended)**

```bash
streamlit run email_triage_ui.py
```

Then open: http://localhost:8501

**Option B: Command Line Demo**

```bash
python email_triage_assistant.py
```

---

## 📖 Usage Guide

### Web UI

1. **Configure API Keys** (in sidebar)
   - Enter ScaleDown API key
   - Enter Gemini/OpenAI API key
   - Click "Initialize Agent"

2. **Load Emails**
   - Click "Load Sample Emails" for demo
   - Or manually add emails via "Add New Email" form

3. **Analyze Emails**
   - Click "Analyze All Emails"
   - Watch AI categorize and draft responses!

4. **Review Results**
   - See categorization and priority scores
   - Review AI-generated summaries
   - Edit and send draft responses

### Python API

```python
from email_triage_assistant import Email, EmailTriageAgent

# Initialize agent
agent = EmailTriageAgent(
    scaledown_key="your-key",
    llm_provider="gemini",
    llm_api_key="your-gemini-key"
)

# Create email
email = Email(
    id="1",
    subject="URGENT: Production Issue",
    sender="ops@company.com",
    body="Server is down, need immediate help!",
    received_date="2025-02-12 10:00:00"
)

# Analyze
analysis = agent.analyze_email(email, compress=True)

print(f"Category: {analysis.category.value}")
print(f"Action: {analysis.action.value}")
print(f"Priority: {analysis.priority_score}/10")
print(f"Summary: {analysis.summary}")
print(f"Draft: {analysis.draft_response}")
```

---

## 🔧 Configuration Options

### ScaleDown Compression

```python
# Auto compression (recommended)
agent.analyze_email(email, compress=True)

# Disable compression
agent.analyze_email(email, compress=False)
```

### LLM Provider

```python
# Use Gemini (free tier)
agent = EmailTriageAgent(
    scaledown_key="key",
    llm_provider="gemini",
    llm_api_key="gemini-key"
)

# Use OpenAI
agent = EmailTriageAgent(
    scaledown_key="key",
    llm_provider="openai",
    llm_api_key="openai-key"
)
```

---

## 📊 Example Output

**Input Email:**
```
From: ops-team@company.com
Subject: URGENT: Server Down
Body: Production server experiencing critical issues...
```

**AI Analysis:**
```
Category: 🚨 Urgent
Action: Respond Now
Priority: 9/10
Sentiment: negative

Summary: Production server outage requiring immediate attention 
affecting thousands of users.

Draft Response:
I've received your urgent message about the production server 
issues. I'm immediately looking into the 500 errors and will 
provide an update within the next 30 minutes...

Keywords: production, server, critical, users, errors

Compression Savings: 450 → 180 tokens (60% saved!)
```

---

## 🎓 Advanced Features

### Batch Processing

```python
# Analyze multiple emails
emails = [email1, email2, email3]
results = agent.batch_analyze(emails, compress=True)

for result in results:
    print(f"{result.category.value}: {result.summary}")
```

### Custom Filtering

```python
# Filter by priority
urgent = [r for r in results if r.priority_score >= 8]

# Filter by category
spam = [r for r in results if r.category == EmailCategory.SPAM]

# Filter by action
respond_now = [r for r in results if r.action == EmailAction.RESPOND_NOW]
```

### Integration with Gmail (Optional)

See `gmail_integration.py` (coming soon) for how to:
- Fetch emails from Gmail
- Apply labels automatically
- Send draft responses
- Archive/delete emails

---

## 💰 Cost Savings Example

**Without ScaleDown:**
- Email thread: 500 tokens
- Analysis prompt: 200 tokens
- Total per email: 700 tokens
- 100 emails/day: 70,000 tokens

**With ScaleDown (80% compression):**
- Email thread: 100 tokens (compressed!)
- Analysis prompt: 40 tokens (compressed!)
- Total per email: 140 tokens
- 100 emails/day: 14,000 tokens

**Savings: 56,000 tokens/day = 80% cost reduction!** 💰

---

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Streamlit
- **Compression**: ScaleDown API
- **LLM**: Google Gemini / OpenAI
- **Agent Framework**: Custom implementation

---

## 📝 Project Structure

```
email-triage-assistant/
├── email_triage_assistant.py  # Core agent logic
├── email_triage_ui.py          # Streamlit web UI
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── .env                        # API keys (create this)
```

---

## 🐛 Troubleshooting

**Error: "API key not found"**
- Make sure you've set environment variables
- Check `.env` file exists and is loaded
- Verify API keys are correct

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

**Compression not working:**
- Verify ScaleDown API key is valid
- Check API rate limits
- Test with smaller emails first

**LLM errors:**
- Check API key is correct
- Verify you have credits/quota
- Try switching providers (Gemini ↔ OpenAI)

---

## 🎯 Use Cases

- **Customer Support Teams**: Auto-prioritize support tickets
- **Sales Teams**: Identify hot leads faster
- **Executives**: Filter important communications
- **Product Teams**: Categorize user feedback
- **Anyone**: Manage email overload!

---

## 🔮 Future Enhancements

- [ ] Gmail API integration (auto-fetch emails)
- [ ] Outlook/Exchange support
- [ ] Email scheduling
- [ ] Team collaboration features
- [ ] Analytics dashboard
- [ ] Custom categorization rules
- [ ] Multi-language support
- [ ] Mobile app

---

## 📚 Resources

- **ScaleDown Docs**: https://docs.scaledown.ai
- **Gemini API**: https://ai.google.dev/docs
- **OpenAI API**: https://platform.openai.com/docs

---

## 🤝 Contributing

Built for the **ScaleDown AI Challenge** - Week 1

**Challenge Details:**
- Build an Agentic or RAG App
- Use ScaleDown for AI access
- Category: Intermediate
- Duration: 1 week

---

## 📄 License

MIT License - Feel free to use and modify!

---

## ✨ Credits

Built with ❤️ using:
- ScaleDown API (prompt compression)
- Google Gemini (LLM)
- Streamlit (web framework)

---

## 🎉 Demo

Try it now:
```bash
streamlit run email_triage_ui.py
```

**Sample emails included!** Just click "Load Sample Emails" to see it in action.

---

**Questions?** Check the About tab in the web UI or visit https://docs.scaledown.ai

**Ready to reduce email stress and save 80% on AI costs?** 🚀
