"""
ShopX Excel & CSV Activity Logger
Automatically records:
1. User Logins and Signups
2. Cart Additions and Updates
3. Purchases and Orders Placed (including Product URLs)
4. Seller Applications
5. Customer Inquiries (forwarded to shopx.customercare@gmail.com)
Saves everything in real-time to both:
- shopx_user_data.xlsx (Multi-sheet formatted Excel workbook)
- shopx_activity_log.csv (Easy import into Google Sheets / Excel)
And streams asynchronously to Google Sheets via serverless Webhook.
"""

import os
import csv
import threading
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "shopx_user_data.xlsx")
CSV_FILE = os.path.join(BASE_DIR, "shopx_activity_log.csv")

SUPPORT_EMAIL = "shopx.customercare@gmail.com"

# Google Sheets Live Webhook Integration
GOOGLE_SHEETS_WEBHOOK_URL = os.environ.get(
    "GOOGLE_SHEETS_WEBHOOK_URL",
    "https://script.google.com/macros/s/AKfycbw6ObP-H0k65oxelCijRkuoU96bCSVYZZQo70oqhAGXSaXIDJccHMs24rEo2vaNDfBoyw/exec"
)

def send_to_google_sheets_async(row_data, event_type="ACTIVITY"):
    """Send row to Google Sheets via webhook asynchronously in background thread."""
    if not GOOGLE_SHEETS_WEBHOOK_URL:
        return

    def _worker():
        try:
            import urllib.request
            import json
            payload = json.dumps({
                "row": row_data,
                "event_type": event_type,
                "support_email": SUPPORT_EMAIL,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }).encode("utf-8")
            req = urllib.request.Request(
                GOOGLE_SHEETS_WEBHOOK_URL,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                pass
        except Exception as e:
            # Silent fallback for offline / restricted environments
            pass

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

_lock = threading.Lock()

# Define headers for each sheet
SHEET_HEADERS = {
    "All Activity Stream": [
        "Timestamp", "Event Type", "Customer Name", "Email / Phone",
        "Item / Details", "Price / Amount (INR)", "IP Address", "Device / Browser"
    ],
    "Logins & Signups": [
        "Timestamp", "Action Type", "Name", "Email / Phone",
        "Status", "IP Address", "Device / Browser"
    ],
    "Cart Activity": [
        "Timestamp", "Customer Name", "Product ID", "Product Title",
        "Brand", "Quantity", "Price Each (INR)", "Total Price (INR)", "IP Address"
    ],
    "Orders & Purchases": [
        "Timestamp", "Order ID", "Customer Name", "Phone", "Email",
        "Delivery Address", "City", "Pincode", "Payment Method",
        "Items Count", "Items Summary", "Total Paid (INR)", "Status", "Product URL(s)"
    ],
    "Seller Applications": [
        "Timestamp", "Brand / Store Name", "Owner Name", "Business Email",
        "Phone Number", "Category", "City", "State", "GSTIN / PAN", "Status", "Forwarded To"
    ],
    "Customer Inquiries": [
        "Timestamp", "Customer Name", "Email", "Phone", "Subject",
        "Message", "Status", "Destination Support Mail"
    ]
}

def init_excel_workbook():
    """Create or update the Excel workbook ensuring all sheets exist with styled headers."""
    with _lock:
        wb = None
        if os.path.exists(EXCEL_FILE):
            try:
                wb = openpyxl.load_workbook(EXCEL_FILE)
            except Exception:
                wb = None

        if wb is None:
            wb = openpyxl.Workbook()
            if "Sheet" in wb.sheetnames:
                wb.remove(wb["Sheet"])

        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="131921", end_color="131921", fill_type="solid")
        thin_border = Border(
            left=Side(style='thin', color='D3D3D3'),
            right=Side(style='thin', color='D3D3D3'),
            top=Side(style='thin', color='D3D3D3'),
            bottom=Side(style='thin', color='D3D3D3')
        )

        for sheet_name, headers in SHEET_HEADERS.items():
            if sheet_name not in wb.sheetnames:
                ws = wb.create_sheet(title=sheet_name)
            else:
                ws = wb[sheet_name]
            
            # Sync header row with defined schema
            for col_idx, col_name in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_idx, value=col_name)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_border
            ws.row_dimensions[1].height = 26
            for col_idx, col_name in enumerate(headers, 1):
                col_letter = get_column_letter(col_idx)
                ws.column_dimensions[col_letter].width = max(len(col_name) + 6, 20)

        try:
            wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error initializing Excel workbook:", e)

        # Also initialize the unified CSV file
        if not os.path.exists(CSV_FILE):
            try:
                with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(SHEET_HEADERS["All Activity Stream"])
            except Exception as e:
                print("Error initializing CSV:", e)

