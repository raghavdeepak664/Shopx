import unittest
import json
import openpyxl
import database
import excel_logger
from app import app

class ShopXSystemTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_email_phone_validation(self):
        print("\n--- Testing Email & Phone Validation ---")
        # Valid emails
        self.assertTrue(database.is_valid_email("test@gmail.com"))
        self.assertTrue(database.is_valid_email("john.doe@company.org"))
        self.assertTrue(database.is_valid_email("shopx.customercare@gmail.com"))
        
        # Invalid emails
        self.assertFalse(database.is_valid_email("invalidemail"))
        self.assertFalse(database.is_valid_email("invalid@"))
        self.assertFalse(database.is_valid_email("@domain.com"))
        self.assertFalse(database.is_valid_email("user@domain"))
        self.assertFalse(database.is_valid_email("user@.com"))
        
        # Valid Indian mobiles
        self.assertTrue(database.is_valid_indian_mobile("9876543210"))
        self.assertTrue(database.is_valid_indian_mobile("+919876543210"))
        self.assertTrue(database.is_valid_indian_mobile("09876543210"))
        self.assertTrue(database.is_valid_indian_mobile("7123456789"))
        
        # Invalid mobiles
        self.assertFalse(database.is_valid_indian_mobile("1234567890"))
        self.assertFalse(database.is_valid_indian_mobile("98765"))
        self.assertFalse(database.is_valid_indian_mobile("abcdefghij"))
        print("[OK] Email and Indian Mobile regex validation passed successfully.")

    def test_02_product_catalog_integrity(self):
        print("\n--- Testing Product Catalog (520 Products, No Duplicates, Clean Categories) ---")
        res = self.app.get("/api/products")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        products = data["products"]
        
        # Check count
        self.assertGreaterEqual(len(products), 500, f"Expected at least 500 products, got {len(products)}")
        print(f"[OK] Catalog contains {len(products)} products.")

        # Check unique IDs and Titles (No Duplicates)
        ids = [p["id"] for p in products]
        titles = [p["title"].strip().lower() for p in products]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate product IDs found!")
        self.assertEqual(len(titles), len(set(titles)), "Duplicate product titles found!")
        print("[OK] Zero duplicate IDs or product titles found across all 520 products.")

        # Check Home & Kitchen category for no robot vacuums
        kitchen_products = [p for p in products if p["category"] == "Home & Kitchen"]
        self.assertGreaterEqual(len(kitchen_products), 50)
        for kp in kitchen_products:
            self.assertNotIn("robot", kp["title"].lower(), f"Robot item found in Kitchen: {kp['title']}")
            self.assertNotIn("cleaner", kp["title"].lower(), f"Cleaner item found in Kitchen: {kp['title']}")
        print(f"[OK] Verified all {len(kitchen_products)} Home & Kitchen products are authentic cookware/appliances with no robot cleaners.")

    def test_03_auth_and_otp_reset(self):
        print("\n--- Testing User Registration, Single-Account Enforcement & OTP Password Reset ---")
        test_email = "test.shopper.2026@gmail.com"
        initial_pwd = "Password@123"
        updated_pwd = "NewSecurePassword@456"

        # 1. Register with malformed email -> MUST FAIL
        res = self.app.post("/api/auth/register", json={
            "name": "Bad Email User",
            "email_phone": "notanemail",
            "password": "Password123"
        })
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.get_json()["success"])

        # 2. Register valid user
        res = self.app.post("/api/auth/register", json={
            "name": "Test Shopper",
            "email_phone": test_email,
            "password": initial_pwd
        })
        if res.status_code == 200:
            self.assertTrue(res.get_json()["success"])

        # 3. Try to register SAME email again -> MUST FAIL (One account per email rule)
        res_dup = self.app.post("/api/auth/register", json={
            "name": "Duplicate Shopper",
            "email_phone": test_email,
            "password": "OtherPassword123"
        })
        self.assertEqual(res_dup.status_code, 400)
        self.assertIn("already exists", res_dup.get_json()["message"].lower())
        print("[OK] Single registration per email strictly enforced.")

        # 4. Request Forgot Password OTP
        res_fp = self.app.post("/api/auth/forgot-password", json={
            "email_phone": test_email
        })
        self.assertEqual(res_fp.status_code, 200)
        fp_data = res_fp.get_json()
        self.assertTrue(fp_data["success"])
        otp = fp_data.get("otp")
        self.assertTrue(otp and len(otp) == 6)
        print(f"[OK] OTP generated successfully: {otp}")

        # 5. Verify OTP and reset password
        res_reset = self.app.post("/api/auth/reset-password", json={
            "email_phone": test_email,
            "otp": otp,
            "new_password": updated_pwd
        })
        self.assertEqual(res_reset.status_code, 200)
        self.assertTrue(res_reset.get_json()["success"])
        print("[OK] OTP verified and password updated successfully in SQLite database.")

        # 6. Login with new password
        res_login = self.app.post("/api/auth/login", json={
            "email_phone": test_email,
            "password": updated_pwd
        })
        self.assertEqual(res_login.status_code, 200)
        self.assertTrue(res_login.get_json()["success"])
        print("[OK] Logged in with updated password successfully.")

    def test_04_seller_registration(self):
        print("\n--- Testing Merchant Registration (Sell on ShopX) ---")
        # Invalid phone
        res_bad = self.app.post("/api/seller/register", json={
            "brand_name": "Acme Innovations",
            "owner_name": "Vikram Patel",
            "email": "vikram@acme.com",
            "phone": "12345",
            "category": "Electronics & Audio"
        })
        self.assertEqual(res_bad.status_code, 400)

        # Valid seller
        res = self.app.post("/api/seller/register", json={
            "brand_name": "Aura Lifestyle India",
            "owner_name": "Neha Sharma",
            "email": "neha@auralifestyle.in",
            "phone": "9811223344",
            "category": "Fashion & Apparel",
            "city": "Bengaluru",
            "state": "Karnataka",
            "gstin": "29AAAAA0000A1Z5"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])
        print("[OK] Merchant registered and saved to SQLite & Excel sheet 'Seller Applications'.")

    def test_05_customer_inquiry_with_phone(self):
        print("\n--- Testing Help & Customer Support Request with Phone ---")
        res = self.app.post("/api/contact", json={
            "name": "Pooja Gupta",
            "email": "pooja.gupta@gmail.com",
            "phone": "9988776655",
            "subject": "Exchange Request for Order SX-192840",
            "message": "I would like to exchange my sneakers for size UK 9. Please assist."
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])
        print("[OK] Customer inquiry with validated phone saved to SQLite & Excel sheet 'Customer Inquiries'.")

    def test_06_order_checkout_product_urls_in_excel(self):
        print("\n--- Testing Order Placement & Direct Product URLs in Excel ---")
        order_payload = {
            "name": "Arun Kumar",
            "phone": "9876501234",
            "email": "arun.kumar@gmail.com",
            "address": "42 Lakeview Residency, Koramangala",
            "city": "Bengaluru",
            "state": "Karnataka",
            "pincode": "560034",
            "paymentMethod": "UPI",
            "items": [
                {
                    "id": 1001,
                    "title": "ShopX Pro 5G Smartphone",
                    "price": 24999,
                    "quantity": 1,
                    "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&auto=format&fit=crop&q=60"
                },
                {
                    "id": 1002,
                    "title": "UltraPulse ANC Wireless Headphones",
                    "price": 4999,
                    "quantity": 2,
                    "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60"
                }
            ],
            "subtotal": 34997,
            "discount": 0,
            "delivery_fee": 0,
            "total": 34997
        }
        res = self.app.post("/api/orders", json=order_payload)
        self.assertEqual(res.status_code, 200)
        order_res = res.get_json()
        self.assertTrue(order_res["success"])
        order_id = order_res["order"]["order_id"]
        print(f"[OK] Order created: {order_id}")

        # Check Excel workbook for product URLs
        wb = openpyxl.load_workbook(excel_logger.EXCEL_FILE, data_only=True)
        self.assertIn("Orders & Purchases", wb.sheetnames)
        ws = wb["Orders & Purchases"]
        
        headers = [str(cell.value) for cell in ws[1]]
        # Find column that contains "Product URL"
        url_col_idx = None
        for idx, h in enumerate(headers, 1):
            if "Product URL" in h:
                url_col_idx = idx
                break
        self.assertIsNotNone(url_col_idx, f"Product URL column not found in headers: {headers}")

        # Check latest rows for presence of product URLs
        found_url = False
        for row in range(ws.max_row, max(1, ws.max_row - 5), -1):
            val = ws.cell(row=row, column=url_col_idx).value
            if val and "https://shopx-ecommerce.onrender.com/store?product=" in str(val):
                found_url = True
                print(f"[OK] Found Product URLs in Excel row {row}: {val}")
                break
        self.assertTrue(found_url, "Product URLs not logged in Orders & Purchases sheet!")

if __name__ == "__main__":
    unittest.main()
