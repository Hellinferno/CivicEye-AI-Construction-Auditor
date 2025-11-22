import os
import google.generativeai as genai
from dotenv import load_dotenv

def check_models():
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    print("Listing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

if __name__ == "__main__":
    check_models()
