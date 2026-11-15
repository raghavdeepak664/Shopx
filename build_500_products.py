import json
import os

from generate_catalog import (
    IMAGES_KITCHEN, IMAGES_MOBILES, IMAGES_LAPTOPS, IMAGES_AUDIO,
    IMAGES_WATCHES, IMAGES_FOOTWEAR, IMAGES_FASHION, IMAGES_CAMERAS
)

def build_full_catalog():
    products = []
    current_id = 1

    def add_p(title, brand, category, price, orig_price, rating, reviews, desc, specs, tags, img_pool, is_deal=False, is_best=False):
        nonlocal current_id
        img_idx = (current_id - 1) % len(img_pool)
        img = img_pool[img_idx]
        alt_imgs = [img_pool[(img_idx + i) % len(img_pool)] for i in range(1, min(4, len(img_pool)))]
        
        # Color variants with realistic hex
        colors = [
            {"name": "Midnight Black", "hex": "#1a1a1a", "image": img},
            {"name": "Arctic Silver", "hex": "#e2e8f0", "image": alt_imgs[0] if alt_imgs else img},
            {"name": "Deep Navy", "hex": "#1e3a8a", "image": alt_imgs[1] if len(alt_imgs) > 1 else img}
        ]
        
        discount = int(round((orig_price - price) / orig_price * 100)) if orig_price > price else 5
        
        prod = {
            "id": current_id,
            "title": title,
            "brand": brand,
            "category": category,
            "price": price,
            "original_price": orig_price,
            "discount": discount,
            "rating": round(rating, 1),
            "reviews_count": reviews,
            "image": img,
            "additional_images": [img] + alt_imgs,
            "colors": colors,
            "description": desc,
            "specs": specs,
            "in_stock": True,
            "is_bestseller": is_best,
            "is_deal": is_deal,
            "is_assured": True,
            "fast_delivery": True,
            "deal_claimed_percent": random.randint(45, 95),
            "tags": tags
        }
        products.append(prod)
        current_id += 1

    import random
    random.seed(42)

    # ==========================================
    # 1. HOME & KITCHEN (85 products)
    # Strictly authentic kitchen cookware, dining, appliances, cutlery - NO ROBOTS!
    # ==========================================
    kitchen_items = [
        ("Philips Digital Air Fryer XL 4.2L with Rapid Air Technology", "Philips", 7999, 11995, 4.7, 5420, "Cook crispy, tender meals with up to 90% less oil using patented Rapid Air convection.", {"Capacity": "4.2 Litres", "Power": "1400 Watts", "Preset Modes": "7 Programs", "Warranty": "2 Years"}),
        ("Prestige Iris Plus 750W Mixer Grinder with 3 Stainless Steel Jars", "Prestige", 2999, 6195, 4.5, 14200, "Heavy-duty 750W motor with 3 versatile stainless steel jars and transparent juicer jar.", {"Motor Power": "750 Watts", "Jars Count": "3 Jars + Juicer", "Blade Material": "Forged Stainless Steel", "Warranty": "2 Years"}),
        ("Hawkins Contura 3 Litre Hard Anodised Inner Lid Pressure Cooker", "Hawkins", 1850, 2450, 4.8, 18900, "Curved body for easy stirring, non-reactive black hard-anodized surface for quick heating.", {"Capacity": "3.0 Litres", "Material": "Hard Anodised Aluminum", "Lid Type": "Inner Lid", "Base": "Gas & Induction Compatible"}),
        ("Morphy Richards Europa 800-Watt Espresso and Cappuccino Coffee Maker", "Morphy Richards", 4499, 6495, 4.4, 3810, "Brews 4 cups of rich espresso with steam wand for frothing velvety cappuccinos.", {"Power": "800 Watts", "Pressure": "4 Bar Steam", "Capacity": "4 Cups", "Carafe": "Heat-Resistant Glass"}),
        ("Pigeon by Stovekraft Non-Stick 3-Piece Cookware Set (Kadai, Tawa, Fry Pan)", "Pigeon", 1399, 2995, 4.2, 9800, "5-layer non-stick coating with ergonomic cool-touch handles for everyday cooking.", {"Set Includes": "24cm Kadai, 24cm Fry Pan, 28cm Flat Tawa", "Coating": "5-Layer PFOA Free", "Warranty": "1 Year"}),
        ("Kent Ultra Storage 7L UV + UF Water Purifier with Carbon Block", "Kent", 6499, 9000, 4.6, 6200, "Multi-stage UV and UF water filtration system with 7-litre food-grade storage tank.", {"Filtration Type": "UV + UF + Activated Carbon", "Storage Tank": "7 Litres", "Purification Rate": "60 L/hr", "Power": "36W"}),
        ("Bajaj Splendora 3 Litre 3000W Instant Water Heater Geyser for Kitchen", "Bajaj", 2799, 4490, 4.5, 4120, "High-efficiency 3000W copper heating element with thermoplastic rust-proof outer body.", {"Capacity": "3 Litres", "Power": "3000 Watts", "Pressure Rating": "6 Bar", "Safety": "Auto Thermal Cut-out"}),
        ("Borosil Glass Meal Prep Container Set with Air-Tight Snap Lids (Pack of 4)", "Borosil", 1199, 1790, 4.7, 7200, "100% borosilicate glass containers safe for microwave, oven, freezer, and dishwasher.", {"Pieces": "4 Containers (400ml x 4)", "Material": "100% Borosilicate Glass", "Lids": "Silicone Gasket Air-Tight", "Microwave Safe": "Yes"}),
        ("Milton Thermosteel Flip Lid 1000ml Vacuum Insulated Flask Bottle", "Milton", 899, 1290, 4.8, 22100, "Double-walled vacuum insulation keeps liquids steaming hot or ice-cold for 24 hours.", {"Capacity": "1000 ml", "Material": "18/8 Food Grade Stainless Steel", "Insulation": "Double Wall Vacuum", "Leak Proof": "Yes"}),
        ("Solimo Premium Stainless Steel 6-Piece Chef Kitchen Knife Block Set", "Solimo", 849, 1500, 4.3, 5600, "Precision-tapered stainless steel blades with durable wooden storage stand block.", {"Knives Included": "Chef, Bread, Utility, Paring, Sharpener", "Material": "High-Carbon Stainless Steel", "Block": "Solid Pine Wood"}),
        ("LG 28L Charcoal Convection Microwave Oven with Diet Fry & Auto Cook", "LG", 16490, 22990, 4.7, 3420, "Charcoal lighting heater replicates tandoori flavors with 301 Indian auto cook menus.", {"Capacity": "28 Litres", "Type": "Charcoal Convection", "Cavity": "Stainless Steel", "Special Features": "Diet Fry, Indian Roti Basket"}),
        ("Prestige PIC 20 1600W Induction Cooktop with Push Button Controls", "Prestige", 2199, 3695, 4.4, 11400, "Automatic power and temperature adjustment with anti-magnetic walls for Indian cookware.", {"Power": "1600 Watts", "Control": "Push Button Interface", "Timer": "Built-in Preset Timer", "Voltage": "230V AC"}),
        ("Wonderchef Nutri-Blend 400W Mixer Grinder Blender with 2 Unbreakable Jars", "Wonderchef", 2499, 4500, 4.6, 8900, "Compact 22,000 RPM bullet blender designed by Chef Sanjeev Kapoor for smoothies and masalas.", {"Power": "400 Watts", "RPM": "22,000 RPM", "Jars": "500ml Blending + 300ml Grinding", "Blades": "4-Wing Stainless Steel"}),
        ("Cello Opalware Dazzle Tropical Lagoon 33-Piece Luxury Dinner Set", "Cello", 2499, 4490, 4.6, 4300, "Bone-ash free opalware dinnerware with scratch-resistant, chip-resistant glossy finish.", {"Pieces Count": "33 Pieces (6 Full Plates, 6 Quarter, 12 Bowls)", "Material": "Toughened Opalware Glass", "Dishwasher Safe": "Yes"}),
        ("Bergner Tri-Ply Stainless Steel 24cm Fry Pan with Cast Steel Stay-Cool Handle", "Bergner", 1799, 2990, 4.7, 2100, "3-layer construction ensures zero hotspot heat distribution for restaurant-grade searing.", {"Diameter": "24 cm", "Construction": "Triply (SS 304 - Aluminum - SS 430)", "Induction Bottom": "Yes", "Warranty": "5 Years"}),
        ("Agaro Grand 1400W 30L Professional Oven Toaster Griller (OTG) with Rotisserie", "Agaro", 5499, 8990, 4.5, 3100, "Motorized rotisserie for spit roasting, convection heating, and 6 versatile cooking stages.", {"Capacity": "30 Litres", "Power": "1400 Watts", "Temperature Range": "90°C to 230°C", "Accessories": "Rotisserie Fork, Bake Pan, Grill Rack"}),
        ("Inalsa Pro Inox 1000W Hand Blender with Chopper and Whisk Attachments", "Inalsa", 2199, 3995, 4.4, 6700, "1000-watt variable speed immersion blender with titanium blades and 600ml chopper bowl.", {"Power": "1000 Watts", "Speeds": "Variable Speed + Turbo", "Attachments": "Whisker, Chopper Bowl, Beaker", "Blade": "SS 304"}),
        ("Tupperware Plastic Modular Mates Square Dry Food Storage Dispenser Set (Pack of 4)", "Tupperware", 1799, 2750, 4.7, 5100, "Airtight, moisture-proof pantry canisters with transparent viewing windows.", {"Capacity": "4 Litres each", "Material": "100% Virgin BPA-Free Plastic", "Stackable": "Yes", "Lids": "Tabbed Air-Tight Seals"}),
        ("Classic Cast Iron Pre-Seasoned 10-Inch Deep Dosa & Roti Tawa", "Rock Tawa", 1199, 1999, 4.8, 7300, "Naturally non-stick pre-seasoned cast iron pan for crispy dosas and enriched iron content.", {"Material": "100% Pure Cast Iron", "Pre-Seasoned": "100% Organic Flaxseed Oil", "Weight": "2.1 kg", "Diameter": "26 cm"}),
        ("Prestige Deluxe Alpha Svachh 5.5L Stainless Steel Outer Lid Pressure Cooker", "Prestige", 2799, 4100, 4.7, 8800, "Spillage control deep lid prevents frothy liquid from spilling down the cooker walls.", {"Capacity": "5.5 Litres", "Material": "SS 304 Food Grade", "Safety": "Controlled Gasket Release System", "Base": "Alpha Induction Bottom"}),
        ("Bajaj Majesty 16-Litre Oven Toaster Griller with Keep Warm Function", "Bajaj", 3299, 5299, 4.3, 4900, "Stainless steel heating elements with dual heating zones for baking cakes and toasting.", {"Capacity": "16 Litres", "Power": "1200 Watts", "Timer": "60 Minutes with Auto Shut-off", "Included": "Crumb Tray, Grill Rack"}),
        ("Havells Instacook 1400-Watt Induction Cooktop with Auto Cook Presets", "Havells", 2399, 4195, 4.5, 3900, "LED digital display with 7 pre-programmed Indian cooking functions and timer control.", {"Power": "1400 Watts", "Cookware Compatibility": "Induction Ready Cookware", "Display": "Digital Soft-touch LED", "Warranty": "1 Year"}),
        ("Pigeon 1.5L Stainless Steel Electric Kettle for Rapid Water Boiling", "Pigeon", 599, 1195, 4.3, 24500, "360-degree swivel base with auto shut-off and boil-dry safety protection.", {"Capacity": "1.5 Litres", "Power": "1500 Watts", "Body": "Brushed Stainless Steel", "Safety": "Auto Cut-Off on Boiling"}),
        ("Milton Pro Cook Granite Induction Bottom 3-Piece Cookware Combo", "Milton", 2199, 3990, 4.6, 3200, "Hard-wearing granite spatter coating, heavy-gauge aluminum for uniform heat retention.", {"Items": "Kadhai with Glass Lid (24cm), Fry Pan (24cm), Tawa (25cm)", "Coating": "Triple Layer Granite", "PFOA Free": "Yes"}),
        ("Vinod Platinum Triply Stainless Steel Extra Deep Kadhai with Lid (2.5L)", "Vinod", 1899, 2850, 4.8, 4100, "Magnetic outer layer suitable for induction and flame; inner non-reactive hygienic SS 304.", {"Capacity": "2.5 Litres", "Layers": "SAS Technology (Steel-Aluminum-Steel)", "Lid": "Stainless Steel Tight Seal", "Warranty": "5 Years"}),
        ("InstaCuppa Manual French Press Coffee & Tea Maker (600ml) with 4-Level Mesh", "InstaCuppa", 1299, 2199, 4.7, 3400, "Heat-resistant borosilicate glass carafe with double-mesh filter for smooth grit-free coffee.", {"Capacity": "600 ml (4 Cups)", "Plunger": "4-Part Filtration Screen", "Frame": "Chrome Stainless Steel", "Dishwasher Safe": "Yes"}),
        ("Lifelong 2-Burner Gas Stove with Toughened Glass Top and Heavy Brass Burners", "Lifelong", 1699, 4495, 4.2, 12000, "6mm black shatterproof toughened glass top with nylon knobs and anti-skid rubber feet.", {"Burners": "2 High Efficiency Brass Burners", "Top": "6mm Toughened Glass", "Ignition": "Manual", "Certification": "ISI Certified"}),
        ("Butterfly Jet Elite 750-Watt Mixer Grinder with 4 Heavy Duty Jars", "Butterfly", 3199, 5999, 4.4, 7600, "Powerful motor with overload protector, micro-balanced motor for low vibration and noise.", {"Power": "750 Watts", "Jars": "4 SS Jars (1.5L, 1.0L, 0.4L, Juicer)", "Speed": "3 Speeds + Whip", "Warranty": "2 Years"}),
        ("Philips Daily Collection 2-Slice Pop-up Toaster with 8 Browning Settings", "Philips", 1799, 2595, 4.5, 5900, "Integrated bun rack for warming croissants, 8 adjustable browning levels, removable crumb tray.", {"Power": "830 Watts", "Slots": "2 Wide Self-Centering Slots", "Functions": "Defrost, Reheat, Cancel", "Warranty": "2 Years"}),
        ("Kent Hand Blender 300W Stainless Steel Blades for Smoothies & Soups", "Kent", 999, 1600, 4.3, 3100, "Ergonomic single-button control with detachable stainless steel shaft for quick cleanup.", {"Power": "300 Watts", "Shaft": "Detachable Food Grade SS", "Speed": "One-Touch Push Control", "Cord Length": "1.2 Meters"}),
        ("Cello Checkers PET Plastic Storage Jar Set with Ribbed Grip (Pack of 18)", "Cello", 649, 1250, 4.4, 8200, "Clear BPA-free canisters with threaded lids in 3 convenient sizes (300ml, 650ml, 1200ml).", {"Pack Count": "18 Jars (6 x 300ml, 6 x 650ml, 6 x 1200ml)", "Material": "100% Food-Grade PET", "Air Tight": "Yes"}),
        ("Prestige Omega Deluxe Granite Omni Tawa (280 mm Diameter)", "Prestige", 899, 1495, 4.6, 14800, "Durable granite finish non-stick surface compatible with both metal spoons and induction.", {"Diameter": "28 cm (280mm)", "Coating": "Granite 5-Layer German Coating", "Base": "Gas and Induction", "Warranty": "2 Years"}),
        ("Borosil Pronto Stainless Steel Drip Coffee Maker with Reusable Filter", "Borosil", 1999, 3290, 4.5, 2100, "600ml glass carafe brews up to 4 cups in 6 minutes with warming plate to keep coffee piping hot.", {"Capacity": "600 ml", "Filter": "Washable Mesh Filter", "Auto Keep Warm": "Yes", "Power": "650 Watts"}),
        ("Spotzero by Milton Microfiber Dish Cleaning Scrub Sponge Pack (Pack of 6)", "Milton", 199, 350, 4.4, 5300, "Heavy-duty dual-action sponges with scratch-safe scrubber side for pots and delicate glassware.", {"Count": "6 Pieces", "Material": "High Density Polyurethane Sponge", "Scratch Free": "Yes"}),
        ("Wonderchef Royal Velvet Non-Stick Induction Flat Kadai with Glass Lid (26cm)", "Wonderchef", 1499, 2600, 4.5, 3800, "Virgin aluminum base heats evenly with marble non-stick coating and heat-resistant bakelite handle.", {"Size": "26 cm", "Capacity": "3.2 Litres", "Coating": "5-Layer MetaTuff Non-Stick", "Lid": "Tempered Glass with Steam Vent"}),
        ("Bajaj Rex 500W Mixer Grinder with Nutri-Pro Feature & 3 Stainless Steel Jars", "Bajaj", 1999, 3600, 4.3, 16800, "Rust-proof ABS plastic body with vacuum feet and vacuum-locking multi-functional blades.", {"Power": "500 Watts", "Jars": "1.2L Liquidizing, 0.8L Dry, 0.3L Chutney", "Overload Protection": "Yes", "Warranty": "1 Year"}),
        ("Hawkins Futura Hard Anodised Deep Frying Pan 2.5 Litre with Rosewood Handle", "Hawkins", 1350, 1825, 4.8, 5200, "Extra thick 4.06mm base stays flat, absorbs heat faster, and never warps under high heat.", {"Capacity": "2.5 Litres", "Thickness": "4.06 mm Hard Anodised", "Handle": "Stay-Cool Rosewood Handle", "Gas Compatible": "Yes"}),
        ("Solimo Stainless Steel Induction Bottom Handi Set with Lids (Set of 3)", "Solimo", 999, 1800, 4.3, 4400, "Heavy-gauge food-grade stainless steel pots with snug-fitting lids for boiling and curries.", {"Set Sizes": "1.0L, 1.5L, and 2.0L", "Material": "SS 201 Mirror Finish", "Induction Compatible": "Yes"}),
        ("Agaro Royal 4-Slice Automatic Bread Toaster with Dual Independent Controls", "Agaro", 2999, 4990, 4.6, 1800, "Dual independent control zones with 6 browning settings and removable dual crumb trays.", {"Capacity": "4 Slices", "Power": "1400 Watts", "Slots": "Extra Wide 36mm Slots", "Warranty": "2 Years"}),
        ("Kent Multi-Cooker 800W for Boiling Eggs, Noodles, Steaming & Soups", "Kent", 1499, 2500, 4.4, 2800, "Multi-functional electric cooking kettle with stainless steel inner pot and egg steaming rack.", {"Capacity": "1.2 Litres", "Power": "800 Watts", "Accessories": "Egg Steamer Rack, Glass Lid", "Swivel Base": "360 Degree"}),
        ("Prestige Nakshatra Plus Hard Anodised Duo Handi Pressure Cooker (3L)", "Prestige", 1699, 2490, 4.7, 6100, "Traditional handi shape with unique deep lid for spill-proof everyday dal and rice cooking.", {"Capacity": "3 Litres", "Body": "Hard Anodised Heavy Gauge", "Induction Base": "Alpha Duo Bottom", "Warranty": "5 Years"}),
        ("Milton Executive Stainless Steel Insulated Lunch Box with Bag (Set of 3 Jars)", "Milton", 799, 1150, 4.6, 19200, "Airtight and leak-proof stainless steel tiffin containers nestled inside thermal fabric jacket.", {"Containers": "3 Stainless Steel Containers (280ml each)", "Jacket": "Washable Insulated Carrier", "Leakproof": "100% Guaranteed"}),
        ("Borosil Klip N Store Microwave Safe Glass Containers with Steam Vent (Set of 3)", "Borosil", 999, 1490, 4.7, 3900, "Built-in silicone air vent allows steam release during microwave reheating without removing lid.", {"Sizes": "320ml, 520ml, 800ml", "Material": "100% Borosilicate Glass", "Temperature": "Withstands up to 400°C"}),
        ("Philips Daily Collection 300W Hand Mixer with Dough Hooks & Strip Beatters", "Philips", 1899, 2695, 4.5, 4100, "Lightweight hand mixer with 5 speed settings and stainless steel wire beaters for fluffy cake batter.", {"Power": "300 Watts", "Speeds": "5 Speeds + Turbo Boost", "Beaters": "Stainless Steel Strip Beatters", "Warranty": "2 Years"}),
        ("Pigeon 4-Burner Glass Top Gas Stove with High Flame Brass Burners", "Pigeon", 2999, 6495, 4.1, 7900, "Sleek black toughened glass surface with spacious burner layout to accommodate large cookware.", {"Burners": "4 Brass Burners (2 Big, 2 Small)", "Top": "Spill-Proof Toughened Glass", "Pan Supports": "Tubular Powder Coated"}),
        ("Cello Dura Cool Insulated Water Jug 5 Litres with Easy-Flow Dispenser Tap", "Cello", 699, 1150, 4.4, 4300, "Polyurethane foam insulation keeps iced beverages and water chilled for over 12 hours.", {"Capacity": "5.0 Litres", "Insulation": "PUF Insulation", "Tap": "Food Grade Easy Push Dispenser", "Handle": "Sturdy Carry Handle"}),
        ("Wonderchef Regalia 4-in-1 Juicer Mixer Grinder 500W with Pulp Extractor", "Wonderchef", 2999, 5000, 4.3, 3100, "Heavy-duty centrifugal juicing mesh with large pulp collector and 2 stainless steel grinding jars.", {"Power": "500 Watts", "Functions": "Juicing, Blending, Wet & Dry Grinding", "Pulp Container": "1.5L Detachable"}),
        ("Prestige Svachh Hard Anodised Pressure Pan 3.5L with Glass Lid Combo", "Prestige", 2199, 3295, 4.7, 4800, "Versatile flat pressure pan converts from rapid pressure cooker to deep sauté pan with glass lid.", {"Capacity": "3.5 Litres", "Finish": "Hard Anodised Black", "Lids": "Pressure Lid + Tempered Glass Lid", "Warranty": "5 Years"}),
        ("Hawkins Hevibase 3 Litre Hard Anodised Induction Base Pressure Cooker", "Hawkins", 1999, 2650, 4.8, 6400, "Double-thickness 6.35mm base cooks food uniformly with minimal oil and stays flat forever.", {"Capacity": "3.0 Litres", "Base Thickness": "6.35 mm", "Material": "Hard Anodised Aluminum", "Induction Base": "Magnetic Stainless Steel"}),
        ("Morphy Richards New Europa 800W 4-Cup Drip Coffee Maker with Mesh Filter", "Morphy Richards", 2499, 3895, 4.4, 1900, "Anti-drip mechanism prevents spills when carafe is removed; keep-warm plate maintains brew temperature.", {"Capacity": "600 ml", "Power": "800 Watts", "Filter Type": "Permanent Washable Nylon", "Warranty": "2 Years"}),
    ]

    # Fill remaining Home & Kitchen items to reach 85 products
    extra_kitchen_names = [
        "Prestige CleanHome Vegetable & Fruit Disinfectant Purifier", "Kent Instant Egg Boiler with 3 Boiling Modes for 7 Eggs",
        "Borosil Chef Delite 300-Watt Electric Food Chopper with Twin Blades", "Inalsa Stand Mixer 1200W with 5L Stainless Steel Bowl",
        "Milton Smart Electric Tiffin Lunchbox with Auto Cut-off Heating", "Cello Triply Stainless Steel Casserole with Glass Lid 2.5L",
        "Hawkins Stainless Steel 3L Sandwich Bottom Pressure Cooker", "Philips 750W Juicer Mixer Grinder with NuPure Extraction",
        "Wonderchef Crimson Edge Electric Kettle 1.8L Cordless", "Bajaj Platini Time Art 4-Slice Pop-Up Toaster with LCD Display",
        "Vinod Hard Anodised Roti Tawa with Stay-Cool Wooden Grip 28cm", "Pigeon Healthifry Digital Air Fryer 3.2L 1200W",
        "Kent Electric Kettle Glass Body 1.7L with Blue LED Glow", "Solimo Wall Mounted Stainless Steel Kitchen Spice Rack Organizer",
        "Tupperware Clear Bowl Set with Airtight Colored Lids 3-Pack", "Prestige Induction Friendly Milk Boiler with Whistle 2L",
        "Butterfly Curve Stainless Steel 3-Burner Gas Stove Cooktop", "Morphy Richards 20L Solo Microwave Oven with 5 Power Levels",
        "Agaro Regal Electric Citrus Juicer 100W with Bi-Directional Cone", "Lifelong 500W Mixer Grinder with Liquidizing and Chutney Jars",
        "Milton Pro Cook Cast Iron Kadai with Dual Helper Handles 26cm", "Cello Infusion Glass Water Bottle with Fruit Infuser Basket",
        "Wonderchef Velvet Handi with Glass Lid 22cm PFOA Free", "Borosil Stainless Steel Insulated Gravy Casserole 1.5L",
        "Inalsa 2-in-1 Waffle Maker and Grill Toaster with Non-Stick Plates", "Hawkins Futura Hard Anodised Sauce Pan 2 Litre with Spout",
        "Prestige Svachh Gas Stove 3-Burner with Spill Proof Trays", "Bajaj Deluxe 2-Slice Sandwich Press Maker with Floating Hinge",
        "Pigeon Sheen Stainless Steel Vacuum Thermal Carafe 1.5L", "Kent Cold Pressed Slow Juicer with Low RPM Masticating Tech",
        "Philips Daily Collection 4-in-1 Food Processor with 6 Discs", "Solimo High Grade Silicone Spatula and Basting Brush Set",
        "Cello Aqua Stainless Steel Single Wall Water Bottle 1000ml (Set of 2)", "Wonderchef Gas Oven Tandoor for Roti, Naan & Kebabs",
        "Vinod Stainless Steel Steamer and Modak Maker with Glass Lid"
    ]
    for idx, name in enumerate(extra_kitchen_names):
        brand = name.split()[0]
        price = random.randint(899, 8999)
        orig = int(price * random.uniform(1.2, 1.5))
        kitchen_items.append((
            name, brand, price, orig, round(random.uniform(4.3, 4.9), 1), random.randint(800, 9500),
            f"Authentic premium kitchenware: {name} engineered for everyday Indian culinary excellence.",
            {"Brand": brand, "Category": "Kitchenware & Appliances", "Material": "Food-Grade Stainless Steel / Glass", "Warranty": "1-2 Years"},
        ))

    # Add all 85 Home & Kitchen products
    for item in kitchen_items[:85]:
        add_p(
            title=item[0],
            brand=item[1],
            category="Home & Kitchen",
            price=item[2],
            orig_price=item[3],
            rating=item[4],
            reviews=item[5],
            desc=item[6],
            specs=item[7],
            tags=["kitchen", "cookware", "appliances", "culinary"],
            img_pool=IMAGES_KITCHEN,
            is_deal=random.random() > 0.6,
            is_best=random.random() > 0.7
        )

    # ==========================================
    # 2. MOBiles & TABLETS (75 products)
    # ==========================================
    mobile_models = [
        ("Apple iPhone 15 Pro Max (256 GB, Natural Titanium)", "Apple", 149900, 159900, 4.9, 8400, "Titanium design, A17 Pro chip, Action button, 5x Telephoto camera."),
        ("Apple iPhone 15 (128 GB, Pink)", "Apple", 69999, 79900, 4.8, 12400, "Dynamic Island, 48MP Main camera, USB-C, durable color-infused glass back."),
        ("Apple iPhone 14 (128 GB, Midnight)", "Apple", 56999, 69900, 4.7, 19800, "A15 Bionic chip, dual-camera system with Photonic Engine, all-day battery life."),
        ("Apple iPhone 13 (128 GB, Starlight)", "Apple", 49999, 59900, 4.7, 34200, "Cinematic mode in 1080p at 30 fps, Super Retina XDR display, ceramic shield."),
        ("Samsung Galaxy S24 Ultra 5G (12GB/256GB, Titanium Gray)", "Samsung", 129999, 144999, 4.8, 9200, "Galaxy AI, 200MP camera, built-in S Pen, Snapdragon 8 Gen 3."),
        ("Samsung Galaxy S24 5G (8GB/256GB, Onyx Black)", "Samsung", 74999, 84999, 4.7, 4100, "Compact flagship, dynamic AMOLED 2X 120Hz, Galaxy AI photo assistant."),
        ("Samsung Galaxy Z Fold 5 5G (12GB/512GB, Phantom Black)", "Samsung", 154999, 169999, 4.7, 2400, "Massive 7.6-inch folding screen, multi-window productivity, Flex Mode."),
        ("Samsung Galaxy Z Flip 5 5G (8GB/256GB, Mint)", "Samsung", 89999, 99999, 4.6, 3800, "3.4-inch Flex Window cover screen, zero-gap hinge, hands-free FlexCam."),
        ("Samsung Galaxy A55 5G (8GB/128GB, Awesome Iceblue)", "Samsung", 39999, 44999, 4.5, 6800, "Metal frame, 50MP OIS camera, IP67 water resistance, Knox Vault."),
        ("OnePlus 12 5G (16GB/512GB, Flowy Emerald)", "OnePlus", 64999, 69999, 4.7, 5600, "4th Gen Hasselblad Camera, Snapdragon 8 Gen 3, 100W SUPERVOOC charging."),
        ("OnePlus 12R 5G (8GB/128GB, Cool Blue)", "OnePlus", 39999, 42999, 4.6, 8100, "Snapdragon 8 Gen 2, 1.5K 120Hz ProXDR display, 5500 mAh battery."),
        ("OnePlus Nord CE 4 5G (8GB/256GB, Celadon Marble)", "OnePlus", 24999, 26999, 4.4, 7200, "Snapdragon 7 Gen 3, 100W SUPERVOOC charge, 5500mAh battery."),
        ("Google Pixel 8 Pro (12GB/128GB, Bay Blue)", "Google", 89999, 106999, 4.6, 3400, "Google Tensor G3, Best Take, Magic Audio Eraser, pro camera controls."),
        ("Google Pixel 8 5G (8GB/128GB, Hazel)", "Google", 62999, 75999, 4.5, 4900, "Compact powerhouse, 50MP main sensor, 7 years of Android feature drops."),
        ("Google Pixel 7a (8GB/128GB, Sea)", "Google", 37999, 43999, 4.4, 8600, "Tensor G2, 64MP dual rear cameras, wireless charging, IP67 rating."),
        ("Nothing Phone (2) (12GB/256GB, Dark Grey)", "Nothing", 39999, 54999, 4.6, 4200, "Glyph Interface LED light patterns, Snapdragon 8+ Gen 1, clean Nothing OS 2.5."),
        ("Nothing Phone (2a) 5G (8GB/128GB, White)", "Nothing", 23999, 25999, 4.5, 6400, "Dimensity 7200 Pro, 50MP dual cameras with OIS, transparent back casing."),
        ("Xiaomi 14 Ultra (16GB/512GB, Black Titanium)", "Xiaomi", 99999, 119999, 4.8, 1800, "Leica Quad Camera with 1-inch stepless variable aperture sensor, 90W HyperCharge."),
        ("Redmi Note 13 Pro+ 5G (12GB/512GB, Fusion Purple)", "Redmi", 31999, 35999, 4.4, 9100, "Curved 1.5K AMOLED 120Hz, 200MP OIS camera, 120W HyperCharge, IP68."),
        ("Vivo X100 Pro 5G (16GB/512GB, Asteroid Black)", "Vivo", 89999, 99999, 4.8, 1600, "ZEISS APO 1-inch sensor telephoto, Dimensity 9300, V3 imaging chip."),
        ("Realme 12 Pro+ 5G (12GB/256GB, Submarine Blue)", "Realme", 29999, 33999, 4.4, 5800, "Periscope portrait camera, luxury watch design, 120Hz curved AMOLED."),
        ("Motorola Edge 50 Pro 5G (12GB/256GB, Moonlight Pearl)", "Motorola", 35999, 41999, 4.5, 4100, "Pantone validated camera & display, 125W TurboPower, IP68 rating."),
        ("Apple iPad Pro 13-inch M4 (256GB, Wi-Fi, Space Black)", "Apple", 129900, 139900, 4.9, 1200, "Ultra Retina XDR tandem OLED, breakthrough M4 chip, razor-thin 5.1mm body."),
        ("Apple iPad Air 11-inch M2 (128GB, Wi-Fi, Space Gray)", "Apple", 59900, 64900, 4.8, 2800, "Apple M2 chip, Center Stage landscape 12MP front camera, Touch ID."),
        ("Apple iPad 10th Gen 10.9-inch (64GB, Wi-Fi, Blue)", "Apple", 34900, 39900, 4.7, 14200, "All-screen liquid retina display, A14 Bionic chip, USB-C connector."),
        ("Samsung Galaxy Tab S9 Ultra (14.6-inch AMOLED, 12GB/256GB with S Pen)", "Samsung", 108999, 119999, 4.8, 1100, "Gigantic Dynamic AMOLED 2X screen, IP68 dust/water resistant body and S Pen."),
        ("Samsung Galaxy Tab S9 FE (10.9-inch, 6GB/128GB, Mint)", "Samsung", 34999, 44999, 4.6, 3200, "Exynos 1380, bundled S Pen, Dual speakers by AKG, 8000mAh battery."),
        ("OnePlus Pad 11.61-inch 144Hz ReadFit Screen (8GB/128GB, Halo Green)", "OnePlus", 37999, 39999, 4.6, 2100, "7:5 aspect ratio, 144Hz high refresh display, 67W SUPERVOOC charging."),
        ("Lenovo Tab P12 Pro 12.6-inch 2K AMOLED (8GB/256GB, Storm Grey)", "Lenovo", 39999, 49999, 4.4, 1800, "12.6-inch 2K AMOLED with HDR10+, Quad JBL speakers with Dolby Atmos.")
    ]
    # Expand to 75
    for i in range(len(mobile_models), 75):
        brand = random.choice(["Samsung", "Xiaomi", "Realme", "Motorola", "iQOO", "Poco", "Honor", "Apple"])
        name = f"{brand} Galaxy Prime Max 5G Edition Series {i+1} (128GB)"
        p_val = random.randint(14999, 79999)
        mobile_models.append((name, brand, p_val, int(p_val * 1.18), round(random.uniform(4.3, 4.8), 1), random.randint(1200, 15000), "Fast 5G smartphone with immersive high-refresh screen and AI dual camera."))

    for item in mobile_models[:75]:
        add_p(
            title=item[0], brand=item[1], category="Mobiles & Tablets",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Display": "AMOLED / Super Retina 120Hz", "Camera": "50MP OIS Triple Cam", "Battery": "5000 mAh Fast Charge", "Network": "5G VoLTE"},
            tags=["smartphone", "5g", "flagship", "camera", "mobile"],
            img_pool=IMAGES_MOBILES, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    # ==========================================
    # 3. LAPTOPS & COMPUTERS (75 products)
    # ==========================================
    laptop_models = [
        ("Apple MacBook Pro 16-inch M3 Max (36GB Unified RAM, 1TB SSD, Space Black)", "Apple", 349900, 379900, 5.0, 920, "M3 Max with 16-core CPU and 40-core GPU, Liquid Retina XDR display, up to 22h battery."),
        ("Apple MacBook Air 15-inch M3 Chip (16GB RAM, 512GB SSD, Starlight)", "Apple", 144900, 154900, 4.9, 1420, "M3 chip, 15.3-inch Liquid Retina display, thin 11.5mm silent fanless aluminum body."),
        ("Dell XPS 15 9530 Touchscreen Laptop (Intel i7-13700H, RTX 4060, 32GB/1TB)", "Dell", 214990, 249990, 4.7, 850, "3.5K OLED InfinityEdge touchscreen with carbon fiber palm rest and CNC aluminum."),
        ("ASUS ROG Zephyrus G16 (Intel Core Ultra 9, RTX 4070 8GB, 32GB/1TB, OLED 240Hz)", "ASUS", 189990, 219990, 4.8, 1200, "Precision CNC aluminum body with Slash Lighting, 2.5K 240Hz OLED gaming panel."),
        ("Lenovo ThinkPad X1 Carbon Gen 11 (Intel Core i7-1365U, 16GB/1TB SSD, 2.8K OLED)", "Lenovo", 179990, 209990, 4.8, 640, "Ultra-durable military-spec carbon fiber chassis, ergonomic ThinkPad TrackPoint keyboard."),
        ("HP Spectre x360 2-in-1 Touch Laptop (14-inch 2.8K OLED, Core Ultra 7, 16GB/1TB)", "HP", 154990, 179990, 4.7, 780, "360-degree convertible with IMAX Enhanced OLED screen and 9MP AI camera with night mode."),
        ("Acer Predator Helios 16 Gaming Laptop (Intel i9-14900HX, RTX 4080 12GB, 32GB/1TB)", "Acer", 229990, 269990, 4.7, 910, "5th Gen AeroBlade 3D fan cooling, 240Hz WQXGA mini-LED display with per-key RGB."),
        ("LG Gram 17 Lightweight Laptop (Intel Core Ultra 7, 16GB/1TB, 17-inch WQXGA)", "LG", 134990, 159990, 4.6, 520, "Massive 17-inch display in an featherlight 1.35kg magnesium alloy chassis with 80Wh battery."),
        ("Logitech MX Master 3S Advanced Wireless Performance Mouse (Quiet Clicks)", "Logitech", 8995, 10995, 4.9, 12800, "8K DPI any-surface glass tracking sensor with MagSpeed electromagnetic scroll wheel."),
        ("Keychron Q1 Pro Wireless Custom Mechanical Keyboard (Gateron Jupiter Brown)", "Keychron", 16999, 19999, 4.9, 2100, "Full CNC aluminum body, double-gasket acoustic dampening, QMK/VIA programmable."),
        ("LG UltraGear 27-inch QHD OLED Gaming Monitor (240Hz, 0.03ms, G-SYNC)", "LG", 79999, 99999, 4.8, 1400, "Breathtaking OLED contrast ratio with 240Hz refresh rate and 0.03ms instant response time."),
        ("Dell UltraSharp 32-inch 4K USB-C Hub Monitor with IPS Black Technology", "Dell", 69999, 84999, 4.8, 1100, "IPS Black panel delivers 2000:1 contrast, 98% DCI-P3 color gamut, and 90W USB-C PD hub."),
        ("Samsung 990 PRO 2TB PCIe 4.0 NVMe M.2 Internal Gaming SSD with Heatsink", "Samsung", 18999, 24999, 4.9, 6400, "Read speeds up to 7450 MB/s for PS5 console and elite PC desktop gaming stations."),
        ("Sony PlayStation 5 Console Slim Disc Edition with 1TB SSD", "Sony", 54990, 59990, 4.9, 24100, "Ray tracing immersion with DualSense haptic feedback and ultra-fast 1TB storage."),
        ("Elgato Stream Deck MK.2 Studio Controller with 15 Customizable LCD Keys", "Elgato", 14990, 17990, 4.8, 3800, "One-touch tactile control for streaming, recording, audio balancing, and app automation.")
    ]
    for i in range(len(laptop_models), 75):
        brand = random.choice(["Dell", "HP", "Lenovo", "ASUS", "Acer", "MSI", "Apple"])
        name = f"{brand} ProBook Business Workstation 15.6 Series {i+1} (16GB/512GB)"
        p_val = random.randint(39990, 169990)
        laptop_models.append((name, brand, p_val, int(p_val * 1.15), round(random.uniform(4.3, 4.9), 1), random.randint(400, 6000), "High-performance enterprise laptop with anti-glare display and long-lasting battery."))

    for item in laptop_models[:75]:
        add_p(
            title=item[0], brand=item[1], category="Laptops & Computers",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Processor": "Intel Core / Apple M-Series", "RAM": "16GB - 32GB High Speed", "Storage": "512GB - 1TB NVMe SSD", "Display": "QHD / OLED IPS"},
            tags=["laptop", "computing", "macbook", "workstation", "gaming"],
            img_pool=IMAGES_LAPTOPS, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    # ==========================================
    # 4. AUDIO & HEADPHONES (65 products)
    # ==========================================
    audio_models = [
        ("Sony WH-1000XM5 Wireless Noise Canceling Over-Ear Headphones (Silver)", "Sony", 28990, 34990, 4.8, 14200, "Industry-leading noise cancellation with two processors and 8 microphones for clear calls."),
        ("Bose QuietComfort Ultra Wireless Noise Cancelling Headphones", "Bose", 35900, 39900, 4.8, 6200, "World-class active noise cancellation with breakthrough spatial Bose Immersive Audio."),
        ("Apple AirPods Pro (2nd Gen) with MagSafe Case (USB-C)", "Apple", 22900, 24900, 4.8, 29000, "Up to 2x more active noise cancellation with Personalized Spatial Audio."),
        ("Apple AirPods Max Over-Ear Headphones with Active Noise Cancellation (Space Gray)", "Apple", 59900, 64900, 4.7, 4300, "Custom acoustic design with Apple-designed H1 chips in each ear cup and knit mesh canopy."),
        ("Sennheiser Momentum 4 Wireless ANC Headphones with 60-Hour Battery", "Sennheiser", 24990, 34990, 4.7, 3100, "Audiophile-inspired 42mm transducer system with massive 60-hour playtime on a single charge."),
        ("JBL Flip 6 Portable Waterproof Bluetooth Speaker with 12H Battery", "JBL", 9999, 13999, 4.7, 18400, "Bold 2-way sound system with IP67 water and dust resistance for outdoor adventures."),
        ("Marshall Stanmore III Wireless Home Bluetooth Speaker (Black)", "Marshall", 31999, 39999, 4.8, 2800, "Iconic rock 'n' roll vintage aesthetics with wider stereo soundstage and dynamic loudness."),
        ("boAt Airdopes 141 ANC True Wireless Earbuds with 42H Playtime", "boAt", 1499, 4490, 4.2, 38000, "Active Noise Cancellation up to 32dB with low latency 50ms BEAST Mode for gaming."),
        ("Audio-Technica ATH-M50x Professional Studio Monitor Headphones", "Audio-Technica", 12999, 17500, 4.9, 16400, "Critically acclaimed studio sound clarity with 45mm large-aperture neodymium drivers."),
        ("Shure SM7B Vocal Dynamic Cardioid Studio Recording Microphone", "Shure", 38990, 45990, 4.9, 5200, "Legendary broadcast microphone for podcasts, studio vocals, and radio broadcasting.")
    ]
    for i in range(len(audio_models), 65):
        brand = random.choice(["Sony", "JBL", "Bose", "boAt", "Marshall", "Sennheiser", "Noise", "Realme"])
        name = f"{brand} SoundPulse Wireless ANC Bluetooth Series {i+1}"
        p_val = random.randint(1299, 29990)
        audio_models.append((name, brand, p_val, int(p_val * 1.35), round(random.uniform(4.2, 4.9), 1), random.randint(1500, 18000), "Crystal clear acoustics with dynamic bass and long-lasting wireless playback."))

    for item in audio_models[:65]:
        add_p(
            title=item[0], brand=item[1], category="Audio & Headphones",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Driver": "40mm High-Res Audio Drivers", "Battery": "30+ Hours Wireless", "Connectivity": "Bluetooth 5.3 / 3.5mm AUX", "Noise Cancellation": "Hybrid Active Noise Cancellation"},
            tags=["audio", "headphones", "anc", "music", "bluetooth"],
            img_pool=IMAGES_AUDIO, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    # ==========================================
    # 5. SMART WATCHES & WEARABLES (50 products)
    # ==========================================
    watch_models = [
        ("Apple Watch Ultra 2 (49mm Titanium Case with Orange Ocean Band)", "Apple", 89900, 94900, 4.9, 3200, "3000-nit display, dual-frequency GPS, 36 hours normal battery and water resistance to 100m."),
        ("Apple Watch Series 9 GPS 45mm (Midnight Aluminum Case with Sport Band)", "Apple", 41900, 44900, 4.8, 9800, "Double Tap gesture, bright 2000-nit display, ECG, Blood Oxygen and cycle tracking."),
        ("Samsung Galaxy Watch 6 Classic (47mm Bluetooth, Stainless Steel Black)", "Samsung", 32999, 40999, 4.7, 4300, "Physical rotating bezel, sapphire crystal glass, body composition analysis, sleep coaching."),
        ("Garmin Forerunner 965 Premium GPS Running Smartwatch with AMOLED Display", "Garmin", 64990, 72990, 4.9, 1600, "Titanium bezel, training readiness score, integrated maps and up to 23 days battery life."),
        ("Fitbit Charge 6 Fitness Tracker with Google Apps (Obsidian / Black)", "Fitbit", 14999, 18999, 4.5, 5100, "Accurate heart rate tracking during HIIT, built-in GPS, YouTube Music controls, and EDA scan."),
        ("Fossil Gen 6 Smartwatch with Alexa Built-in (Smoke Stainless Steel)", "Fossil", 14995, 24995, 4.3, 3900, "Snapdragon Wear 4100+, continuous SpO2 tracking, fast charging up to 80% in 30 minutes.")
    ]
    for i in range(len(watch_models), 50):
        brand = random.choice(["Apple", "Samsung", "Garmin", "Amazfit", "Noise", "Fire-Boltt", "boAt", "Fitbit"])
        name = f"{brand} Chrono Pro Smartwatch Series {i+1} with AMOLED Display"
        p_val = random.randint(1999, 49990)
        watch_models.append((name, brand, p_val, int(p_val * 1.4), round(random.uniform(4.2, 4.8), 1), random.randint(1200, 14000), "Comprehensive health monitoring smartwatch with heart rate, SpO2, and workout modes."))

    for item in watch_models[:50]:
        add_p(
            title=item[0], brand=item[1], category="Smart Watches & Wearables",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Display": "1.4-inch AMOLED Always-On", "Sensors": "Heart Rate, SpO2, Sleep, ECG", "Battery": "Up to 14 Days", "Water Resistance": "5 ATM Swimproof"},
            tags=["smartwatch", "wearables", "fitness", "health", "applewatch"],
            img_pool=IMAGES_WATCHES, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    # ==========================================
    # 6. FOOTWEAR & SNEAKERS (60 products)
    # ==========================================
    footwear_models = [
        ("Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found' (UK 9)", "Nike", 18995, 22995, 4.9, 8100, "Vintage cracked leather collar, iconic Chicago white, black and varsity red color blocking."),
        ("Adidas Ultraboost Light Running Shoes for Men (Core Black / Cloud White)", "Adidas", 12999, 18999, 4.7, 6400, "Light BOOST cushioning delivers epic energy return with breathable PRIMEKNIT+ textile."),
        ("Puma Men's Smash v2 Leather Casual Court Sneakers (White / Black)", "Puma", 2499, 4499, 4.4, 18200, "Soft genuine leather upper with contrast formstrip and dual-density SoftFoam+ sockliner."),
        ("New Balance 9060 Lifestyle Sneakers (Rain Cloud Grey with Castlerock)", "New Balance", 15999, 17999, 4.8, 3200, "Futuristic wavy design lines with dual-density ABZORB and SBS heel cushioning."),
        ("On Cloudmonster Max Cushioning Road Running Shoes (All Black)", "On Running", 17999, 19999, 4.8, 2900, "Monster-level CloudTec elements paired with snappy Speedboard for soft landings."),
        ("Nike Air Force 1 '07 Classic Low-Top Sneakers (Triple White)", "Nike", 8495, 9695, 4.8, 24100, "Stitched leather overlays, encapsulated Nike Air cushioning, timeless low-cut padded collar.")
    ]
    for i in range(len(footwear_models), 60):
        brand = random.choice(["Nike", "Adidas", "Puma", "Reebok", "New Balance", "Asics", "Red Tape", "Clarks"])
        name = f"{brand} Aeroflex Sport Running Shoes Series {i+1}"
        p_val = random.randint(1799, 16999)
        footwear_models.append((name, brand, p_val, int(p_val * 1.3), round(random.uniform(4.3, 4.8), 1), random.randint(800, 11000), "Engineered mesh upper with responsive shock-absorbing midsole for daily training."))

    for item in footwear_models[:60]:
        add_p(
            title=item[0], brand=item[1], category="Footwear & Sneakers",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Upper": "Premium Mesh / Suede / Leather", "Sole": "Durable High-Traction Rubber", "Cushioning": "Air Cushion / Responsive Foam", "Sizes Available": "UK 6, 7, 8, 9, 10, 11"},
            tags=["footwear", "sneakers", "running", "casual", "nike"],
            img_pool=IMAGES_FOOTWEAR, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    # ==========================================
    # 7. FASHION & APPAREL (60 products)
    # ==========================================
    fashion_models = [
        ("Levi's Men's 511 Slim Fit Stretch Denim Jeans (Dark Indigo)", "Levi's", 2799, 4299, 4.5, 14200, "Modern slim jeans with room to move. Added stretch provides all-day comfort."),
        ("Tommy Hilfiger Men's Classic Pique Polo Shirt (Navy Blue)", "Tommy Hilfiger", 2499, 3999, 4.4, 5800, "Collegiate polo with signature flag embroidery on chest in 100% breathable organic cotton."),
        ("Ray-Ban Classic Aviator Polarized Sunglasses (Gold Frame / Green G-15)", "Ray-Ban", 9890, 12890, 4.7, 8200, "Legendary polarized crystal lenses block 99% of glare with 100% UV protection."),
        ("Calvin Klein Jeans Men's Monogram Logo Cotton Fleece Hoodie (Jet Black)", "Calvin Klein", 4999, 7999, 4.6, 2100, "Cozy brushed cotton fleece with kangaroo front pocket and contrast monogram chest graphic."),
        ("Zara Men's Textured Tailored Slim Fit Suit Blazer (Charcoal Grey)", "Zara", 6990, 9990, 4.5, 1600, "Notch lapel collar with double back vents and structured shoulders for formal events."),
        ("Manyavar Men's Royal Silk Blend Embroidered Kurta Pajama Set (Maroon)", "Manyavar", 3999, 6999, 4.7, 3400, "Artisan jacquard embroidery along mandarin collar with comfortable matching churidar.")
    ]
    for i in range(len(fashion_models), 60):
        brand = random.choice(["Levi's", "Tommy Hilfiger", "Zara", "H&M", "Allen Solly", "Peter England", "Jack & Jones", "U.S. Polo"])
        name = f"{brand} Urban Classic Casual Apparel Edition {i+1}"
        p_val = random.randint(999, 8999)
        fashion_models.append((name, brand, p_val, int(p_val * 1.35), round(random.uniform(4.2, 4.8), 1), random.randint(900, 9500), "Crafted with soft breathable organic fabrics for effortless everyday comfort and style."))

    for item in fashion_models[:60]:
        add_p(
            title=item[0], brand=item[1], category="Fashion & Apparel",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Material": "100% Breathable Cotton / Denim", "Fit": "Regular / Slim Fit", "Care": "Machine Wash Warm", "Sizes Available": "S, M, L, XL, XXL"},
            tags=["fashion", "clothing", "apparel", "denim", "casual"],
            img_pool=IMAGES_FASHION, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    # ==========================================
    # 8. CAMERAS & PHOTOGRAPHY (50 products)
    # ==========================================
    camera_models = [
        ("Sony Alpha 7 IV Full-Frame Hybrid Mirrorless Camera (Body Only)", "Sony", 204990, 242990, 4.9, 2100, "33MP Exmor R full-frame sensor with 4K 60p video and Real-time Eye AF for Humans and Animals."),
        ("Canon EOS R50 Mirrorless Camera with RF-S 18-45mm IS STM Lens", "Canon", 61990, 75995, 4.7, 3100, "Compact content creation camera with 24.2MP sensor and uncropped 6K oversampled 4K 30p."),
        ("DJI Mini 4 Pro Fly More Combo Drone with DJI RC 2 Smart Controller", "DJI", 112990, 128990, 4.9, 1800, "Sub-249g folding drone with omnidirectional obstacle avoidance and 4K 60fps HDR vertical video."),
        ("GoPro HERO12 Black Action Camera with Enduro Battery & Waterproof Casing", "GoPro", 37990, 44990, 4.7, 6800, "5.3K 60fps video with HyperSmooth 6.0 stabilization and rugged waterproof design to 33ft."),
        ("Fujifilm X-T5 Mirrorless Digital Camera Body (Silver Classic)", "Fujifilm", 149999, 169999, 4.8, 1400, "40.2MP X-Trans CMOS 5 HR sensor with classic tactile exposure dials and 7 stops of IBIS."),
        ("Sony FE 24-70mm f/2.8 GM II G Master Standard Zoom Full-Frame Lens", "Sony", 179990, 199990, 4.9, 980, "The world's lightest f/2.8 standard zoom lens with extreme optical clarity and smooth bokeh.")
    ]
    for i in range(len(camera_models), 50):
        brand = random.choice(["Sony", "Canon", "Nikon", "Fujifilm", "GoPro", "DJI", "Sigma", "Godox"])
        name = f"{brand} Lumix Pro Photography Optics Kit Series {i+1}"
        p_val = random.randint(14999, 189990)
        camera_models.append((name, brand, p_val, int(p_val * 1.2), round(random.uniform(4.4, 4.9), 1), random.randint(300, 4500), "Professional optics with multi-coating glass for stunning image resolution."))

    for item in camera_models[:50]:
        add_p(
            title=item[0], brand=item[1], category="Cameras & Photography",
            price=item[2], orig_price=item[3], rating=item[4], reviews=item[5], desc=item[6],
            specs={"Resolution": "4K / 6K Video & 30+ Megapixels", "Sensor": "Full-Frame / APS-C CMOS", "Stabilization": "5-Axis In-Body Optical", "Connectivity": "Wi-Fi, Bluetooth, USB-C"},
            tags=["camera", "photography", "mirrorless", "4k", "dji"],
            img_pool=IMAGES_CAMERAS, is_deal=random.random() > 0.6, is_best=random.random() > 0.7
        )

    print(f"Generated {len(products)} products total.")
    return products

if __name__ == "__main__":
    products = build_full_catalog()
    
    # Save to static_data.py
    py_code = f'"""\nPre-defined Python catalog data for ShopX database seeding (500+ Items).\n"""\n\nDEFAULT_PRODUCTS = {repr(products)}\n'
    with open(r'C:\Users\ragha\.gemini\antigravity\scratch\shopx\static_data.py', 'w', encoding='utf-8') as f:
        f.write(py_code)
    print("Successfully wrote static_data.py!")

    # Save to static/js/products-data.js
    js_code = f'/**\n * ShopX Pre-loaded Products Catalog (500+ Items)\n */\nconst INITIAL_PRODUCTS = {json.dumps(products, indent=2)};\n'
    with open(r'C:\Users\ragha\.gemini\antigravity\scratch\shopx\static\js\products-data.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    print("Successfully wrote static/js/products-data.js!")
