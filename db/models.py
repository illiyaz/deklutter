from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, LargeBinary
from sqlalchemy.sql import func
from .session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)  # nullable for OAuth-only users
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    provider = Column(String)              # 'google'
    scope = Column(Text)
    access_token = Column(LargeBinary)     # encrypted
    refresh_token = Column(LargeBinary)    # encrypted
    expiry = Column(DateTime)

class MailDecisionLog(Base):
    __tablename__ = "mail_decision_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    message_id = Column(String, index=True)
    sender_hash = Column(String, index=True)
    subject = Column(Text)
    size_bytes = Column(Integer)
    internal_date = Column(DateTime)
    proposed = Column(String)              # keep/review/delete
    confidence = Column(Integer)           # 0-100
    applied = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    action = Column(String)                # scan, delete, revoke, etc.
    provider = Column(String)              # google, yahoo, etc.
    details = Column(Text)                 # JSON with action details
    items_count = Column(Integer)          # number of items processed
    created_at = Column(DateTime, server_default=func.now(), index=True)

class OAuthState(Base):
    __tablename__ = "oauth_states"
    id = Column(Integer, primary_key=True)
    state = Column(String, unique=True, index=True)  # The OAuth state token
    provider = Column(String)              # 'google', 'yahoo', etc.
    source = Column(String)                # 'gpt', 'web', etc.
    user_id = Column(Integer, nullable=True)  # Optional: if we know the user
    redirect_uri = Column(String, nullable=True)  # Where to redirect after OAuth
    expires_at = Column(DateTime, index=True)  # State expires after 30 minutes
    created_at = Column(DateTime, server_default=func.now())