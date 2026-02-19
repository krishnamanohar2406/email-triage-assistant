# 📧 Intelligent Email Triage System

**Your AI-powered inbox assistant that actually understands your emails**

Ever feel overwhelmed by hundreds of emails? Wish someone could just read them all, figure out what's important, and organize everything for you? Well, that's exactly what this does — except it's not "someone," it's AI powered by ScaleDown compression and Google's Gemini.

---

## 🎯 What Does This Actually Do?

Imagine waking up to 50 new emails. Instead of spending an hour reading through newsletters, spam, and trying to find that ONE urgent message from your boss... you just:

1. **Login** → Connect your Gmail
2. **Click "Analyze"** → AI reads every email  
3. **Review** → See what's urgent, what's spam, what can wait
4. **Confirm** → Type "OK" and watch magic happen
   - ⭐ Important emails get starred
   - 🗑️ Spam gets deleted
   - 📦 Newsletters get archived
   - ✅ Everything organized!

**All this while saving 80% on AI costs** thanks to ScaleDown compression.

---

## 🚀 Why This is Actually Cool

### **It Really Reads Your Emails**
Not just looking for keywords like "urgent" or "meeting." It actually understands:
- *"Hey, can we reschedule tomorrow's call?"* → Important, needs response
- *"🎉 YOU WON $1,000,000!!!"* → Obvious spam
- *"Weekly newsletter from TechCrunch"* → Newsletter, can archive

### **It Shows Its Work**
Unlike black-box AI, you see exactly:
- What the email was (original content)
- How it got compressed (80% smaller!)
- Why the AI categorized it that way
- What action it recommends

### **You're In Control**
Nothing happens until YOU say "OK." Review everything first, then execute.

### **Works Both Ways**
- **Web UI** → Beautiful dashboard in your browser
- **Command Line** → For the terminal warriors

---

## 📁 Project Structure

Here's what's inside (and what each file does):

```
email-triage-system/
│
├── 🎨 streamlit_app.py          # Beautiful web interface
├── 💻 main.py                   # Command-line version
│
├── 🧠 email_analyzer.py         # The brain - understands emails
├── 🗜️ scaledown_service.py     # Compresses prompts (saves 80% tokens)
├── 🤖 gemini_service.py         # Talks to Google's AI
├── 📧 gmail_connector.py        # Connects to your Gmail
│
├── ⚙️ config.py                 # Settings and API keys
├── 📋 requirements.txt          # What to install
├── 📖 README.md                 # You are here!
└── 🔐 .env                      # Your API keys (you create this)
```

### **Quick Explanation:**

**User Interfaces** (pick one):
- `streamlit_app.py` - Web UI with pretty graphs and cards
- `main.py` - Terminal UI for those who like typing

**The Magic Trio** (where AI happens):
- `email_analyzer.py` - Coordinates everything, makes decisions
- `scaledown_service.py` - Shrinks prompts from 500 tokens → 100 tokens
- `gemini_service.py` - Sends compressed prompts to AI

**Utilities:**
- `gmail_connector.py` - Fetches emails, stars them, moves spam
- `config.py` - Stores settings (API keys, model names, etc.)

---

## 🛠️ Setup (Don't Worry, It's Easy!)

### **Step 1: Get the Code**
```bash
git clone <your-repo>
cd email-triage-system
```

### **Step 2: Install Stuff**
```bash
pip install -r requirements.txt
```
That's it! Just `requests`, `python-dotenv`, and `streamlit`. No heavy ML libraries.

### **Step 3: Get API Keys**

#### **ScaleDown API (for compression)**
1. Visit: https://blog.scaledown.ai/blog/getting-started
2. Sign up / contact for API access
3. Copy your key (starts with `sk_`)

#### **Gemini API (for AI - it's FREE!)**
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key (starts with `AIza`)

No credit card needed! Gemini gives you:
- 15 requests/minute
- 1,500 requests/day
- 1 million tokens/day

**That's enough for ~5,000 emails per day!**

### **Step 4: Create `.env` File**
In your project folder, create a file named `.env`:

```env
SCALEDOWN_API_KEY=sk_your_scaledown_key_here
GEMINI_API_KEY=AIzaSy_your_gemini_key_here
```

### **Step 5: Get Gmail App Password**

**You CANNOT use your regular Gmail password!** Google blocks that for security.

Here's how to get an App Password:
1. Go to: https://myaccount.google.com/apppasswords
2. You'll need **2-Step Verification enabled** first
3. Click "Generate"
4. Choose "Mail" → "Other device" → Name it "Email Triage"
5. Copy the 16-character password
6. Use THIS password when logging in

---

## 🎮 How to Use

### **Option 1: Web Interface (Pretty!)**

```bash
streamlit run streamlit_app.py
```

Opens in browser at `http://localhost:8501`

