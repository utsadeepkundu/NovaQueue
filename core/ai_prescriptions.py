import requests
import json
from django.conf import settings

def get_available_models(api_key):
    """
    Dynamically fetches the list of models available to this API key.
    This solves the 'guessing game' of which model version is active.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Filter for models that support generateContent
            # The 'name' field usually looks like 'models/gemini-1.5-flash'
            available = [
                m['name'].replace('models/', '') 
                for m in data.get('models', []) 
                if 'generateContent' in m.get('supportedGenerationMethods', [])
            ]
            return available
    except Exception as e:
        print(f"Error listing models: {e}")
    return []

def generate_ai_prescription(raw_notes):
    """
    Sends raw doctor notes to Gemini and returns a structured health plan.
    """
    # Replace with your actual key if not using settings
    # Transcribed from your screenshot:
    api_key = "AIzaSyC61ZYwr-ygcjb9-x0IC_Rp9OavuJWXTD0"  # settings.GEMINI_API_KEY
    
    if not api_key:
        print("DEBUG: API Key is missing")
        return "AI processing unavailable: Missing API Key."
    
    # Ensure no accidental whitespace
    api_key = api_key.strip()

    # 1. Try standard preferred models first (Fastest/Cheapest)
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]
    
    prompt = f"""
    Act as a helpful medical assistant. 
    Convert these doctor's notes into a clear, HTML-formatted health plan for a patient.
    Use <b> for headings. Do NOT use Markdown (no ** or ##).
    
    Structure:
    1. Medication Table (Name, Dosage, Frequency)
    2. Diet & Lifestyle Advice
    3. Warning Signs (When to return)
    
    Doctor's Notes: {raw_notes}
    """
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    last_error = ""
    
    # Attempt hardcoded list first
    print("--- Starting AI Prescription Generation ---")
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            print(f"Attempting with model: {model_name}...")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                ai_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if ai_text: 
                    print("Success!")
                    return ai_text
            elif response.status_code == 404:
                print(f"{model_name} not found (404).")
            else:
                print(f"{model_name} failed: {response.status_code} - {response.text}")
                last_error = f"{response.status_code} error"
                
        except Exception as e:
            print(f"Connection error with {model_name}: {e}")
            continue

    # 2. If we get here, hardcoded models failed. Let's auto-discover what IS available.
    print("Hardcoded models failed. Auto-discovering available models...")
    discovered_models = get_available_models(api_key)
    print(f"Discovered models: {discovered_models}")
    
    for model_name in discovered_models:
        if model_name in models_to_try: continue # Already tried these
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            print(f"Attempting with discovered model: {model_name}...")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                ai_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if ai_text: 
                    print(f"Success with {model_name}!")
                    return ai_text
        except:
            continue

    return f"AI Assistant Unavailable. (Last Error: {last_error})"