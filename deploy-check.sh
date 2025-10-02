#!/bin/bash
# Simple deployment preparation script

echo "🚀 Preparing Vision AI Box Counting API for deployment..."

# Check if required files exist
echo "📋 Checking required files..."

required_files=("main.py" "requirements.txt" "prompt.txt" ".env.example")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing!"
        exit 1
    fi
done

# Validate requirements.txt
echo "📦 Validating requirements.txt..."
if grep -q "fastapi" requirements.txt && grep -q "openai" requirements.txt; then
    echo "✅ Key dependencies found"
else
    echo "❌ Missing key dependencies in requirements.txt"
    exit 1
fi

# Check if .env file exists (for local testing)
if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "✅ OpenAI API key configured"
    else
        echo "⚠️  OpenAI API key may not be set in .env"
    fi
else
    echo "⚠️  No .env file found (needed for local testing)"
fi

echo ""
echo "🎯 Deployment Options:"
echo "1. Railway (Recommended): Push to GitHub, then deploy via railway.app"
echo "2. Google Cloud Run: Use 'gcloud run deploy' with the provided Dockerfile"
echo "3. Docker: Use 'docker build -t vision-ai . && docker run -p 8080:8080 vision-ai'"
echo ""
echo "📚 See deploy-railway.md or deploy-cloudrun.md for detailed instructions"
echo ""
echo "✨ Ready for deployment!"