from uvicorn import run
from src.main import app

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
