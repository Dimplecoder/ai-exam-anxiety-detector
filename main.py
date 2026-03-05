from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is working"}

@app.get("/docs-test")
def test():
    return {"status": "ok"}