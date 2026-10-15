"""
ShopX Database Module
Handles SQLite initialization, product seeding, search, filtering, and order management.
"""

import sqlite3
import json
import os
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import excel_logger

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shopx.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        brand TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        original_price REAL NOT NULL,
        discount INTEGER NOT NULL,
        rating REAL NOT NULL,
        reviews_count INTEGER NOT NULL,
        image TEXT NOT NULL,
        additional_images TEXT NOT NULL,
        description TEXT NOT NULL,
        specs TEXT NOT NULL,
        in_stock INTEGER NOT NULL DEFAULT 1,
        is_bestseller INTEGER NOT NULL DEFAULT 0,
        is_deal INTEGER NOT NULL DEFAULT 0,
        is_assured INTEGER NOT NULL DEFAULT 1,
        fast_delivery INTEGER NOT NULL DEFAULT 1,
        deal_claimed_percent INTEGER DEFAULT 50,
        tags TEXT NOT NULL
    )
    """)

    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        customer_phone TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        pincode TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        items TEXT NOT NULL,
        subtotal REAL NOT NULL,
        discount REAL NOT NULL,
        delivery_fee REAL NOT NULL,
        coupon_applied TEXT,
        total REAL NOT NULL,
        status TEXT NOT NULL,
        expected_delivery TEXT NOT NULL
    )
    """)

    # Reviews table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        rating INTEGER NOT NULL,
        date TEXT NOT NULL,
        verified INTEGER DEFAULT 1,
        title TEXT NOT NULL,
        comment TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    # Coupons table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        code TEXT PRIMARY KEY,
        discount_type TEXT NOT NULL,
        value REAL NOT NULL,
        max_discount REAL,
        min_order REAL NOT NULL,
        description TEXT NOT NULL
    )
    """)

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email_phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    """)

    # User activity table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        user_name TEXT,
        email_phone TEXT,
        details TEXT,
        amount REAL,
        ip_address TEXT
    )
    """)

    # Contact inquiries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING'
    )
    """)

    # Ensure customer_email column exists on orders
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN customer_email TEXT")
    except Exception:
        pass

    conn.commit()

    # Re-sync products table with clean 40-item catalog & color variants
    cursor.execute("DELETE FROM products")
    seed_data(cursor)
    conn.commit()

    conn.close()

def seed_data(cursor):
    from static_data import DEFAULT_PRODUCTS
    products = DEFAULT_PRODUCTS

    for p in products:
        specs = p.get("specs", {}).copy()
        if "colors" in p:
            specs["colors"] = p["colors"]
        cursor.execute("""
        INSERT INTO products (
            id, title, brand, category, price, original_price, discount, rating,
            reviews_count, image, additional_images, description, specs,
            in_stock, is_bestseller, is_deal, is_assured, fast_delivery,
            deal_claimed_percent, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p.get("id"),
            p.get("title"),
            p.get("brand"),
            p.get("category"),
            p.get("price"),
            p.get("original_price"),
            p.get("discount"),
            p.get("rating"),
            p.get("reviews_count"),
            p.get("image"),
            json.dumps(p.get("additional_images", [p.get("image")])),
            p.get("description"),
            json.dumps(specs),
            1 if p.get("in_stock", True) else 0,
            1 if p.get("is_bestseller", False) else 0,
            1 if p.get("is_deal", False) else 0,
            1 if p.get("is_assured", True) else 0,
            1 if p.get("fast_delivery", True) else 0,
            p.get("deal_claimed_percent", random.randint(50, 95)),
            json.dumps(p.get("tags", []))
        ))

    # Seed Coupons (Updated: Removed ShopX Plus, added FESTIVE10)
    coupons = [
        ("SHOPX100", "fixed", 100, None, 500, "Flat ₹100 OFF on orders above ₹500"),
        ("FESTIVE20", "percent", 20, 1000, 1500, "20% OFF up to ₹1,000"),
        ("WELCOME50", "fixed", 50, None, 299, "Flat ₹50 OFF on first purchase"),
        ("FESTIVE10", "percent", 10, 500, 999, "10% OFF on all orders above ₹999")
    ]
    cursor.executemany("INSERT OR REPLACE INTO coupons VALUES (?, ?, ?, ?, ?, ?)", coupons)

    # Seed initial reviews
    sample_reviews = [
        (1, "Vikram Malhotra", 5, "2 days ago", 1, "Best iPhone ever! Titanium feel is incredible", "The weight reduction compared to the 14 Pro is noticeable immediately. The camera is pin sharp, battery lasts all day, and USB-C is finally here!"),
        (1, "Sneha Roy", 4, "1 week ago", 1, "Premium phone, smooth 120Hz", "Very happy with the purchase. Action button is super handy. Price is steep but trade-in made it reasonable."),
        (6, "Aditya Sharma", 5, "3 days ago", 1, "Unbeatable noise cancellation for flights & office", "The XM5 is astonishingly quiet. Multipoint connects seamlessly between my laptop and phone. Very comfortable headband."),
        (11, "Rahul Verma", 5, "Yesterday", 1, "Grail sneaker acquired!", "Authentic pair with ShopX Assured tag. The vintage cracked leather accents look phenomenal in person.")
    ]
    cursor.executemany("""
    INSERT INTO reviews (product_id, author, rating, date, verified, title, comment)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_reviews)

