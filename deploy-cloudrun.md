# Google Cloud Run Deployment Guide

## 🏃‍♂️ Deploy to Google Cloud Run

### Prerequisites
- Google Cloud account with billing enabled
- gcloud CLI installed
- Docker installed locally

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Step 2: Deploy Commands

```bash
# Build and deploy to Cloud Run
gcloud run deploy vision-ai-box-counting \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key_here \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

### Step 3: Set Environment Variables

```bash
gcloud run services update vision-ai-box-counting \
  --set-env-vars OPENAI_API_KEY=your_openai_key,LOG_LEVEL=INFO \
  --region us-central1
```

### Benefits of Cloud Run
- Pay only when processing requests
- Automatic scaling (including to zero)
- Handles high traffic spikes
- Integrated with Google Cloud services
- Professional monitoring and logging