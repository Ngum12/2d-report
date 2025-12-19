from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.config import APP_NAME, APP_DESCRIPTION
from app.database import init_db
from app.routes import annotator_router, dashboard_router, export_router, slack_router

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(annotator_router)
app.include_router(dashboard_router)
app.include_router(export_router)
app.include_router(slack_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Redirect root to annotator log page."""
    return RedirectResponse(url="/log")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return RedirectResponse(url="/log")