def log_event(event_type, customer_name, email_phone, details, amount=0, ip_address="127.0.0.1", user_agent=""):
    """Append event to All Activity Stream sheet, CSV, and Google Sheets."""
    init_excel_workbook()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_data = [
        timestamp,
        event_type,
        customer_name or "Guest User",
        email_phone or "N/A",
        details or "",
        f"₹{amount:,.2f}" if isinstance(amount, (int, float)) and amount > 0 else (str(amount) if amount else "—"),
        ip_address or "127.0.0.1",
        user_agent or "Web Browser"
    ]

    with _lock:
        try:
            with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(row_data)
        except Exception as e:
            print("Error writing to CSV:", e)

        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            if "All Activity Stream" in wb.sheetnames:
                ws = wb["All Activity Stream"]
                ws.append(row_data)
                wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error logging activity to Excel:", e)

    send_to_google_sheets_async(row_data, event_type=event_type)

def log_login_or_signup(action_type, name, email_phone, status="SUCCESS", ip_address="127.0.0.1", user_agent=""):
    """Specific logger for Logins & Signups sheet."""
    init_excel_workbook()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_data = [
        timestamp,
        action_type,
        name,
        email_phone,
        status,
        ip_address,
        user_agent
    ]

    log_event(
        event_type=action_type,
        customer_name=name,
        email_phone=email_phone,
        details=f"User {action_type} - Status: {status}",
        amount=0,
        ip_address=ip_address,
        user_agent=user_agent
    )

    with _lock:
        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            if "Logins & Signups" in wb.sheetnames:
                ws = wb["Logins & Signups"]
                ws.append(row_data)
                wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error logging login to Excel:", e)

def log_cart_activity(customer_name, product_id, title, brand, quantity, price, action="ADDED", ip_address="127.0.0.1"):
    """Specific logger for Cart Activity sheet."""
    init_excel_workbook()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_price = (price or 0) * (quantity or 1)

    row_data = [
        timestamp,
        customer_name or "Guest",
        product_id,
        title,
        brand or "N/A",
        quantity,
        price,
        total_price,
        ip_address
    ]

    log_event(
        event_type="ADD_TO_CART",
        customer_name=customer_name,
        email_phone="",
        details=f"{action}: {title} (x{quantity})",
        amount=total_price,
        ip_address=ip_address
    )

    with _lock:
        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            if "Cart Activity" in wb.sheetnames:
                ws = wb["Cart Activity"]
                ws.append(row_data)
                wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error logging cart to Excel:", e)

