"""
Statistics and analytics endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from db.session import get_db
from db.models import MailDecisionLog, ActivityLog
from services.gateway.deps import CurrentUser, get_current_user
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/stats")
def get_user_stats(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's email cleanup statistics
    
    Returns:
    - Total emails scanned
    - Total emails deleted
    - Space saved (MB)
    - Breakdown by decision (delete/review/keep)
    - Recent activity
    """
    
    # Total emails scanned
    total_scanned = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id
    ).count()
    
    # Total emails deleted (applied)
    total_deleted = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.proposed == "delete",
        MailDecisionLog.applied == True
    ).count()
    
    # Space saved (sum of deleted email sizes)
    space_saved_bytes = db.query(
        func.sum(MailDecisionLog.size_bytes)
    ).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.proposed == "delete",
        MailDecisionLog.applied == True
    ).scalar() or 0
    
    space_saved_mb = round(space_saved_bytes / (1024 * 1024), 2)
    
    # Breakdown by decision
    breakdown = db.query(
        MailDecisionLog.proposed,
        func.count(MailDecisionLog.id).label('count'),
        func.sum(MailDecisionLog.size_bytes).label('total_size')
    ).filter(
        MailDecisionLog.user_id == user.user_id
    ).group_by(MailDecisionLog.proposed).all()
    
    breakdown_dict = {}
    for decision, count, total_size in breakdown:
        breakdown_dict[decision] = {
            "count": count,
            "size_mb": round((total_size or 0) / (1024 * 1024), 2)
        }
    
    # Recent activity (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_scanned = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.created_at >= seven_days_ago
    ).count()
    
    recent_deleted = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.proposed == "delete",
        MailDecisionLog.applied == True,
        MailDecisionLog.created_at >= seven_days_ago
    ).count()
    
    # Last scan date
    last_scan = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id
    ).order_by(desc(MailDecisionLog.created_at)).first()
    
    last_scan_date = last_scan.created_at.isoformat() if last_scan else None
    
    return {
        "user_id": user.user_id,
        "all_time": {
            "total_scanned": total_scanned,
            "total_deleted": total_deleted,
            "space_saved_mb": space_saved_mb,
            "breakdown": breakdown_dict
        },
        "last_7_days": {
            "scanned": recent_scanned,
            "deleted": recent_deleted
        },
        "last_scan_date": last_scan_date,
        "message": f"You've saved {space_saved_mb} MB by deleting {total_deleted} emails! 🎉" if total_deleted > 0 else "Start scanning to see your stats!"
    }


@router.get("/stats/top-senders")
def get_top_spam_senders(
    user: CurrentUser = Depends(get_current_user),
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top spam senders (emails marked for deletion)
    
    Returns list of senders with:
    - Sender hash (anonymized)
    - Number of emails
    - Total size
    - Sample subject lines
    """
    
    # Group by sender_hash for deleted emails
    top_senders = db.query(
        MailDecisionLog.sender_hash,
        func.count(MailDecisionLog.id).label('email_count'),
        func.sum(MailDecisionLog.size_bytes).label('total_size'),
        func.array_agg(MailDecisionLog.subject).label('subjects')
    ).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.proposed == "delete"
    ).group_by(
        MailDecisionLog.sender_hash
    ).order_by(
        desc('email_count')
    ).limit(limit).all()
    
    results = []
    for sender_hash, count, total_size, subjects in top_senders:
        # Get a sample subject (first one)
        sample_subject = subjects[0] if subjects else "No subject"
        
        results.append({
            "sender_hash": sender_hash,
            "email_count": count,
            "size_mb": round((total_size or 0) / (1024 * 1024), 2),
            "sample_subject": sample_subject,
            "percentage": round((count / max(1, db.query(MailDecisionLog).filter(
                MailDecisionLog.user_id == user.user_id,
                MailDecisionLog.proposed == "delete"
            ).count())) * 100, 1)
        })
    
    return {
        "top_spam_senders": results,
        "total_senders": len(results),
        "message": f"Top {len(results)} spam senders found!"
    }


@router.get("/stats/timeline")
def get_cleanup_timeline(
    user: CurrentUser = Depends(get_current_user),
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get cleanup activity timeline (daily breakdown)
    
    Returns daily stats for the last N days
    """
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get daily counts
    daily_stats = db.query(
        func.date(MailDecisionLog.created_at).label('date'),
        func.count(MailDecisionLog.id).label('scanned'),
        func.sum(
            func.cast(MailDecisionLog.applied, Integer)
        ).label('deleted')
    ).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.created_at >= start_date
    ).group_by(
        func.date(MailDecisionLog.created_at)
    ).order_by('date').all()
    
    timeline = []
    for date, scanned, deleted in daily_stats:
        timeline.append({
            "date": str(date),
            "scanned": scanned,
            "deleted": deleted or 0
        })
    
    return {
        "timeline": timeline,
        "days": days,
        "total_days_active": len(timeline)
    }


@router.get("/stats/summary")
def get_quick_summary(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Quick summary for GPT to show users
    
    Returns a concise, user-friendly summary
    """
    
    total_deleted = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.proposed == "delete",
        MailDecisionLog.applied == True
    ).count()
    
    space_saved_bytes = db.query(
        func.sum(MailDecisionLog.size_bytes)
    ).filter(
        MailDecisionLog.user_id == user.user_id,
        MailDecisionLog.proposed == "delete",
        MailDecisionLog.applied == True
    ).scalar() or 0
    
    space_saved_mb = round(space_saved_bytes / (1024 * 1024), 2)
    
    # Last scan
    last_scan = db.query(MailDecisionLog).filter(
        MailDecisionLog.user_id == user.user_id
    ).order_by(desc(MailDecisionLog.created_at)).first()
    
    if not last_scan:
        return {
            "message": "No scans yet! Start by scanning your inbox.",
            "has_data": False
        }
    
    days_since_last_scan = (datetime.now() - last_scan.created_at).days
    
    return {
        "message": f"🎉 You've cleaned {total_deleted} emails and saved {space_saved_mb} MB!",
        "total_deleted": total_deleted,
        "space_saved_mb": space_saved_mb,
        "last_scan_days_ago": days_since_last_scan,
        "has_data": True
    }
