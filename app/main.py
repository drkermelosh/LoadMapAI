from fastapi import FastAPI
from app.api.routers import files, jobs, rooms, rules

app = FastAPI(
    title="LoadMap AI",
    version="0.1.0",
    description="Engineer-readyv tool for generating draft load maps from architectural plans."
)

app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(rooms.router, tags=["rooms"])
app.include_router(rules.router, prefix="/rules", tags=["rules"])

@app.get("/")
def root():
    return {"message": "Welcome to LoadMap AI"}

@app.get("/health")
def health():
    return {"status": "OK!"}

