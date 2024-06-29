import requests
import os

gemini_api_key = "AIzaSyATbMmZOg2ZXOPZWCk09vHheOgdKgFXy1o"
gemini_api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

def get_recommendations(user_data):
    headers = {
        'Authorization': f'Bearer {gemini_api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'age': user_data['age'],
        'gender': user_data['gender'],
        'weight': user_data['weight'],
        'height': user_data['height']
    }

    try:
        response = requests.post(gemini_api_url + '/recommendations', json=payload, headers=headers)
        response.raise_for_status()
        
        # Print full response details for debugging
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())
        
        recommendations = response.json().get('recommendations', [])
        print("Recommendations from Gemini API:", recommendations)  # Debug print
        
        return recommendations
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Gemini API: {e}")
        return None
