from fastapi import FastAPI

app = FastAPI(title="LoadMap AI", version="0.1.0")

@app.get("/")
def roof():
    return {"message" : "Hello from LoadMap AI - Engineer-ready load mapping"}