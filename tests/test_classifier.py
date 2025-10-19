"""
Unit tests for email classification logic
"""

import pytest
from services.classifier.policy import classify_bulk, _heuristic

class TestHeuristic:
    """Test individual heuristic classification"""
    
    def test_protected_domain_bank(self):
        """Bank emails should always be kept"""
        email = {
            "from": "alerts@chase.com",
            "subject": "Your account statement",
            "labels": ["INBOX"],
            "size": 50000
        }
        decision, confidence = _heuristic(email)
        assert decision == "keep"
        assert confidence >= 0.9
    
    def test_protected_domain_government(self):
        """Government emails should be kept"""
        email = {
            "from": "noreply@irs.gov",
            "subject": "Tax notice",
            "labels": ["INBOX"],
            "size": 30000
        }
        decision, confidence = _heuristic(email)
        assert decision == "keep"
        assert confidence >= 0.9
    
    def test_protected_domain_indian_services(self):
        """Indian service emails should be kept"""
        email = {
            "from": "alerts@zerodha.com",
            "subject": "Trade confirmation",
            "labels": ["INBOX"],
            "size": 20000
        }
        decision, confidence = _heuristic(email)
        assert decision == "keep"
        assert confidence >= 0.9
    
    def test_important_keyword_receipt(self):
        """Emails with 'receipt' should be reviewed"""
        email = {
            "from": "store@example.com",
            "subject": "Your receipt for order #12345",
            "labels": ["INBOX"],
            "size": 15000
        }
        decision, confidence = _heuristic(email)
        assert decision == "review"
        assert confidence >= 0.8
    
    def test_important_keyword_otp(self):
        """OTP emails should be reviewed"""
        email = {
            "from": "noreply@service.com",
            "subject": "Your OTP is 123456",
            "labels": ["INBOX"],
            "size": 5000
        }
        decision, confidence = _heuristic(email)
        assert decision == "review"
        assert confidence >= 0.8
    
    def test_promotional_label(self):
        """Gmail promotional category should be deleted"""
        email = {
            "from": "marketing@store.com",
            "subject": "50% off sale this weekend!",
            "labels": ["CATEGORY_PROMOTIONS"],
            "size": 100000
        }
        decision, confidence = _heuristic(email)
        assert decision == "delete"
        assert confidence >= 0.7
    
    def test_promotional_with_important_keyword(self):
        """Promotional email with important keyword should be reviewed"""
        email = {
            "from": "marketing@store.com",
            "subject": "Your order receipt - 50% off!",
            "labels": ["CATEGORY_PROMOTIONS"],
            "size": 50000
        }
        decision, confidence = _heuristic(email)
        assert decision == "review"
        assert confidence >= 0.7
    
    def test_social_label(self):
        """Gmail social category should be deleted"""
        email = {
            "from": "notifications@linkedin.com",
            "subject": "You have 5 new connections",
            "labels": ["CATEGORY_SOCIAL"],
            "size": 80000
        }
        decision, confidence = _heuristic(email)
        assert decision == "delete"
        assert confidence >= 0.7
    
    def test_newsletter_keywords(self):
        """Newsletter emails should be deleted"""
        email = {
            "from": "newsletter@techblog.com",
            "subject": "Weekly newsletter - Top 10 articles",
            "labels": ["INBOX"],
            "size": 120000
        }
        decision, confidence = _heuristic(email)
        assert decision == "delete"
        assert confidence >= 0.6
    
    def test_inbox_without_promo_labels(self):
        """Regular inbox emails should be kept"""
        email = {
            "from": "friend@gmail.com",
            "subject": "Hey, how are you?",
            "labels": ["INBOX"],
            "size": 10000
        }
        decision, confidence = _heuristic(email)
        assert decision == "keep"
        assert confidence >= 0.6
    
    def test_large_email(self):
        """Very large emails should be reviewed"""
        email = {
            "from": "sender@example.com",
            "subject": "Important document attached",
            "labels": ["INBOX"],
            "size": 5000000  # 5MB
        }
        decision, confidence = _heuristic(email)
        assert decision == "review"
        assert confidence >= 0.6


