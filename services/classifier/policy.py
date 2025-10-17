import hashlib
from .llm_adapter import judge_edge_cases

BULK_HINTS = ("unsubscribe", "no-reply", "noreply", "newsletter")
PROMO_LABELS = {"CATEGORY_PROMOTIONS", "CATEGORY_FORUMS", "CATEGORY_SOCIAL"}

def _sender_hash(sender: str) -> str:
    return hashlib.sha1(sender.lower().encode()).hexdigest()[:12]

def _heuristic(item):
    sender = item.get("from","").lower()
    subject = (item.get("subject") or "").lower()
    labels = set(item.get("labels") or [])
    size = item.get("size", 0)

    # promotional/social labels → likely delete if older than ~90d (we don’t parse date here in MVP)
    if labels & PROMO_LABELS:
        return "delete", 0.9

    # bulky newsletters
    if any(h in sender or h in subject for h in BULK_HINTS):
        return "delete", 0.85

    # very large messages (likely attachments) → review
    if size > 3_000_000:  # > ~3MB
        return "review", 0.7

    return "keep", 0.6

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