**What You'll See:**
1. **Login page** → Enter Gmail + App Password
2. **Dashboard** → Select date range, click "Fetch & Analyze"
3. **Watch magic** → See compression happening in real-time
4. **Results page** → Review all analyses with pretty cards
5. **Execute** → Click button, type "OK", done!

### **Option 2: Command Line (Classic!)**

```bash
python main.py
```

**Menu appears:**
```
📧 INTELLIGENT EMAIL TRIAGE SYSTEM
═══════════════════════════════════════

Choose Mode:
1. Login with Gmail
2. Demo Mode

Enter choice: 1
```

Follow the prompts, same result!

---

## 🧪 Try Demo Mode First!

Not ready to connect your real email? Try demo mode:

**Web UI:**
- Click "🎭 Run Demo Mode" button

**Command Line:**
- Choose option 2 when prompted

You'll see 3 sample emails analyzed:
- 🚨 Urgent production server issue
- 📰 Tech newsletter
- 🗑️ Obvious spam

Perfect for seeing how it works without any risk!

---

## 💡 How It Actually Works (The Flow)

Let me walk you through what happens when you analyze an email:

### **1. Fetch Email from Gmail**
```
📧 Email arrives:
From: boss@company.com
Subject: URGENT: Q4 Report Due Tomorrow
Body: Hey, we need that report by EOD tomorrow...
```

### **2. Build Context**
```
Original prompt: 523 characters
"EMAIL TO ANALYZE:
From: boss@company.com
Subject: URGENT: Q4 Report Due Tomorrow  
Body: Hey, we need that report by EOD tomorrow for the board meeting..."
```

### **3. ScaleDown Compression** 🗜️
```
🗜️ ScaleDown working...
   Original: 520 tokens
   Compressed: 43 tokens
   ✓ Saved: 477 tokens (92%)

Compressed version:
"boss@company.com: urgent Q4 rpt EOD tmrw board mtg..."
```

**This is the magic!** ScaleDown shrinks the prompt while keeping the meaning.

### **4. Send to Gemini AI** 🤖
```
🤖 Gemini analyzing compressed prompt...
   Model: gemini-1.5-flash
   ✓ Analysis received
```

Gemini reads the compressed version and understands:
- This is from your boss
- It's urgent (due tomorrow)
- It's about a report
- Board meeting is involved

### **5. AI Response** (JSON format)
```json
{
  "category": "URGENT",
  "action": "STAR",
  "priority_score": 9,
  "summary": "Boss needs Q4 report by tomorrow for board meeting",
  "reasoning": "Urgent deadline, from supervisor, high-stakes meeting",
  "key_points": ["Q4 report", "Due tomorrow", "Board meeting"],
  "sentiment": "urgent",
  "requires_response": true
}
```

### **6. Show Results**
```
📊 Analysis Result:
   Category: 🚨 Urgent
   Priority: 9/10
   Action: Star (Important)
   
   Summary: Boss needs Q4 report by tomorrow
   Reasoning: Urgent deadline from supervisor
   
   💾 Compression Stats:
   Original: 520 tokens → Compressed: 43 tokens
   Savings: 92% (477 tokens saved)
```

### **7. You Decide**
```
⚠️ CONFIRMATION REQUIRED

Actions to perform:
  ⭐ Star: 1 email
  
Type 'OK' to proceed: OK
```

### **8. Execute**
```
🔄 Executing...
   [1/1] URGENT: Q4 Report Due Tomorrow
   ✓ Starred

✅ Complete!
```

**Your email is now starred in Gmail!**

---

## 📊 Real Example: Processing 7 Emails

Here's what happened in a real test:

```
📧 7 Emails Analyzed:

1. "Immediate Payment Required"        → 📧 Normal (5/10)
2. "Congratulations!!! You Won ₹25L"   → 🗑️ SPAM (1/10) 
3. "URGENT: Account Suspension"        → 🗑️ SPAM (1/10)
4. "Guaranteed 300% Return in 7 Days" → 📧 Normal (5/10)
5. "hiiii"                             → 📧 Normal (5/10)
6. "Critical: Payment Transactions"    → 🚨 URGENT (9/10)
7. "URGENT: Production Server Down"    → 🚨 URGENT (9/10)

Actions Taken:
  ⭐ Starred: 2 emails (#6, #7)
  🗑️ Spam: 2 emails (#2, #3)
  ➖ No action: 3 emails (#1, #4, #5)

Compression Stats:
  Total tokens saved: 3,151
  Average savings per email: 450 tokens (85%)
  Cost saved: ~$0.0016 USD
```

**What This Means:**
- Without ScaleDown: Would use ~3,640 tokens
- With ScaleDown: Used only ~489 tokens
- **Saved 87% on AI costs!**

---

## 🎨 Features You'll Love

### **In the Web UI:**

