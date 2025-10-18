
import os
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from db.session import Base, engine
from db import models  # Import models so they're registered with Base
from services.gateway.routes_gmail import router as gmail_router
from services.gateway.routes_universal import router as universal_router
from services.gateway.routes_oauth import router as oauth_router
from services.auth.routes import router as auth_router
from services.auth.gpt_oauth import router as gpt_oauth_router

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

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>Deklutter API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2563eb; }
            .status { color: #16a34a; font-weight: bold; }
            a { color: #2563eb; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .endpoint { background: #f3f4f6; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>📧 Deklutter API</h1>
        <p class="status">✅ Status: Online</p>
        <p>AI-powered Gmail inbox cleaner - Automatically identify and remove spam, newsletters, and promotional emails.</p>
        
        <h2>🚀 Quick Links</h2>
        <div class="endpoint">
            <a href="/docs" target="_blank">📚 API Documentation (Swagger)</a>
        </div>
        <div class="endpoint">
            <a href="/health" target="_blank">💚 Health Check</a>
        </div>
        
        <h2>🔗 Resources</h2>
        <ul>
            <li><a href="https://github.com/illiyaz/deklutter" target="_blank">GitHub Repository</a></li>
            <li><a href="/privacy">Privacy Policy</a></li>
            <li><a href="/terms">Terms of Service</a></li>
        </ul>
        
        <h2>📖 API Endpoints</h2>
        <ul>
            <li><code>POST /auth/signup</code> - Create account</li>
            <li><code>POST /auth/login</code> - Login</li>
            <li><code>POST /auth/google/init</code> - Initialize Gmail OAuth</li>
            <li><code>POST /gmail/scan</code> - Scan Gmail inbox</li>
            <li><code>POST /gmail/apply</code> - Apply cleanup</li>
        </ul>
        
        <p style="margin-top: 40px; color: #6b7280; font-size: 14px;">
            Powered by FastAPI | Deployed on Render
        </p>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/openapi.json")
def get_openapi_schema():
    """Serve OpenAPI schema for GPT Actions and API documentation"""
    import yaml
    
    openapi_path = os.path.join(os.path.dirname(__file__), "..", "..", "openapi.yaml")
    try:
        with open(openapi_path, 'r') as f:
            openapi_dict = yaml.safe_load(f)
        return openapi_dict
    except FileNotFoundError:
        # Fallback to FastAPI's built-in OpenAPI
        return app.openapi()

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
app.include_router(gpt_oauth_router, prefix="/auth", tags=["GPT OAuth"])
app.include_router(oauth_router, prefix="/oauth", tags=["Universal OAuth"])
app.include_router(gmail_router, prefix="", tags=["Gmail (Legacy)"])
app.include_router(universal_router, prefix="/v1", tags=["Universal API"])