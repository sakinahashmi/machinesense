from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db
from app.api import (
    health,
    dashboard,
    machines,
    investigations,
    maintenance,
    historical_cases,
    insights
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and load datasets
    print("Initializing MachineSense database and manufacturing datasets...")
    init_db()
    print("MachineSense backend ready!")
    yield
    # Shutdown
    print("MachineSense backend shutting down...")


# Initialize database tables & datasets
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(health.router)
app.include_router(dashboard.router)
app.include_router(machines.router)
app.include_router(investigations.router)
app.include_router(maintenance.router)
app.include_router(historical_cases.router)
app.include_router(insights.router)


@app.get("/")
def read_root():
    return {
        "message": "MachineSense API is running",
        "status": "online",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
