from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from app.api.routers import files, jobs, plans, rooms, rules

app = FastAPI(
    title="LoadMap AI",
    version="0.1.0",
    description="Engineer-readyv tool for generating draft load maps from architectural plans."
)

app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(rooms.router, tags=["rooms"])
app.include_router(rules.router, prefix="/rules", tags=["rules"])

# Unified error payload: {"error": {"code": <int>, "message", "<detail>""}}
@app.exception_handler(StarletteHTTPException)
async def http_exception_handlet(
    request: Request,
    exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.detail}},
    )

@app.get("/")
def root():
    return {"message": "Welcome to LoadMap AI"}

@app.get("/health")
def health():
    return {"status": "OK!"}

