#needed for deployment
"""
"""
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


#comment out above when deploy
from server.api import create_app
app = create_app(os.getenv("PROJECT_MODE", "production"))
