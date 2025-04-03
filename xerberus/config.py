from dotenv import load_dotenv
import os

def get_config():
    load_dotenv()
    return {
        "API_URL": os.getenv("API_URL", "https://xerberus-metrics-api-515850710964.us-central1.run.app/graphql"),
        "XERBERUS_API_KEY": os.getenv("XERBERUS_API_KEY", ""),
        "XERBERUS_API_EMAIL": os.getenv("XERBERUS_API_EMAIL")
    }
