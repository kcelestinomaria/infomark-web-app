# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
personal_access_token = os.getenv('PAT')
