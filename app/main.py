from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.logger import get_logger
from app.backend.routes import router

logger = get_logger("main")

app = FastAPI(title="Clash Royale AI Coach")
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

logger.info("FastAPI application initialized")
