#!/bin/bash

# Email Triage Assistant - Quick Start Script

echo "========================================="
echo "📧 Email Triage Assistant - Quick Start"
echo "========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "✅ Created .env file"
    echo ""
    echo "📝 Please edit .env and add your API keys:"
    echo "   1. SCALEDOWN_API_KEY (get from: https://blog.scaledown.ai/blog/getting-started)"
    echo "   2. GEMINI_API_KEY (get from: https://aistudio.google.com/app/apikey)"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check API keys
echo "🔑 Checking API keys..."
if [ -z "$SCALEDOWN_API_KEY" ] || [ "$SCALEDOWN_API_KEY" = "your_scaledown_api_key_here" ]; then
    echo "❌ SCALEDOWN_API_KEY not set in .env file"
    echo "   Get it from: https://blog.scaledown.ai/blog/getting-started"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ No LLM API key found in .env file"
    echo "   Get Gemini key from: https://aistudio.google.com/app/apikey"
    exit 1
fi

echo "✅ API keys configured"
echo ""

# Ask user which mode to run
echo "🚀 Choose how to run:"
echo "   1) Web UI (Streamlit) - Recommended"
echo "   2) CLI Demo"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🌐 Starting Web UI..."
        echo "   Opening browser at: http://localhost:8501"
        echo ""
        echo "💡 Tips:"
        echo "   - Click 'Load Sample Emails' in sidebar"
        echo "   - Click 'Initialize Agent' first"
        echo "   - Then 'Analyze All Emails'"
        echo ""
        streamlit run email_triage_ui.py
        ;;
    2)
        echo ""
        echo "🖥️  Running CLI Demo..."
        echo ""
        python email_triage_assistant.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
