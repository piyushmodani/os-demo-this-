from fastapi import FastAPI

from app.api.chat import router as chat_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    application = FastAPI(
        title="AI Financial Mentor API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Mount routers
    application.include_router(chat_router)

    return application


app = create_app()