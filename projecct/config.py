import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    # Pull your API key from the environment variable EXCHANGE_API_KEY
    API_KEY = os.getenv("EXCHANGE_API_KEY")
    # Use placeholders for API key and the currency code
    API_URL = "https://v6.exchangerate-api.com/v6/{}/latest/{}"
    
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")