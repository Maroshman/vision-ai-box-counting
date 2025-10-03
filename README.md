# 🤖 Vision AI Box Counting API

AI-powered box counting and label extraction from images using OpenAI's GPT-4o Vision API.

## ✨ Features

- 📦 **Accurate box counting** using advanced computer vision
- 🏷️ **Label extraction** from shipping labels, barcodes, and text
- 📊 **Confidence scoring** for reliability assessment
- 🔄 **Multiple image formats** (JPEG, PNG, WebP, GIF)
- 🛠️ **Easy prompt customization** via external `prompt.txt`
- 🌐 **RESTful API** with interactive documentation
- 🚀 **Cloud-ready** deployment configurations

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/vision-ai-box-counting.git
   cd vision-ai-box-counting
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API keys (required)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key and secure API key for authentication
   # Generate API key with: openssl rand -hex 32
   ```

4. **Run the API**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Test the API**
   - Open http://127.0.0.1:8000/docs for interactive documentation
   - Or use: `python debug_upload.py your_image.jpg`

## 🌐 Deployment

### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repository
2. Connect to [Railway](https://railway.app)
3. Set `OPENAI_API_KEY` environment variable
4. Deploy automatically!

### Google Cloud Run
```bash
gcloud run deploy --source . --platform managed
```

See `deploy-railway.md` or `deploy-cloudrun.md` for detailed instructions.

## 📖 API Usage

### Authentication

The API requires authentication using API keys for all endpoints except `/health`. You must set an `API_KEY` in your environment variables.

**Required Authentication:**
```bash
curl -X POST "https://your-api-url.com/count-boxes" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@boxes.jpg"
```

### Upload Image for Analysis
```bash
curl -X POST "https://your-api-url.com/count-boxes" \
  -F "file=@boxes.jpg"
```

### Example Response
```json
{
  "filename": "boxes.jpg",
  "analysis": {
    "total_count": 12,
    "box_details": [
      {
        "box_id": 1,
        "type": "shipping_box",
        "labels": ["FRAGILE", "Amazon"],
        "confidence": 0.9,
        "position": "top_left"
      }
    ],
    "summary": {
      "total_boxes": 12,
      "boxes_with_labels": 8,
      "common_labels": ["FRAGILE", "Amazon"],
      "arrangement": "stacked_pyramid"
    },
    "confidence_score": 0.85
  }
}
```

## 🔧 Customization

### Modify AI Prompt
Edit `prompt.txt` to customize the AI analysis behavior:

```bash
python prompt_manager.py edit    # Edit prompt
python prompt_manager.py backup  # Create backup
python prompt_manager.py show    # View current prompt
```

## 📋 Endpoints

- **GET** `/` - API information
- **GET** `/health` - Health check
- **POST** `/count-boxes` - Detailed box analysis
- **POST** `/count-boxes-simple` - Simple count and labels

## 🛠️ Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [OpenAI GPT-4o](https://openai.com/) - Advanced vision AI model
- [Pillow](https://python-pillow.org/) - Image processing
- [Uvicorn](https://www.uvicorn.org/) - ASGI web server

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- 📚 Check the documentation in `/docs`
- 🐛 Report issues on GitHub
- 💬 Join discussions in GitHub Discussions