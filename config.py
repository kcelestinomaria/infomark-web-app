# config.py
import os
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
personal_access_token = os.getenv('PAT')

#genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')