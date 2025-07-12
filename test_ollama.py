"""
Ollama Test Utility
Quick script to test Ollama connection and available models
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def test_ollama_connection():
    """Test Ollama connectivity and model availability"""
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    
    print(f"🧪 Testing Ollama at {ollama_url}")
    print(f"🤖 Expected model: {ollama_model}")
    print("-" * 50)
    
    try:
        # Test basic connectivity
        print("1. Testing basic connectivity...")
        response = requests.get(f"{ollama_url}/api/version", timeout=10)
        
        if response.status_code == 200:
            version_info = response.json()
            print(f"   ✅ Ollama is running (version: {version_info.get('version', 'unknown')})")
        else:
            print(f"   ❌ Ollama responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Ollama at {ollama_url}")
        print(f"   💡 Make sure Ollama is running. Try: ollama serve")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    try:
        # Test available models
        print("\n2. Checking available models...")
        response = requests.get(f"{ollama_url}/api/tags", timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('models', [])
            
            if models:
                print(f"   ✅ Found {len(models)} models:")
                for model in models:
                    name = model.get('name', 'unknown')
                    size = model.get('size', 0)
                    size_mb = size / (1024 * 1024) if size else 0
                    print(f"      - {name} ({size_mb:.1f} MB)")
                    
                # Check if our target model is available
                model_names = [model.get('name', '') for model in models]
                if any(ollama_model in name for name in model_names):
                    print(f"   ✅ Target model '{ollama_model}' is available!")
                else:
                    print(f"   ⚠️  Target model '{ollama_model}' not found!")
                    print(f"   💡 You can download it with: ollama pull {ollama_model}")
                    return False
            else:
                print("   ⚠️  No models found!")
                print(f"   💡 Download the model with: ollama pull {ollama_model}")
                return False
        else:
            print(f"   ❌ Error getting models: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking models: {e}")
        return False
    
    try:
        # Test generation
        print("\n3. Testing text generation...")
        test_prompt = "Hello! Please respond with just the word 'SUCCESS' to confirm you're working."
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": ollama_model,
                "prompt": test_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "max_tokens": 50
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '').strip()
            print(f"   ✅ Generation test successful!")
            print(f"   📝 Response: {generated_text[:100]}...")
            
            if 'SUCCESS' in generated_text.upper():
                print(f"   🎯 Model responded correctly!")
            else:
                print(f"   ⚠️  Model response was unexpected, but generation works")
                
        else:
            print(f"   ❌ Generation failed: HTTP {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing generation: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Ollama is ready for use.")
    return True


def suggest_models():
    """Suggest good models for summarization"""
    print("\n🤖 Recommended models for Discord summarization:")
    print("   • llama3.2 (small, fast, good for summaries)")
    print("   • llama3.1 (larger, more detailed)")
    print("   • mistral (good alternative)")
    print("   • phi3 (very fast, Microsoft model)")
    
    print("\n💡 To download a model:")
    print("   ollama pull llama3.2")
    print("   ollama pull mistral")


if __name__ == "__main__":
    print("🧪 Ollama Test Utility")
    print("=" * 30)
    
    if not test_ollama_connection():
        print("\n❌ Ollama test failed!")
        suggest_models()
    else:
        print("\n✅ Everything looks good!")
    
    input("\nPress Enter to exit...")
