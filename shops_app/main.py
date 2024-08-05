from fastapi import FastAPI

app = FastAPI()


#register routes


@app.get("/")
def read_root():
    """
    root path endpoint
    """
    return {"Hello": "World"}
