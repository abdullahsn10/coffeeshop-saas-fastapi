import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# database settings
DATABASE_SETTINGS = {
    "URL": os.getenv("SQLALCHEMY_DATABASE_URL"),
}

# security settings
with open(os.getenv("PRIVATE_KEY_PATH"), "r") as key_file:
    PRIVATE_KEY = key_file.read()

with open(os.getenv("PUBLIC_KEY_PATH"), "r") as key_file:
    PUBLIC_KEY = key_file.read()


JWT_TOKEN_SETTINGS = {
    "PRIVATE_KEY": PRIVATE_KEY,
    "PUBLIC_KEY": PUBLIC_KEY,
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
}

