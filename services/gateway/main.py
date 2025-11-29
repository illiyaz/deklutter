
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from db.session import Base, engine
from db import models  # Import models so they're registered with Base
from services.gateway.routes_gmail import router as gmail_router
from services.gateway.routes_universal import router as universal_router
from services.gateway.routes_oauth import router as oauth_router
from services.gateway.routes_stats import router as stats_router
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

# Load custom OpenAPI schema at startup
def load_custom_openapi():
    """Load custom OpenAPI schema from openapi.yaml file"""
    import yaml
    
    possible_paths = [
        "/opt/render/project/src/openapi.yaml",
        os.path.join(os.getcwd(), "openapi.yaml"),
        os.path.join(os.path.dirname(__file__), "..", "..", "openapi.yaml"),
        "openapi.yaml"
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    schema = yaml.safe_load(f)
                if schema and 'openapi' in schema:
                    logger.info(f"✅ Loaded custom OpenAPI schema from: {path}")
                    return schema
        except Exception as e:
            logger.error(f"Error loading from {path}: {e}")
            continue
    
    logger.warning("⚠️ Could not load custom openapi.yaml, using FastAPI defaults")
    return None

# Try to load custom schema
custom_openapi_schema = load_custom_openapi()

# Create FastAPI app
if custom_openapi_schema:
    app = FastAPI(
        title=custom_openapi_schema.get('info', {}).get('title', 'Deklutter API'),
        version=custom_openapi_schema.get('info', {}).get('version', '1.0.0'),
        description=custom_openapi_schema.get('info', {}).get('description', ''),
        servers=custom_openapi_schema.get('servers', [])
    )
    # Override the openapi method to return our custom schema
    def custom_openapi():
        return custom_openapi_schema
    app.openapi = custom_openapi
else:
    app = FastAPI(title="Deklutter API", version="0.1.0")

logger.info("Starting Deklutter API...")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    """Health check endpoint for monitoring"""
    import time
    from db.session import SessionLocal
    from sqlalchemy import text
    
    # Check database connection
    db_healthy = False
    db_error = None
    tables_exist = False
    
    try:
        db = SessionLocal()
        # Test basic query
        db.execute(text("SELECT 1"))
        db_healthy = True
        
        # Check if tables exist
        result = db.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('users', 'oauth_tokens', 'mail_decision_logs')
        """))
        count = result.scalar()
        tables_exist = (count >= 3)
        
        db.close()
    except Exception as e:
        db_error = str(e)
        logger.error(f"Database health check failed: {e}")
    
    return {
        "status": "healthy" if (db_healthy and tables_exist) else "degraded",
        "version": "1.0.0",
        "timestamp": int(time.time()),
        "services": {
            "database": "healthy" if db_healthy else "unhealthy",
            "api": "healthy",
            "tables": "created" if tables_exist else "missing"
        },
        "debug": {
            "db_error": db_error,
            "tables_exist": tables_exist
        } if db_error or not tables_exist else None
    }

@app.get("/debug/files")
def debug_files():
    """Debug endpoint to see what files are available"""
    import glob
    cwd = os.getcwd()
    files = {
        "cwd": cwd,
        "files_in_cwd": os.listdir(cwd),
        "openapi_yaml_exists": os.path.exists(os.path.join(cwd, "openapi.yaml")),
        "dirname_file": os.path.dirname(__file__),
        "glob_yaml": glob.glob("**/*.yaml", recursive=True)[:20]
    }
    return files

# OpenAPI schema is now served automatically by FastAPI via app.openapi override

@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    from services.gateway.privacy_policy import PRIVACY_POLICY_HTML
    return PRIVACY_POLICY_HTML

@app.get("/terms", response_class=HTMLResponse)
def terms():
    return """
    <html><body>
    <h1>Terms of Service - Deklutter</h1>
    <p>This is a development/testing application.</p>
    <p>By using this service, you agree to allow Deklutter to access your Gmail for spam detection purposes.</p>
    </body></html>
    """

@app.get("/version")
def version():
    """Get API version and build info"""
    return {
        "version": "1.0.0",
        "build_date": "2025-10-19",
        "features": {
            "gmail": True,
            "yahoo": False,
            "outlook": False,
            "drive": False
        },
        "status": "production"
    }

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(gpt_oauth_router, prefix="/auth", tags=["GPT OAuth"])
app.include_router(oauth_router, prefix="/oauth", tags=["Universal OAuth"])
app.include_router(stats_router, prefix="/api", tags=["Statistics"])
app.include_router(gmail_router, prefix="", tags=["Gmail (Legacy)"])
app.include_router(universal_router, prefix="/v1", tags=["Universal API"])