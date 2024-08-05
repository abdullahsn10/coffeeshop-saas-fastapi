import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# database settings
DATABASE_SETTINGS = {
    "URL": os.getenv("SQLALCHEMY_DATABASE_URL"),
}

