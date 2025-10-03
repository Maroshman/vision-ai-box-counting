# Railway Deployment Guide for Vision AI Box Counting API

## 🚄 Deploy to Railway (Recommended)

### Prerequisites
- GitHub account
- Railway account (free at railway.app)
- Your code in a GitHub repository

### Step 1: Prepare Your Project

1. **Create railway.json** (deployment config)
2. **Update requirements.txt** (ensure all dependencies are listed)
3. **Create Procfile** (tells Railway how to run your app)
4. **Set environment variables**

### Step 2: Deploy

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway auto-detects Python and installs dependencies
6. Set environment variables in Railway dashboard
7. Your API will be live at `https://your-app-name.railway.app`

### Step 3: Set Environment Variables in Railway

**Required Variables:**
```
OPENAI_API_KEY=your_openai_api_key_here
API_KEY=your_secure_api_key_here
```

**Optional Variables:**
```
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=20
```

**How to set variables:**
1. In Railway dashboard, click your service
2. Go to "Variables" tab
3. Click "New Variable" for each one
4. Add the variable name and value
5. Railway will automatically redeploy

**Generate secure API key:**
```bash
openssl rand -hex 32
```

### Step 4: Test Your Deployment

```bash
# Test health endpoint (no auth required)
curl https://your-app-name.railway.app/health

# Test authenticated endpoint
curl -X POST "https://your-app-name.railway.app/count-boxes" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@your_image.jpg"
```

## 🐳 Alternative: Google Cloud Run

If you prefer Google Cloud, see `deploy-cloudrun.md`

## 📝 Notes

- Railway automatically handles HTTPS/SSL
- Auto-scaling based on traffic
- Logs available in Railway dashboard
- Custom domains supported
- Persistent storage available if needed