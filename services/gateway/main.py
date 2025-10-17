
import os
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from db.session import Base, engine
from db import models  # Import models so they're registered with Base
from services.gateway.routes_gmail import router as gmail_router
from services.auth.routes import router as auth_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set specific log levels
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI(title="Deklutter API", version="0.1.0")

logger.info("Starting Deklutter API...")

# create tables on boot (for dev)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    return """
    <html><body>
    <h1>Privacy Policy - Deklutter</h1>
    <p>This is a development/testing application.</p>
    <p>We collect and store OAuth tokens to access your Gmail for spam detection.</p>
    <p>Data is encrypted and stored securely. You can revoke access anytime.</p>
    </body></html>
    """

@app.get("/terms", response_class=HTMLResponse)
def terms():
    return """
    <html><body>
    <h1>Terms of Service - Deklutter</h1>
    <p>This is a development/testing application.</p>
    <p>By using this service, you agree to allow Deklutter to access your Gmail for spam detection purposes.</p>
    </body></html>
    """

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(gmail_router, prefix="", tags=["Gmail"])