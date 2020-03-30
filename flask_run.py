from app import create_app
from dynaconf import settings
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

application = create_app()

# Uncomment this while testing the app locally
if os.environ.get("ENVIRONMENT") == "development":
    application.run(host="0.0.0.0", port=5000, debug=True)

