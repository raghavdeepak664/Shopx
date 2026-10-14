"""
ShopX - E-Commerce Web Application (Amazon / Flipkart Inspired)
Flask Application Server
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, make_response
import database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

# Initialize database upon startup
with app.app_context():
    database.init_db()

@app.route("/")
def index():
    user_cookie = request.cookies.get("shopx_user_session")
    if not user_cookie:
        return redirect("/login")
    return render_template("index.html")

@app.route("/store")
def store_page():
    return render_template("index.html")

# API Endpoints
@app.route("/api/products", methods=["GET"])
def api_get_products():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    min_rating = request.args.get("min_rating", type=float)
    brand = request.args.get("brand", "").strip()
    assured_only = request.args.get("assured", "false").lower() == "true"
    deals_only = request.args.get("deals", "false").lower() == "true"
    sort_by = request.args.get("sort", "relevance")

    products = database.get_products(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        brand=brand,
        assured_only=assured_only,
        deals_only=deals_only,
        sort_by=sort_by
    )
    return jsonify({
        "success": True,
        "count": len(products),
        "products": products
    })

@app.route("/api/products/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    product = database.get_product(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404
    return jsonify({"success": True, "product": product})

@app.route("/api/categories", methods=["GET"])
def api_get_categories():
    categories = database.get_categories()
    return jsonify({"success": True, "categories": categories})

@app.route("/api/brands", methods=["GET"])
def api_get_brands():
    category = request.args.get("category", "")
    brands = database.get_brands(category)
    return jsonify({"success": True, "brands": brands})

@app.route("/api/coupon/validate", methods=["POST"])
def api_validate_coupon():
    data = request.get_json() or {}
    code = data.get("code", "").strip()
    order_amount = float(data.get("order_amount", 0))
    res = database.validate_coupon(code, order_amount)
    return jsonify(res)

@app.route("/api/orders", methods=["POST"])
def api_create_order():
    data = request.get_json() or {}
    if not data.get("items"):
        return jsonify({"success": False, "message": "Cart is empty"}), 400
    
    order_info = database.create_order(data)
    return jsonify({"success": True, "order": order_info})

@app.route("/api/orders", methods=["GET"])
def api_get_orders():
    orders = database.get_orders()
    return jsonify({"success": True, "orders": orders})

@app.route("/api/orders/<order_id>/track", methods=["GET"])
def api_track_order(order_id):
    tracking = database.get_order_tracking(order_id)
    if not tracking:
        return jsonify({"success": False, "message": "Order not found"}), 404
    return jsonify({"success": True, "order": tracking})

@app.route("/api/products/<int:product_id>/reviews", methods=["POST"])
def api_add_review(product_id):
    data = request.get_json() or {}
    author = data.get("author", "Verified Buyer")
    rating = int(data.get("rating", 5))
    title = data.get("title", "")
    comment = data.get("comment", "")

    if not comment:
        return jsonify({"success": False, "message": "Review comment cannot be empty"}), 400

    database.add_product_review(product_id, author, rating, title, comment)
    return jsonify({"success": True, "message": "Review submitted successfully!"})

# Authentication & User Tracking Routes
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie("shopx_user_session", "", expires=0, path="/")
    return resp

@app.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email_phone = data.get("email_phone", "").strip()
    password = data.get("password", "").strip()
    ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "Unknown Browser")

    if not name or not email_phone or not password:
        return jsonify({"success": False, "message": "Please fill all required fields."}), 400

    res = database.register_user(name, email_phone, password, ip_addr, user_agent)
    status_code = 200 if res.get("success") else 400
    resp = make_response(jsonify(res), status_code)
    if res.get("success"):
        session_info = json.dumps({"name": res.get("name", name), "email_phone": email_phone, "isLoggedIn": True})
        resp.set_cookie("shopx_user_session", session_info, max_age=60*60*24*30, path="/", samesite="Lax")
    return resp

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email_phone = data.get("email_phone", "").strip()
    password = data.get("password", "").strip()
    ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "Unknown Browser")

    if not email_phone or not password:
        return jsonify({"success": False, "message": "Please enter your email/phone and password."}), 400

    res = database.login_user(email_phone, password, ip_addr, user_agent)
    status_code = 200 if res.get("success") else 400
    resp = make_response(jsonify(res), status_code)
    if res.get("success"):
        session_info = json.dumps({"name": res.get("name", "Shopper"), "email_phone": res.get("email_phone", email_phone), "isLoggedIn": True})
        resp.set_cookie("shopx_user_session", session_info, max_age=60*60*24*30, path="/", samesite="Lax")
    return resp

# Real-time Cart Tracking Route (Logged to Excel)
@app.route("/api/track/cart", methods=["POST"])
def api_track_cart():
    data = request.get_json() or {}
    customer_name = data.get("customer_name", "Guest User")
    product_id = data.get("product_id")
    title = data.get("title", "Product")
    brand = data.get("brand", "")
    quantity = data.get("quantity", 1)
    price = data.get("price", 0)
    action = data.get("action", "ADDED")
    ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)

    database.track_cart_action(customer_name, product_id, title, brand, quantity, price, action, ip_addr)
    return jsonify({"success": True, "message": "Cart activity logged to Excel"})

# Protected Admin / Direct File Downloads
ADMIN_KEY = os.environ.get("ADMIN_KEY", "shopx_secure_admin_2026")

@app.route("/admin/export-excel")
def export_excel():
    if request.args.get("key") != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    import excel_logger
    from flask import send_file
    return send_file(excel_logger.EXCEL_FILE, as_attachment=True, download_name="shopx_user_data.xlsx")

@app.route("/admin/export-csv")
def export_csv():
    if request.args.get("key") != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    import excel_logger
    from flask import send_file
    return send_file(excel_logger.CSV_FILE, as_attachment=True, download_name="shopx_activity_log.csv")

@app.route("/admin")
def admin_page():
    if request.args.get("key") != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template("admin.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"=====================================================")
    print(f"  ShopX Server is running at http://127.0.0.1:{port}")
    print(f"=====================================================")
    app.run(host="0.0.0.0", port=port, debug=True)