def log_order_purchase(order_dict, ip_address="127.0.0.1"):
    """Specific logger for Orders & Purchases sheet, storing product URLs."""
    init_excel_workbook()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    items = order_dict.get("items", [])
    items_count = sum(i.get("quantity", 1) for i in items)
    items_summary = "; ".join([f"{i.get('title', 'Item')[:25]} (x{i.get('quantity', 1)})" for i in items])
    
    # Generate direct product URLs for each item
    base_url = "https://shopx-ecommerce.onrender.com"
    product_urls_list = []
    for item in items:
        pid = item.get("id") or item.get("product_id") or 1
        p_title = item.get("title", "Product")[:20]
        product_urls_list.append(f"{base_url}/store?product={pid}")
    product_urls_str = " | ".join(product_urls_list)

    customer_email = order_dict.get("email") or order_dict.get("customer_email") or "N/A"
    customer_phone = order_dict.get("phone") or order_dict.get("customer_phone") or "N/A"

    row_data = [
        timestamp,
        order_dict.get("order_id", "N/A"),
        order_dict.get("name") or order_dict.get("customer_name") or "Customer",
        customer_phone,
        customer_email,
        order_dict.get("address", "N/A"),
        order_dict.get("city", "N/A"),
        order_dict.get("pincode", "N/A"),
        order_dict.get("payment_method", "UPI"),
        items_count,
        items_summary,
        order_dict.get("total", 0),
        order_dict.get("status", "Order Confirmed"),
        product_urls_str
    ]

    log_event(
        event_type="ORDER_PLACED",
        customer_name=order_dict.get("name") or order_dict.get("customer_name"),
        email_phone=f"{customer_email} | {customer_phone}",
        details=f"Order {order_dict.get('order_id')}: {items_summary} | URLs: {product_urls_str}",
        amount=order_dict.get("total", 0),
        ip_address=ip_address
    )

    with _lock:
        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            if "Orders & Purchases" in wb.sheetnames:
                ws = wb["Orders & Purchases"]
                ws.append(row_data)
                wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error logging order to Excel:", e)

    # Stream to Google Sheets with product URLs
    send_to_google_sheets_async(row_data, event_type="ORDER_PURCHASE")

def log_seller_application(seller_dict, ip_address="127.0.0.1"):
    """Specific logger for Seller Applications sheet."""
    init_excel_workbook()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_data = [
        timestamp,
        seller_dict.get("brand_name", "N/A"),
        seller_dict.get("owner_name", "N/A"),
        seller_dict.get("email", "N/A"),
        seller_dict.get("phone", "N/A"),
        seller_dict.get("category", "General"),
        seller_dict.get("city", "N/A"),
        seller_dict.get("state", "N/A"),
        seller_dict.get("gstin", "N/A"),
        "PENDING_REVIEW",
        SUPPORT_EMAIL
    ]

    log_event(
        event_type="SELLER_APPLICATION",
        customer_name=seller_dict.get("owner_name"),
        email_phone=f"{seller_dict.get('email')} | {seller_dict.get('phone')}",
        details=f"New Seller: {seller_dict.get('brand_name')} ({seller_dict.get('category')}) - Forwarded to {SUPPORT_EMAIL}",
        amount=0,
        ip_address=ip_address
    )

    with _lock:
        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            if "Seller Applications" in wb.sheetnames:
                ws = wb["Seller Applications"]
                ws.append(row_data)
                wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error logging seller to Excel:", e)

    send_to_google_sheets_async(row_data, event_type="SELLER_APPLICATION")

def log_customer_inquiry(inquiry_dict, ip_address="127.0.0.1"):
    """Specific logger for Customer Inquiries sheet."""
    init_excel_workbook()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_data = [
        timestamp,
        inquiry_dict.get("name", "Customer"),
        inquiry_dict.get("email", "N/A"),
        inquiry_dict.get("phone", "N/A"),
        inquiry_dict.get("subject", "General Inquiry"),
        inquiry_dict.get("message", ""),
        "PENDING",
        SUPPORT_EMAIL
    ]

    log_event(
        event_type="CUSTOMER_INQUIRY",
        customer_name=inquiry_dict.get("name"),
        email_phone=f"{inquiry_dict.get('email')} | {inquiry_dict.get('phone')}",
        details=f"[{inquiry_dict.get('subject')}] {inquiry_dict.get('message')[:80]} - Sent to {SUPPORT_EMAIL}",
        amount=0,
        ip_address=ip_address
    )

    with _lock:
        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            if "Customer Inquiries" in wb.sheetnames:
                ws = wb["Customer Inquiries"]
                ws.append(row_data)
                wb.save(EXCEL_FILE)
        except Exception as e:
            print("Error logging inquiry to Excel:", e)

    send_to_google_sheets_async(row_data, event_type="CUSTOMER_INQUIRY")

# Initialize on module import
init_excel_workbook()