def get_products(query="", category="", min_price=None, max_price=None, min_rating=None, brand="", assured_only=False, deals_only=False, sort_by="relevance"):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if query:
        sql += " AND (title LIKE ? OR brand LIKE ? OR category LIKE ? OR tags LIKE ?)"
        q_wild = f"%{query}%"
        params.extend([q_wild, q_wild, q_wild, q_wild])

    if category and category != "All":
        sql += " AND category = ?"
        params.append(category)

    if min_price is not None:
        sql += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        sql += " AND price <= ?"
        params.append(max_price)

    if min_rating is not None and min_rating > 0:
        sql += " AND rating >= ?"
        params.append(min_rating)

    if brand:
        brands_list = [b.strip() for b in brand.split(",") if b.strip()]
        if brands_list:
            placeholders = ",".join(["?"] * len(brands_list))
            sql += f" AND brand IN ({placeholders})"
            params.extend(brands_list)

    if assured_only:
        sql += " AND is_assured = 1"

    if deals_only:
        sql += " AND is_deal = 1"

    # Sorting
    if sort_by == "price_asc":
        sql += " ORDER BY price ASC"
    elif sort_by == "price_desc":
        sql += " ORDER BY price DESC"
    elif sort_by == "rating":
        sql += " ORDER BY rating DESC, reviews_count DESC"
    elif sort_by == "discount":
        sql += " ORDER BY discount DESC"
    elif sort_by == "newest":
        sql += " ORDER BY id DESC"
    else:  # relevance
        sql += " ORDER BY is_bestseller DESC, is_deal DESC, rating DESC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    
    result = []
    for r in rows:
        d = dict(r)
        d["additional_images"] = json.loads(d["additional_images"]) if d["additional_images"] else []
        d["specs"] = json.loads(d["specs"]) if d["specs"] else {}
        d["colors"] = d["specs"].get("colors", [])
        d["tags"] = json.loads(d["tags"]) if d["tags"] else []
        d["in_stock"] = bool(d["in_stock"])
        d["is_bestseller"] = bool(d["is_bestseller"])
        d["is_deal"] = bool(d["is_deal"])
        d["is_assured"] = bool(d["is_assured"])
        d["fast_delivery"] = bool(d["fast_delivery"])
        result.append(d)

    conn.close()
    return result

def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    d = dict(row)
    d["additional_images"] = json.loads(d["additional_images"]) if d["additional_images"] else []
    d["specs"] = json.loads(d["specs"]) if d["specs"] else {}
    d["colors"] = d["specs"].get("colors", [])
    d["tags"] = json.loads(d["tags"]) if d["tags"] else []
    
    # Also fetch reviews
    cursor.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC", (product_id,))
    reviews = [dict(rev) for rev in cursor.fetchall()]
    d["reviews"] = reviews

    conn.close()
    return d

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) as count FROM products GROUP BY category ORDER BY count DESC")
    cats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cats

