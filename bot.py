import os
import krakenex
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

api_key = os.getenv("KRAKEN_API_KEY")
api_secret = os.getenv("KRAKEN_API_SECRET")

# Connect to Kraken
kraken = krakenex.API()
kraken.key = api_key
kraken.secret = api_secret

# Test connection
response = kraken.query_private("Balance")

if response["error"]:
    print("Connection failed:")
    print(response["error"])
else:
    print("✅ Kraken connection successful!")
    print("Account balances:")
    print(response["result"])

