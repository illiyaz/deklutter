
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

@app.get("/openapi.json")
def get_openapi_schema():
    """Serve OpenAPI schema for GPT Actions and API documentation"""
    import yaml
    
    # Try multiple paths (order matters - try most specific first)
    possible_paths = [
        "/opt/render/project/src/openapi.yaml",  # Render's path (try first)
        os.path.join(os.getcwd(), "openapi.yaml"),  # Current working directory
        os.path.join(os.path.dirname(__file__), "..", "..", "openapi.yaml"),  # Relative to this file
        "openapi.yaml"  # Direct path
    ]
    
    for openapi_path in possible_paths:
        try:
            logger.info(f"Trying to load OpenAPI schema from: {openapi_path}")
            if not os.path.exists(openapi_path):
                logger.info(f"Path does not exist: {openapi_path}")
                continue
            
            with open(openapi_path, 'r') as f:
                openapi_dict = yaml.safe_load(f)
            
            # Validate it has required fields
            if not openapi_dict or 'openapi' not in openapi_dict:
                logger.error(f"Invalid OpenAPI schema in {openapi_path}")
                continue
                
            logger.info(f"✅ Successfully loaded OpenAPI schema from: {openapi_path}")
            return openapi_dict
        except FileNotFoundError as e:
            logger.info(f"File not found: {openapi_path}")
            continue
        except Exception as e:
            logger.error(f"❌ Error loading OpenAPI from {openapi_path}: {str(e)}", exc_info=True)
            continue
    
    # Fallback to FastAPI's built-in OpenAPI
    logger.warning("Could not find openapi.yaml, using FastAPI auto-generated schema")
    return app.openapi()

@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    return """
    <html>
    <head>
        <title>Privacy Policy - Deklutter</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; line-height: 1.6; }
            h1 { color: #2563eb; }
            h2 { color: #1e40af; margin-top: 30px; }
            .highlight { background: #dbeafe; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .important { color: #dc2626; font-weight: bold; }
            ul { margin: 10px 0; }
            li { margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>🔐 Privacy Policy - Deklutter</h1>
        <p><em>Last updated: October 18, 2025</em></p>
        
        <h2>📧 What We Access</h2>
        <div class="highlight">
            <p><strong>We ONLY read email metadata:</strong></p>
            <ul>
                <li>✅ Sender email address</li>
                <li>✅ Subject line</li>
                <li>✅ Date received</li>
                <li>✅ Email size</li>
                <li>✅ Labels/categories</li>
            </ul>
            <p class="important">❌ We NEVER read email content/body</p>
            <p class="important">❌ We NEVER read attachments</p>
            <p class="important">❌ We NEVER send emails on your behalf</p>
        </div>
        
        <h2>🔒 Data Storage & Security</h2>
        <ul>
            <li><strong>OAuth Tokens:</strong> Encrypted with AES-256, stored securely</li>
            <li><strong>Email Metadata:</strong> Analyzed in real-time, not permanently stored</li>
            <li><strong>Activity Logs:</strong> Kept for 90 days for your reference</li>
            <li><strong>User Data:</strong> Deleted completely upon revocation</li>
        </ul>
        
        <h2>⏱️ Access Duration</h2>
        <ul>
            <li><strong>Access Token:</strong> 1 hour (auto-renewed seamlessly)</li>
            <li><strong>Refresh Token:</strong> 90 days</li>
            <li><strong>Total Access:</strong> Until you revoke (instant revocation available)</li>
        </ul>
        
        <h2>🛡️ Your Rights</h2>
        <div class="highlight">
            <p><strong>You can at any time:</strong></p>
            <ul>
                <li>✅ Revoke access instantly (say "revoke access" to the GPT)</li>
                <li>✅ View your activity log</li>
                <li>✅ Request data deletion</li>
                <li>✅ Export your data</li>
            </ul>
        </div>
        
        <h2>📊 What We Do With Your Data</h2>
        <ul>
            <li><strong>Classification:</strong> Identify spam/promotional emails using AI</li>
            <li><strong>Statistics:</strong> Show you inbox analytics</li>
            <li><strong>Cleanup:</strong> Move unwanted emails to trash (recoverable for 30 days)</li>
        </ul>
        <p class="important">We NEVER sell, share, or use your data for advertising.</p>
        
        <h2>🔐 Security Measures</h2>
        <ul>
            <li>✅ End-to-end encryption for all tokens</li>
            <li>✅ Secure HTTPS connections only</li>
            <li>✅ Regular security audits</li>
            <li>✅ No third-party data sharing</li>
            <li>✅ Minimal data retention</li>
        </ul>
        
        <h2>📞 Contact Us</h2>
        <p>Questions about privacy? Email us at: <strong>mohammad.illiyaz@gmail.com</strong></p>
        
        <h2>🔄 Revoke Access</h2>
        <div class="highlight">
            <p><strong>To revoke access:</strong></p>
            <ol>
                <li>Say "revoke access" to the Deklutter GPT, OR</li>
                <li>Visit <a href="https://myaccount.google.com/permissions">Google Account Permissions</a>, OR</li>
                <li>Email us at mohammad.illiyaz@gmail.com</li>
            </ol>
            <p><em>All your data will be deleted immediately upon revocation.</em></p>
        </div>
        
        <p style="margin-top: 40px; color: #6b7280; font-size: 14px;">
            Powered by FastAPI | Deployed on Render | <a href="/">Back to Home</a>
        </p>
    </body>
    </html>
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