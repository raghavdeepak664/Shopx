"""
Unit and Integration Tests for the 4 User-Reported Fixes:
1. Customer care and seller inquiries dispatched to shopx.customercare@gmail.com
2. Flexible login via email, mobile (with/without +91), and username
3. Forgot password OTP delivery (Email dispatch + Interactive SMS alert)
4. Product image matching accuracy
"""

import unittest
import json
import sqlite3
import mail_service
import database
import app as flask_app

class TestFourFixes(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.app.test_client()
        self.app.testing = True
        conn = sqlite3.connect("shopx.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = 'Deepak123' WHERE email_phone = '9876543210'")
        conn.commit()
        conn.close()

    def test_1_support_and_seller_email_dispatch(self):
        """Fix 1: Customer inquiries and seller inquiries are sent to shopx.customercare@gmail.com."""
        # 1. Contact inquiry
        res = self.app.post("/api/contact", json={
            "name": "Aman Sharma",
            "email": "aman.sharma@example.com",
            "phone": "9811223344",
            "subject": "Delivery Delayed",
            "message": "When will my package arrive at Hub 4?"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("shopx.customercare@gmail.com", data["message"])

        # 2. Seller application
        res_seller = self.app.post("/api/seller/register", json={
            "brand_name": "Artisan Craft Studio",
            "owner_name": "Pooja Gupta",
            "email": "pooja@artisancraft.com",
            "phone": "9876501234",
            "category": "Home & Kitchen",
            "city": "Jaipur",
            "state": "Rajasthan",
            "gstin": "08AAAAA0000A1Z5"
        })
        self.assertEqual(res_seller.status_code, 200)
        s_data = res_seller.get_json()
        self.assertTrue(s_data["success"])

        # Verify notifications recorded in outbox
        outbox = mail_service.get_recent_outbox(20)
        self.assertGreater(len(outbox), 0)
        # Check that shopx.customercare@gmail.com is in outbox recipients
        recipients = [m["to"] for m in outbox]
        self.assertIn("shopx.customercare@gmail.com", recipients)

    def test_2_flexible_login(self):
        """Fix 2: Login works with email, phone with country code, plain 10-digit phone, and username."""
        # 1. Login with plain 10-digit mobile
        res1 = self.app.post("/api/auth/login", json={
            "email_phone": "9876543210",
            "password": "Deepak123"
        })
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(res1.get_json()["success"])

        # 2. Login with phone having country code +91
        res2 = self.app.post("/api/auth/login", json={
            "email_phone": "+919876543210",
            "password": "Deepak123"
        })
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(res2.get_json()["success"])

        # 3. Login with email
        res3 = self.app.post("/api/auth/login", json={
            "email_phone": "raghavdeepak664@gmail.com",
            "password": "Deepak123"
        })
        self.assertEqual(res3.status_code, 200)
        self.assertTrue(res3.get_json()["success"])

        # 4. Login with username
        res4 = self.app.post("/api/auth/login", json={
            "email_phone": "Deepak Raghav",
            "password": "Deepak123"
        })
        self.assertEqual(res4.status_code, 200)
        self.assertTrue(res4.get_json()["success"])

    def test_3_forgot_password_otp_delivery(self):
        """Fix 3: OTP is generated and delivered for both mobile and email."""
        # 1. Mobile OTP
        res_mobile = self.app.post("/api/auth/forgot-password", json={
            "email_phone": "+919876543210"
        })
        self.assertEqual(res_mobile.status_code, 200)
        m_data = res_mobile.get_json()
        self.assertTrue(m_data["success"])
        self.assertTrue(m_data["is_sms"])
        self.assertEqual(len(m_data["otp"]), 6)

        # 2. Email OTP
        res_email = self.app.post("/api/auth/forgot-password", json={
            "email_phone": "raghavdeepak664@gmail.com"
        })
        self.assertEqual(res_email.status_code, 200)
        e_data = res_email.get_json()
        self.assertTrue(e_data["success"])
        self.assertFalse(e_data["is_sms"])
        self.assertEqual(len(e_data["otp"]), 6)

        # 3. Verify OTP reset works
        res_reset = self.app.post("/api/auth/reset-password", json={
            "email_phone": "+919876543210",
            "otp": m_data["otp"],
            "new_password": "VerifiedPass2026"
        })
        self.assertEqual(res_reset.status_code, 200)
        self.assertTrue(res_reset.get_json()["success"])

    def test_4_product_images_match_names(self):
        """Fix 4: Product imagery strictly matches product titles."""
        conn = sqlite3.connect("shopx.db")
        cur = conn.cursor()
        cur.execute("SELECT id, title, category, image FROM products")
        products = cur.fetchall()
        conn.close()

        self.assertEqual(len(products), 520)

        # Verify key semantic associations
        for p_id, title, cat, img in products:
            t = title.lower()
            if "mouse" in t:
                self.assertTrue("photo-1615663245857" in img or "photo-1527864550417" in img, f"Mouse image mismatch for {title}: {img}")
            elif "keyboard" in t:
                self.assertTrue("photo-1587829741301" in img or "photo-1618384887929" in img, f"Keyboard image mismatch for {title}: {img}")
            elif "monitor" in t and "headphone" not in t:
                self.assertTrue("photo-1527443224154" in img or "photo-1547119957-637f8679db1e" in img, f"Monitor image mismatch for {title}: {img}")
            elif "drone" in t:
                self.assertTrue("photo-1507582020474" in img or "photo-1527977966376" in img, f"Drone image mismatch for {title}: {img}")
            elif "airpods" in t or "earbuds" in t:
                self.assertTrue("photo-1600294037681" in img or "photo-1590658268037" in img or "photo-1572569511254" in img, f"Earbuds image mismatch for {title}: {img}")
            elif "coffee" in t:
                self.assertTrue("photo-1517668808822" in img or "photo-1514432324607" in img, f"Coffee maker image mismatch for {title}: {img}")

if __name__ == "__main__":
    unittest.main()
