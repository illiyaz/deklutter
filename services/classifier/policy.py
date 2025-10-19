import hashlib
from .llm_adapter import judge_edge_cases

BULK_HINTS = ("unsubscribe", "newsletter", "marketing", "promotional")

# Gmail's built-in categories (most reliable)
PROMO_LABELS = {"CATEGORY_PROMOTIONS", "CATEGORY_FORUMS", "CATEGORY_SOCIAL"}

# Domains that should NEVER be auto-deleted (important senders)
PROTECTED_DOMAINS = {
    # Financial
    "bank", "paypal", "stripe", "razorpay", "paytm", "phonepe", 
    "amazon", "flipkart", "zerodha", "groww", "upstox",
    # Tech/Work
    "apple", "google", "microsoft", "zoom", "slack", "github",
    "atlassian", "notion", "figma",
    # Government/Education
    "gov.in", "gov", ".edu", "irs.gov", "uscis.gov", "nsdl", "epfo",
    # Travel
    "airline", "booking", "hotel", "uber", "lyft", "ola", "makemytrip",
    "goibibo", "cleartrip", "irctc",
    # Healthcare
    "healthcare", "hospital", "doctor", "medical", "practo", "1mg",
    # Utilities
    "electricity", "water", "gas", "telecom", "airtel", "jio", "vodafone"
}

# Keywords that indicate important emails
IMPORTANT_KEYWORDS = {
    "invoice", "receipt", "payment", "order", "confirmation", "booking",
    "ticket", "reservation", "appointment", "statement", "tax",
    "verification", "security", "alert", "urgent", "action required",
    "otp", "password", "reset", "delivery", "shipped", "refund"
}

def _sender_hash(sender: str) -> str:
    return hashlib.sha1(sender.lower().encode()).hexdigest()[:12]

def _heuristic(item):
    sender = item.get("from","").lower()
    subject = (item.get("subject") or "").lower()
    labels = set(item.get("labels") or [])
    size = item.get("size", 0)

    # SAFETY: Protected domains should NEVER be auto-deleted
    if any(domain in sender for domain in PROTECTED_DOMAINS):
        return "keep", 0.95
    
    # SAFETY: Important keywords in subject → always review
    if any(keyword in subject for keyword in IMPORTANT_KEYWORDS):
        return "review", 0.90  # High confidence - user should review
    
    # SAFETY: Emails in INBOX (not in promotions) → be conservative
    if "INBOX" in labels and not (labels & PROMO_LABELS):
        return "keep", 0.85

    # PRIMARY CLASSIFICATION: Trust Gmail's categories (most accurate)
    if labels & PROMO_LABELS:
        # Gmail already categorized as promotional/social/forums
        # Still check for important keywords even in promotions
        if any(keyword in subject for keyword in IMPORTANT_KEYWORDS):
            return "review", 0.80
        # Trust Gmail's categorization - safe to delete
        return "delete", 0.85  # Increased confidence (Gmail is accurate)

    # SECONDARY: Newsletter/marketing keywords (less reliable than Gmail)
    if any(h in sender or h in subject for h in BULK_HINTS):
        return "delete", 0.70

    # Large messages with attachments → review
    if size > 3_000_000:  # > ~3MB
        return "review", 0.75

    # Default: keep (be conservative)
    return "keep", 0.65

def classify_bulk(items: list[dict]):
    results = []
    counts = {"delete":0,"review":0,"keep":0}
    total_size = 0

    # First pass: heuristics
    for it in items:
        decision, conf = _heuristic(it)
        total_size += it.get("size",0)
        results.append({
            "id": it["id"],
            "sender_hash": _sender_hash(it.get("from","")),
            "subject": it.get("subject",""),
            "size": it.get("size",0),
            "decision": decision,
            "confidence": conf
        })
        counts[decision]+=1

    # Optional LLM pass for edge cases (keep it simple; upgrade later)
    # results = judge_edge_cases(results, items)  # uncomment after wiring model

    summary = {
        "total_items": len(items),
        "counts": counts,
        "approx_size_mb": round(total_size/1_000_000,2)
    }
    return {"items": results, "summary": summary}