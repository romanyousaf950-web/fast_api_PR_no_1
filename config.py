import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "User Management API")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"