class TestClassifyBulk:
    """Test bulk classification"""
    
    def test_empty_list(self):
        """Empty email list should return empty results"""
        result = classify_bulk([])
        assert result["summary"]["total_items"] == 0
        assert result["summary"]["counts"]["delete"] == 0
        assert result["summary"]["counts"]["review"] == 0
        assert result["summary"]["counts"]["keep"] == 0
    
    def test_single_email(self):
        """Single email classification"""
        emails = [{
            "id": "msg_1",
            "from": "marketing@store.com",
            "subject": "Sale alert!",
            "labels": ["CATEGORY_PROMOTIONS"],
            "size": 50000
        }]
        result = classify_bulk(emails)
        assert result["summary"]["total_items"] == 1
        assert result["summary"]["counts"]["delete"] == 1
    
    def test_mixed_emails(self):
        """Mix of delete, review, and keep emails"""
        emails = [
            {
                "id": "msg_1",
                "from": "marketing@store.com",
                "subject": "Sale!",
                "labels": ["CATEGORY_PROMOTIONS"],
                "size": 50000
            },
            {
                "id": "msg_2",
                "from": "alerts@chase.com",
                "subject": "Account alert",
                "labels": ["INBOX"],
                "size": 30000
            },
            {
                "id": "msg_3",
                "from": "store@example.com",
                "subject": "Your receipt",
                "labels": ["INBOX"],
                "size": 20000
            }
        ]
        result = classify_bulk(emails)
        assert result["summary"]["total_items"] == 3
        assert result["summary"]["counts"]["delete"] == 1
        assert result["summary"]["counts"]["keep"] == 1
        assert result["summary"]["counts"]["review"] == 1
    
    def test_size_calculation(self):
        """Test size calculation in MB"""
        emails = [
            {
                "id": "msg_1",
                "from": "marketing@store.com",
                "subject": "Sale!",
                "labels": ["CATEGORY_PROMOTIONS"],
                "size": 1048576  # 1MB
            },
            {
                "id": "msg_2",
                "from": "newsletter@blog.com",
                "subject": "Weekly update",
                "labels": ["CATEGORY_PROMOTIONS"],
                "size": 2097152  # 2MB
            }
        ]
        result = classify_bulk(emails)
        # Should be approximately 3MB
        assert result["summary"]["approx_size_mb"] >= 2.9
        assert result["summary"]["approx_size_mb"] <= 3.1
    
    def test_items_structure(self):
        """Test that items have correct structure"""
        emails = [{
            "id": "msg_1",
            "from": "marketing@store.com",
            "subject": "Sale!",
            "labels": ["CATEGORY_PROMOTIONS"],
            "size": 50000
        }]
        result = classify_bulk(emails)
        
        assert "items" in result
        assert len(result["items"]) == 1
        
        item = result["items"][0]
        assert "id" in item
        assert "decision" in item
        assert "confidence" in item
        assert item["decision"] in ["delete", "review", "keep"]
        assert 0 <= item["confidence"] <= 100


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_fields(self):
        """Email with missing fields should not crash"""
        email = {
            "id": "msg_1",
            "from": "",
            "subject": None,
            "labels": None,
            "size": 0
        }
        decision, confidence = _heuristic(email)
        # Should default to keep with low confidence
        assert decision == "keep"
    
    def test_malformed_sender(self):
        """Malformed sender email should be handled"""
        email = {
            "from": "not-an-email",
            "subject": "Test",
            "labels": ["INBOX"],
            "size": 1000
        }
        decision, confidence = _heuristic(email)
        assert decision in ["delete", "review", "keep"]
    
    def test_very_large_batch(self):
        """Large batch of emails should be processed"""
        emails = [
            {
                "id": f"msg_{i}",
                "from": "sender@example.com",
                "subject": f"Email {i}",
                "labels": ["INBOX"],
                "size": 10000
            }
            for i in range(1000)
        ]
        result = classify_bulk(emails)
        assert result["summary"]["total_items"] == 1000


class TestProtectedDomains:
    """Test all protected domain categories"""
    
    @pytest.mark.parametrize("domain", [
        "chase.com", "bankofamerica.com", "wellsfargo.com",
        "paypal.com", "stripe.com", "razorpay.com", "paytm.com"
    ])
    def test_financial_domains(self, domain):
        """All financial domains should be protected"""
        email = {
            "from": f"noreply@{domain}",
            "subject": "Account notification",
            "labels": ["INBOX"],
            "size": 10000
        }
        decision, _ = _heuristic(email)
        assert decision == "keep"
    
    @pytest.mark.parametrize("domain", [
        "irs.gov", "uscis.gov", "nsdl.com", "epfindia.gov.in"
    ])
    def test_government_domains(self, domain):
        """All government domains should be protected"""
        email = {
            "from": f"noreply@{domain}",
            "subject": "Official notice",
            "labels": ["INBOX"],
            "size": 10000
        }
        decision, _ = _heuristic(email)
        assert decision == "keep"
    
    @pytest.mark.parametrize("domain", [
        "zerodha.com", "groww.in", "upstox.com", "makemytrip.com", "irctc.co.in"
    ])
    def test_indian_services(self, domain):
        """Indian service domains should be protected"""
        email = {
            "from": f"alerts@{domain}",
            "subject": "Service notification",
            "labels": ["INBOX"],
            "size": 10000
        }
        decision, _ = _heuristic(email)
        assert decision == "keep"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
