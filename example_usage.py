"""
Example of how to use the Vision AI Box Counting API programmatically
"""

import requests
import json
import base64
import os
from pathlib import Path

class BoxCountingClient:
    """Client for the Vision AI Box Counting API"""
    
    def __init__(self, base_url="http://127.0.0.1:8000", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def health_check(self):
        """Check if the API is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
    
    def count_boxes_detailed(self, image_path):
        """Get detailed box counting analysis"""
        with open(image_path, 'rb') as f:
            files = {'file': (Path(image_path).name, f, 'image/jpeg')}
            response = requests.post(f"{self.base_url}/count-boxes", files=files, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("Authentication failed. Please check your API key.")
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    def count_boxes_simple(self, image_path):
        """Get simple box count and labels"""
        with open(image_path, 'rb') as f:
            files = {'file': (Path(image_path).name, f, 'image/jpeg')}
            response = requests.post(f"{self.base_url}/count-boxes-simple", files=files, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("Authentication failed. Please check your API key.")
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

def example_usage():
    """Example of how to use the client"""
    
    # API key is required
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ API_KEY environment variable is required!")
        print("   Set it in your .env file or environment variables")
        print("   Example: API_KEY=your_secure_api_key_here")
        return
    
    client = BoxCountingClient(api_key=api_key)
    print(f"� Using API key authentication")
    
    # Check if API is running
    if not client.health_check():
        print("❌ API is not running. Please start the server first.")
        print("   Run: uvicorn main:app --reload --port 8000")
        return
    
    print("✅ API is running")
    
    # Example image path (replace with your image)
    image_path = "example_boxes.jpg"
    
    if not Path(image_path).exists():
        print(f"⚠️  Example image not found: {image_path}")
        print("   Please replace 'image_path' with the path to your image")
        return
    
    try:
        # Get detailed analysis
        print(f"\n🔍 Analyzing image: {image_path}")
        detailed_result = client.count_boxes_detailed(image_path)
        
        print("\n📊 Detailed Analysis:")
        print(f"   Filename: {detailed_result['filename']}")
        print(f"   File size: {detailed_result['file_size_bytes']} bytes")
        
        analysis = detailed_result['analysis']
        if 'total_count' in analysis:
            print(f"   📦 Total boxes: {analysis['total_count']}")
            print(f"   🎯 Confidence: {analysis.get('confidence_score', 'N/A')}")
            
            # Show box details
            for i, box in enumerate(analysis.get('box_details', [])[:3]):  # Show first 3
                print(f"   Box {i+1}: {box.get('type', 'unknown')} "
                      f"(confidence: {box.get('confidence', 'N/A')})")
                if box.get('labels'):
                    print(f"           Labels: {', '.join(box['labels'])}")
        
        # Get simple analysis
        print(f"\n🔍 Simple Analysis:")
        simple_result = client.count_boxes_simple(image_path)
        print(f"   📦 Count: {simple_result.get('count', 'N/A')}")
        print(f"   🏷️  Labels: {simple_result.get('labels', [])}")
        print(f"   🎯 Confidence: {simple_result.get('confidence', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def create_test_curl_commands():
    """Generate test curl commands"""
    print("\n📋 Test with curl commands:")
    print("\n1. Health check:")
    print("   curl http://127.0.0.1:8000/health")
    
    print("\n2. Detailed box counting:")
    print("   curl -X POST \"http://127.0.0.1:8000/count-boxes\" \\")
    print("     -H \"Authorization: Bearer YOUR_API_KEY\" \\")
    print("     -F \"file=@your_image.jpg\"")
    
    print("\n3. Simple box counting:")
    print("   curl -X POST \"http://127.0.0.1:8000/count-boxes-simple\" \\")
    print("     -H \"Authorization: Bearer YOUR_API_KEY\" \\")
    print("     -F \"file=@your_image.jpg\"")
    
    print("\n   Note: Replace YOUR_API_KEY with your actual API key from .env file")

if __name__ == "__main__":
    print("🤖 Vision AI Box Counting - Example Usage")
    print("="*50)
    
    example_usage()
    create_test_curl_commands()
    
    print("\n💡 Pro tips:")
    print("   - Use high-quality images for better accuracy")
    print("   - Ensure boxes are clearly visible and well-lit")
    print("   - The AI works best with organized arrangements")
    print("   - Multiple angles can help with complex stacks")