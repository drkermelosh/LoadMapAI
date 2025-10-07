from fastapi import FastAPI
from app.api import routes_files, routes_jobs, routes_plans, routes_rules

app = FastAPI(
    title="LoadMap AI",
    version="0.1.0",
    description="Engineer-ready tool for generating draft load maps from architectural plans."
)

app.include_router(routes_files.router, prefix="/files", tags=["files"])
app.include_router(routes_jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(routes_plans.router, prefix="/plans", tags=["plans"])
app.include_router(routes_rules.router, prefix="/rules", tags=["rules"])

@app.get("/")
def root():
    return {"message": "Welcome to LoadMap AI"}

@app.get("/health")
def health():
    return {"status": "OK!"}
