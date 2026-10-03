# ShopX 🛍️ - Next-Gen E-Commerce Platform

A feature-packed, high-performance e-commerce web application inspired by **Amazon** and **Flipkart**.

Built with a responsive, modern design system, interactive product catalogs, real-time search autocomplete, smart filters, sliding shopping cart, checkout flow with confetti celebration, order tracking stepper, and SQLite/REST backend.

---

## ✨ Key Features

### 1. 🔍 Amazon & Flipkart Inspired Header & Navigation
- **ShopX Brand Identity**: Custom logo with "Plus ⚡" tag.
- **Delivery Pincode / Location Selector**: Choose your pincode (e.g. `110001 - New Delhi`) with instant city detection.
- **Smart Search Bar**:
  - Live category selector dropdown.
  - Real-time instant autocomplete dropdown with product thumbnails, highlighted match keywords, and price previews.
  - Clear button and keyboard search handling.
- **Wishlist & Returns/Orders Modal Trigger**: Access saved items and order tracking with 1 click.
- **Dynamic Cart Button**: Live bouncy counter badge showing real-time item counts.
- **Dark Mode / Light Mode**: Instant smooth theme toggling with localStorage persistence.
- **Secondary Ribbon**: Quick shortcuts to Deals, Mobiles, Laptops, Audio, Fashion, Sneakers, and ShopX Plus.

### 2. ⚡ Lightning Deals & Hero Promotions
- **Hero Promotional Banner Carousel**: 3 high-impact sale banners with auto-sliding, dot indicators, and previous/next controls.
- **Lightning Deals Bar**:
  - Real-time ticking countdown timer (`03h : 42m : 19s`).
  - Deal progress meter (`78% Claimed`).
  - Discount tags up to 74% off with original MRP strikethrough.

### 3. 🎯 Full Catalog Filtering & Sorting
- **Categories Strip**: Circular icon pills with active highlights and product counters.
- **Sidebar Filters**:
  - **ShopX Assured / Prime toggle switch**.
  - **Category filter** with live count tags.
  - **Dual price range slider** with min/max manual inputs.
  - **Brand filter checkboxes** (Apple, Samsung, Sony, Nike, Adidas, Philips, etc.).
  - **Customer ratings** (4★ & above, 3★ & above).
  - **Discount thresholds** (50%+, 30%+, 10%+).
  - **Clear all filters** with active filter chips breadcrumb.
- **Sort Options**: Relevance & Featured, Price Low-to-High, Price High-to-Low, Customer Rating, Discount %, Newest.
- **View Toggle**: Grid View (4-column responsive) and List View.

### 4. 🔎 Product Quick View & Details Modal
- Multi-angle high-res image gallery with interactive thumbnail switcher.
- Color and size variant selection pills.
- Pincode delivery speed estimator with instant calculation (e.g., "Delivery by Tomorrow, 11 AM - FREE").
- Key specifications breakdown table.
- Verified customer reviews with star ratings and a functional **"Write a Review"** form.
- "Add to Cart" and "Buy Now" direct purchase buttons.

### 5. 🛒 Sliding Shopping Cart Drawer
- Slide-out drawer with backdrop blur.
- Quantity adjustment stepper (`+` / `-`) and instant item deletion.
- **Free Delivery Meter**: Dynamic progress bar calculating remaining amount needed for free delivery.
- **Promo Coupon Engine**:
  - `SHOPX100`: Flat ₹100 OFF on orders > ₹500
  - `FESTIVE20`: 20% OFF up to ₹1,000
  - `WELCOME50`: Flat ₹50 OFF
  - `PRIMEPLUS`: 10% OFF
- Detailed bill summary (MRP, Product Discount, Delivery Fee, Taxes, Coupon, Final Total, and total savings calculation).

### 6. 💳 Multi-Step Checkout Experience
- **Step 1: Address**: Full name, mobile number, street address, city, and pincode.
- **Step 2: Payment Method**: UPI (Google Pay, PhonePe, Paytm, QR), Credit/Debit Card, Net Banking, and Cash on Delivery (COD).
- **Step 3: Review & Place Order**: Item summary and total payable amount.
- **Celebratory Confetti**: Interactive HTML5 canvas confetti explosion upon placing an order!
- Unique **Order ID generator** (e.g., `SX-849201-44`) with delivery estimate.

### 7. 📦 Live Order Tracking Stepper
- View all previous orders with detailed receipt.
- Multi-step live tracking timeline:
  1. **Order Placed & Confirmed** ✓
  2. **Packed at ShopX Mega Warehouse** ✓
  3. **In Transit (ShopX Express Air)** ⏳
  4. **Out for Delivery**
  5. **Delivered to Doorstep**

---

## 🚀 How to Run

### Method 1: Start the Python Flask Server (Recommended)

1. Open PowerShell or Command Prompt.
2. Navigate to this directory:
   ```powershell
   cd C:\Users\ragha\.gemini\antigravity\scratch\shopx
   ```
3. Run the app:
   ```powershell
   python app.py
   ```
   *(or double-click `run.bat`)*
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Method 2: Open Directly as Standalone HTML (Zero Dependencies!)

Simply double-click `index.html` in your file explorer, or run:
```powershell
Start-Process "C:\Users\ragha\.gemini\antigravity\scratch\shopx\index.html"
```
The application has built-in smart client fallback that provides all 24+ products, search, filtering, cart, coupons, and orders via `localStorage` even without running any web server!

---

## 🗄️ Project Architecture

```
shopx/
├── app.py                 # Flask REST API server
├── database.py            # SQLite database initialization & query helpers
├── static_data.py         # Seed dataset with 24 realistic products
├── requirements.txt       # Dependencies (Flask)
├── run.bat                # Windows quick launcher batch file
├── README.md              # Full documentation
├── index.html             # Standalone browser entry point
├── templates/
│   └── index.html         # Flask Jinja template
└── static/
    ├── css/
    │   └── style.css      # Amazon/Flipkart inspired modern responsive styles
    └── js/
        ├── products-data.js # Client-side catalog & coupon datasets
        └── app.js         # Core application logic & state management
```
