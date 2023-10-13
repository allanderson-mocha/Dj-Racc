import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_SECRET_API = os.getenv("DISCORD_API_TOKEN")