def get_brands(category=None):
    conn = get_connection()
    cursor = conn.cursor()
    if category and category != "All":
        cursor.execute("SELECT brand, COUNT(*) as count FROM products WHERE category = ? GROUP BY brand ORDER BY count DESC", (category,))
    else:
        cursor.execute("SELECT brand, COUNT(*) as count FROM products GROUP BY brand ORDER BY count DESC")
    brands = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return brands

def validate_coupon(code, order_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE UPPER(code) = UPPER(?)", (code,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"valid": False, "message": "Invalid coupon code"}
    coupon = dict(row)
    if order_amount < coupon["min_order"]:
        return {"valid": False, "message": f"Coupon valid only on orders above ₹{int(coupon['min_order'])}"}
    
    discount = 0
    if coupon["discount_type"] == "fixed":
        discount = coupon["value"]
    elif coupon["discount_type"] == "percent":
        discount = (order_amount * coupon["value"]) / 100
        if coupon["max_discount"] and discount > coupon["max_discount"]:
            discount = coupon["max_discount"]

    return {
        "valid": True,
        "code": coupon["code"],
        "discount": round(discount, 2),
        "description": coupon["description"],
        "message": f"Applied successfully! You saved ₹{int(discount)}"
    }

def create_order(order_data):
    conn = get_connection()
    cursor = conn.cursor()
    order_id = f"SX-{random.randint(100000, 999999)}-{random.randint(10, 99)}"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate estimated delivery date: 2 days from now
    from datetime import timedelta
    delivery_date = (datetime.now() + timedelta(days=2)).strftime("%A, %d %b %Y")

    customer_email = order_data.get("email") or order_data.get("customer_email") or ""

    cursor.execute("""
    INSERT INTO orders (
        order_id, created_at, customer_name, customer_email, customer_phone, address,
        city, pincode, payment_method, items, subtotal, discount,
        delivery_fee, coupon_applied, total, status, expected_delivery
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_id,
        created_at,
        order_data.get("name", "Customer"),
        customer_email,
        order_data.get("phone", "9876543210"),
        order_data.get("address", "Flat 402, Highline Residency"),
        order_data.get("city", "New Delhi"),
        order_data.get("pincode", "110001"),
        order_data.get("payment_method", "UPI"),
        json.dumps(order_data.get("items", [])),
        order_data.get("subtotal", 0),
        order_data.get("discount", 0),
        order_data.get("delivery_fee", 0),
        order_data.get("coupon_applied", ""),
        order_data.get("total", 0),
        "Order Confirmed",
        delivery_date
    ))
    conn.commit()
    conn.close()

    result = {
        "order_id": order_id,
        "status": "Order Confirmed",
        "created_at": created_at,
        "expected_delivery": delivery_date,
        "total": order_data.get("total", 0),
        "customer_email": customer_email
    }

    # Automatically save purchase data to Excel and CSV on user's PC!
    try:
        excel_logger.log_order_purchase({**order_data, **result})
    except Exception as e:
        print("Excel logging error:", e)

    return result

def save_contact_inquiry(name, email, subject, message):
    """Save customer or seller business inquiry and stream to Google Sheets."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO contact_inquiries (timestamp, name, email, subject, message, status)
    VALUES (?, ?, ?, ?, ?, 'NEW')
    """, (timestamp, name, email, subject, message))
    conn.commit()
    conn.close()

    # Log to Excel and Google Sheets live webhook
    try:
        excel_logger.log_event(
            event_type="CONTACT_INQUIRY",
            customer_name=name,
            email_phone=email,
            details=f"[{subject}] {message[:60]}",
            amount=0
        )
    except Exception as e:
        print("Error logging contact inquiry:", e)

    return {"success": True, "message": "Inquiry recorded successfully"}

def get_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = []
    for r in cursor.fetchall():
        d = dict(r)
        d["items"] = json.loads(d["items"])
        orders.append(d)
    conn.close()
    return orders

def get_order_tracking(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["items"] = json.loads(d["items"])
    
    # Generate timeline
    timeline = [
        {"step": "Order Placed", "status": "completed", "time": d["created_at"], "description": "We received your order and payment was verified."},
        {"step": "Order Packed", "status": "completed", "time": "ShopX Fulfillment Center, Warehouse 4", "description": "Seller has processed and securely packed your items."},
        {"step": "Shipped", "status": "in_progress", "time": "In Transit via ShopX Express", "description": "Package is on its way to the delivery hub near your pincode."},
        {"step": "Out for Delivery", "status": "upcoming", "time": "Pending local dispatch", "description": "Our courier partner will deliver today."},
        {"step": "Delivered", "status": "upcoming", "time": d["expected_delivery"], "description": "Package delivered to doorstep."}
    ]
    d["timeline"] = timeline
    return d

def register_user(name, email_phone, password, ip_address="127.0.0.1", user_agent=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email_phone = ?", (email_phone,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return {"success": False, "message": "An account with this email or mobile number already exists."}
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hashed_pwd = generate_password_hash(password)
    cursor.execute("""
    INSERT INTO users (name, email_phone, password, created_at, last_login)
    VALUES (?, ?, ?, ?, ?)
    """, (name, email_phone, hashed_pwd, created_at, created_at))
    conn.commit()
    conn.close()

    # Log event status (no plaintext passwords)
    try:
        excel_logger.log_login_or_signup("SIGNUP", name, email_phone, "SUCCESS", ip_address, user_agent)
    except Exception as e:
        print("Excel logging error:", e)

    return {"success": True, "name": name, "email_phone": email_phone, "message": "Account created successfully!"}

def login_user(email_phone, password, ip_address="127.0.0.1", user_agent=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email_phone = ?", (email_phone,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        try:
            excel_logger.log_event("LOGIN_FAILED", "Unknown", email_phone, "Account not found", 0, ip_address, user_agent)
        except Exception:
            pass
        return {"success": False, "message": "No account found with this email or mobile number."}
    
    user_dict = dict(user)
    # Support both hashed passwords and legacy plaintext
    stored_pwd = user_dict["password"]
    is_valid = False
    if stored_pwd.startswith("scrypt:") or stored_pwd.startswith("pbkdf2:"):
        is_valid = check_password_hash(stored_pwd, password)
    else:
        is_valid = (stored_pwd == password)

    if not is_valid:
        conn.close()
        try:
            excel_logger.log_event("LOGIN_FAILED", user_dict["name"], email_phone, "Incorrect password", 0, ip_address, user_agent)
        except Exception:
            pass
        return {"success": False, "message": "Incorrect password. Please try again."}

    # Update last login
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user_dict["id"]))
    conn.commit()
    conn.close()

    # Log event status
    try:
        excel_logger.log_login_or_signup("LOGIN", user_dict["name"], email_phone, "SUCCESS", ip_address, user_agent)
    except Exception as e:
        print("Excel logging error:", e)

    return {"success": True, "name": user_dict["name"], "email_phone": user_dict["email_phone"], "message": "Logged in successfully!"}

def track_cart_action(customer_name, product_id, title, brand, quantity, price, action="ADDED", ip_address="127.0.0.1"):
    try:
        excel_logger.log_cart_activity(customer_name, product_id, title, brand, quantity, price, action, ip_address)
    except Exception as e:
        print("Cart Excel log error:", e)
    return True

def add_product_review(product_id, author, rating, title, comment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO reviews (product_id, author, rating, date, verified, title, comment)
    VALUES (?, ?, ?, 'Just now', 1, ?, ?)
    """, (product_id, author, rating, title, comment))
    
    # Update product rating and reviews count
    cursor.execute("""
    SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?
    """, (product_id,))
    avg_rating, count = cursor.fetchone()
    if avg_rating:
        cursor.execute("UPDATE products SET rating = ?, reviews_count = reviews_count + 1 WHERE id = ?", (round(avg_rating, 1), product_id))
    
    conn.commit()
    conn.close()
    return True