#### **Real-Time Compression Visualization**
See ScaleDown work its magic:
```
🗜️ Compression:
┌──────────┬────────────┬──────────┐
│ Original │ Compressed │ Savings  │
│ 523 chr  │ 105 chr    │ 80%      │
│ 520 tkn  │  43 tkn    │ 477 tkn  │
└──────────┴────────────┴──────────┘

[🔍 View Compressed Content]
```

#### **Color-Coded Email Cards**
- 🔴 **Red border** = Urgent (drop everything!)
- 🟠 **Orange border** = Important (handle today)
- ⚫ **Black border** = Spam (bye bye!)
- 🔵 **Blue border** = Normal (can wait)

#### **Smart Filters**
Filter by:
- Category (Urgent, Important, Spam, etc.)
- Action (Star, Archive, Spam)
- Priority level

#### **Session Statistics**
```
📊 Session Stats:
├─ 7 emails analyzed
├─ 3,151 tokens saved
└─ ~$0.0016 USD saved
```

### **Date Range Options:**

Perfect for different situations:

1. **Latest 7 emails** → Quick check, just see what's on top
2. **Today** → New unread emails since midnight
3. **Yesterday** → Catch up on what you missed
4. **Last 7 days** → Weekly cleanup
5. **Last 15 days** → Deep inbox cleaning (max limit)

---

## 🔒 Security & Privacy

**Your Data:**
- ✅ All processing happens in real-time
- ✅ Nothing is stored on any server
- ✅ Emails go: Gmail → ScaleDown → Gemini → Deleted
- ✅ API keys stay in your `.env` file (never uploaded)

**Gmail Access:**
- Uses App Passwords (not your real password)
- Read-only access to emails
- Can't send emails or access other Google services
- Revoke access anytime at https://myaccount.google.com/apppasswords

**API Keys:**
- ScaleDown API: Industry-standard encryption
- Gemini API: Google's enterprise security
- Both are in your local `.env` file only

---

## 💰 Cost Analysis

**Let's do the math** for a typical user:

### **Small Team (100 emails/day)**

**Without ScaleDown:**
- 100 emails × 500 tokens = 50,000 tokens/day
- × 30 days = 1,500,000 tokens/month
- Cost (at $0.50/1M tokens): **$0.75/month**

**With ScaleDown (80% compression):**
- 100 emails × 100 tokens = 10,000 tokens/day
- × 30 days = 300,000 tokens/month
- Cost: **$0.15/month**

**💰 Savings: $0.60/month or $7.20/year**

### **Medium Company (1,000 emails/day)**

**Without ScaleDown:** $7.50/month = **$90/year**
**With ScaleDown:** $1.50/month = **$18/year**

**💰 Savings: $72/year**

### **Enterprise (10,000 emails/day)**

**Without ScaleDown:** $75/month = **$900/year**
**With ScaleDown:** $15/month = **$180/year**

**💰 Savings: $720/year**

**Plus:**
- ⏰ Time saved: ~2 hours/day not reading spam
- 🧠 Mental clarity: Inbox anxiety = gone
- ✅ Never miss urgent emails again

---

## 🐛 Troubleshooting

### **"API keys not configured"**

**Problem:** `.env` file missing or wrong format

**Solution:**
```bash
# Make sure .env exists in project root
ls -la .env

# Check format (no quotes, no spaces):
SCALEDOWN_API_KEY=sk_abc123
GEMINI_API_KEY=AIzaSy_xyz789
```

### **"Login failed" or "Invalid credentials"**

**Problem:** Using regular Gmail password instead of App Password

**Solution:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate new App Password
3. Use that 16-character password
4. NOT your regular Gmail password!

### **"All models failed" or "Model not found"**

**Problem:** Gemini API key invalid or not activated

**Solution:**
1. Get fresh API key from https://aistudio.google.com/app/apikey
2. Make sure you copied the FULL key
3. Update `.env` file
4. Restart the app

### **"No emails found"**

**Possible reasons:**
- Selected date range has no emails
- All emails already read (if using "Today" option)
- IMAP not enabled for Gmail

**Solution:**
- Try "Latest 7 emails" option
- Check Gmail web to verify emails exist
- Enable IMAP: Settings → Forwarding and POP/IMAP → Enable IMAP

### **Streamlit "Duplicate Element ID"**

**Problem:** Old version of streamlit_app.py

**Solution:** Download the latest version with unique keys added

---

## 🎉 You Made It!

If you read this whole README, you deserve a medal 🏅

Now go organize that inbox! Your future self will thank you.

**Quick start reminder:**
```bash
# Install
pip install -r requirements.txt

# Setup .env
echo "SCALEDOWN_API_KEY=your_key" > .env
echo "GEMINI_API_KEY=your_key" >> .env

# Run
streamlit run streamlit_app.py

# Or
python main.py
```

**Happy triaging! 📧✨**
