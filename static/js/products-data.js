// ShopX Comprehensive Product Catalog Database
const INITIAL_PRODUCTS = [
  {
    id: 1,
    title: "Apple iPhone 15 Pro (128 GB) - Natural Titanium",
    brand: "Apple",
    category: "Mobiles & Tablets",
    price: 119900,
    original_price: 134900,
    discount: 11,
    rating: 4.7,
    reviews_count: 3420,
    image: "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80"
    ],
    description: "iPhone 15 Pro forged in titanium and featuring the groundbreaking A17 Pro chip, customizable Action button, and the most versatile camera system ever on iPhone.",
    specs: {
      "Display": "6.1-inch Super Retina XDR OLED 120Hz ProMotion",
      "Processor": "A17 Pro chip with 6-core GPU",
      "Camera": "48MP Main + 12MP Ultra Wide + 12MP 3x Telephoto",
      "Battery": "Up to 23 hours video playback",
      "Storage": "128 GB",
      "Colors": ["Natural Titanium", "Blue Titanium", "White Titanium", "Black Titanium"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 78,
    tags: ["5g", "flagship", "camera", "titanium"]
  },
  {
    id: 2,
    title: "Samsung Galaxy S24 Ultra 5G (12GB RAM, 256GB Storage, Titanium Gray)",
    brand: "Samsung",
    category: "Mobiles & Tablets",
    price: 129999,
    original_price: 144999,
    discount: 10,
    rating: 4.8,
    reviews_count: 2890,
    image: "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Meet Galaxy S24 Ultra with Galaxy AI, built with a durable titanium shield and integrated S Pen. 200MP camera captures vivid nightography.",
    specs: {
      "Display": "6.8-inch Dynamic AMOLED 2X QHD+ 120Hz",
      "Processor": "Snapdragon 8 Gen 3 for Galaxy",
      "Camera": "200MP Quad Tele System with 5x optical zoom",
      "Battery": "5000 mAh with 45W Fast Charging",
      "Storage": "256 GB / 12GB RAM",
      "Colors": ["Titanium Gray", "Titanium Black", "Titanium Violet"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["galaxy", "ai", "spen", "200mp"]
  },
  {
    id: 3,
    title: "OnePlus 12 (Flowy Emerald, 16GB RAM, 512GB Storage)",
    brand: "OnePlus",
    category: "Mobiles & Tablets",
    price: 64999,
    original_price: 69999,
    discount: 7,
    rating: 4.6,
    reviews_count: 1450,
    image: "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Powered by Qualcomm Snapdragon 8 Gen 3, 4th Gen Hasselblad Camera for Mobile, and revolutionary 100W SUPERVOOC flash charge.",
    specs: {
      "Display": "6.82-inch 2K 120Hz ProXDR Display with Aqua Touch",
      "Processor": "Snapdragon 8 Gen 3",
      "Camera": "50MP Sony LYT-808 + 64MP 3X Periscope + 48MP Ultra-wide",
      "Battery": "5400 mAh with 100W Wired & 50W Wireless Charging",
      "Colors": ["Flowy Emerald", "Silky Black"]
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 62,
    tags: ["hasselblad", "fastcharge", "flagship"]
  },
  {
    id: 4,
    title: "Apple MacBook Air 15-inch M3 Chip (16GB Unified Memory, 512GB SSD)",
    brand: "Apple",
    category: "Laptops & Computers",
    price: 154900,
    original_price: 174900,
    discount: 11,
    rating: 4.9,
    reviews_count: 820,
    image: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Lean, mean, M3 machine. Strikingly thin design with up to 18 hours of battery life and an expansive Liquid Retina display.",
    specs: {
      "Display": "15.3-inch Liquid Retina with True Tone (500 nits)",
      "Processor": "Apple M3 8-core CPU and 10-core GPU",
      "Memory": "16GB Unified Memory",
      "Storage": "512GB Fast SSD",
      "Weight": "1.51 kg",
      "Colors": ["Midnight", "Starlight", "Space Gray", "Silver"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["macbook", "m3", "apple", "laptop"]
  },
  {
    id: 5,
    title: "ASUS ROG Zephyrus G16 Gaming Laptop (Intel Core Ultra 9, RTX 4070, 32GB/1TB)",
    brand: "ASUS",
    category: "Laptops & Computers",
    price: 199990,
    original_price: 239990,
    discount: 17,
    rating: 4.7,
    reviews_count: 410,
    image: "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Ultra-thin precision CNC aluminum chassis with ROG Nebula OLED display, cutting-edge AI-accelerated Intel Core Ultra 9 and NVIDIA GeForce RTX 4070.",
    specs: {
      "Display": "16-inch 2.5K 240Hz 0.2ms OLED ROG Nebula Display",
      "Processor": "Intel Core Ultra 9 185H with Intel AI Boost NPU",
      "GPU": "NVIDIA GeForce RTX 4070 (8GB GDDR6)",
      "Memory": "32GB LPDDR5X 7467MHz",
      "Storage": "1TB PCIe 4.0 NVMe M.2 SSD",
      "Colors": ["Eclipse Gray", "Platinum White"]
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 85,
    tags: ["gaming", "rtx4070", "oled", "rog"]
  },
  {
    id: 6,
    title: "Sony WH-1000XM5 Wireless Industry Leading Noise Canceling Headphones",
    brand: "Sony",
    category: "Audio & Headphones",
    price: 26990,
    original_price: 34990,
    discount: 23,
    rating: 4.8,
    reviews_count: 5120,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Two processors and eight microphones for unprecedented noise cancellation. Exceptional sound quality engineered to perfection with 30-hour battery life.",
    specs: {
      "ANC": "Integrated Processor V1 and HD Noise Canceling Processor QN1",
      "Battery Life": "Up to 30 hours with ANC on (3-min charge = 3 hours)",
      "Connectivity": "Bluetooth 5.2, Multipoint connection, LDAC",
      "Microphones": "4 beamforming microphones with AI voice pickup",
      "Colors": ["Black", "Silver", "Midnight Blue"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 91,
    tags: ["anc", "sony", "headphones", "bluetooth"]
  },
  {
    id: 7,
    title: "Apple AirPods Pro (2nd Gen) with USB-C MagSafe Case",
    brand: "Apple",
    category: "Audio & Headphones",
    price: 21999,
    original_price: 24900,
    discount: 12,
    rating: 4.8,
    reviews_count: 7300,
    image: "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80"
    ],
    description: "H2 chip delivers up to 2x more Active Noise Cancellation, Adaptive Audio that tailors noise control to your environment, and Personalized Spatial Audio.",
    specs: {
      "Chip": "Apple H2 headphone chip, Apple U1 chip in case",
      "Battery": "Up to 6 hours listening time, 30 hours with case",
      "Water Resistance": "Dust, sweat, and water resistant (IP54)",
      "Charging": "USB-C, MagSafe, Apple Watch charger, Qi-certified"
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["airpods", "apple", "tws", "anc"]
  },
  {
    id: 8,
    title: "boAt Airdopes 141 ANC TWS Earbuds with 42H Playtime & Beast Mode",
    brand: "boAt",
    category: "Audio & Headphones",
    price: 1299,
    original_price: 4990,
    discount: 74,
    rating: 4.2,
    reviews_count: 14200,
    image: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Block the unwanted racket with up to 32dB Active Noise Cancellation. Enjoy 50ms low latency BEAST mode for gaming and ASAP charge.",
    specs: {
      "Noise Cancellation": "Up to 32dB ANC",
      "Playtime": "Up to 42 hours total",
      "Drivers": "10mm dynamic drivers",
      "Colors": ["Gunmetal Black", "Cider White", "Emerald Green"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 94,
    tags: ["budget", "boat", "tws", "earbuds"]
  },
  {
    id: 9,
    title: "Apple Watch Series 9 GPS 45mm Midnight Aluminum Case",
    brand: "Apple",
    category: "Smart Watches & Wearables",
    price: 41999,
    original_price: 44900,
    discount: 6,
    rating: 4.7,
    reviews_count: 1890,
    image: "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Smarter, brighter, and mightier. Double tap gesture control, 2000-nit display, advanced health and fitness sensors with ECG and Blood Oxygen.",
    specs: {
      "Display": "Always-On Retina display, up to 2000 nits",
      "Processor": "S9 SiP with 4-core Neural Engine",
      "Health Sensors": "ECG app, Blood Oxygen, Temperature sensing",
      "Colors": ["Midnight", "Starlight", "Silver", "(PRODUCT)RED"]
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["applewatch", "smartwatch", "fitness"]
  },
  {
    id: 10,
    title: "Samsung Galaxy Watch 6 Classic (Bluetooth, 47mm, Black)",
    brand: "Samsung",
    category: "Smart Watches & Wearables",
    price: 31999,
    original_price: 36999,
    discount: 14,
    rating: 4.5,
    reviews_count: 1100,
    image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80"
    ],
    description: "The timeless rotating bezel returns with a 20% larger display, advanced sleep coaching, body composition BIA sensor, and personalized HR zones.",
    specs: {
      "Bezel": "Physical Rotating Stainless Steel Bezel",
      "Display": "1.5-inch Super AMOLED Sapphire Crystal",
      "Sensors": "BioActive Sensor (Optical Heart Rate + Electrical Heart + BIA)",
      "Durability": "5ATM + IP68 / MIL-STD-810H"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 54,
    tags: ["samsung", "classic", "wearos"]
  },
  {
    id: 11,
    title: "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
    brand: "Nike",
    category: "Footwear & Sneakers",
    price: 16995,
    original_price: 21995,
    discount: 23,
    rating: 4.9,
    reviews_count: 3670,
    image: "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=80"
    ],
    description: "The iconic silhouette returns with cracked leather accents, aged vintage midsoles, and authentic box detailing honoring the 1985 classic.",
    specs: {
      "Upper": "Premium leather with aged finish",
      "Sole": "Air-Sole unit in the heel for lightweight cushioning",
      "Style": "High-top basketball sneaker",
      "Sizes Available": ["UK 7", "UK 8", "UK 9", "UK 10", "UK 11"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["jordan", "nike", "sneakers", "streetwear"]
  },
  {
    id: 12,
    title: "Adidas Ultraboost Light Running Shoes for Men (Core Black)",
    brand: "Adidas",
    category: "Footwear & Sneakers",
    price: 11999,
    original_price: 18999,
    discount: 37,
    rating: 4.6,
    reviews_count: 2150,
    image: "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Experience epic energy return with our lightest Boost ever. Continental Rubber outsole delivers extraordinary grip in wet and dry conditions.",
    specs: {
      "Midsole": "Light BOOST cushioning (30% lighter material)",
      "Upper": "PRIMEKNIT+ textile crafted with recycled ocean plastic",
      "Drop": "10 mm (Heel 22 mm / Forefoot 12 mm)",
      "Sizes Available": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10"]
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 71,
    tags: ["ultraboost", "running", "adidas", "gym"]
  },
  {
    id: 13,
    title: "Levi's Men's 511 Slim Fit Stretch Denim Jeans (Dark Indigo)",
    brand: "Levi's",
    category: "Fashion & Apparel",
    price: 2499,
    original_price: 4199,
    discount: 40,
    rating: 4.4,
    reviews_count: 5400,
    image: "https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=800&q=80"
    ],
    description: "A modern slim with room to move. The 511 Slim Fit Stretch Jeans are a classic since right now, engineered with built-in stretch comfort.",
    specs: {
      "Fit": "Slim through seat and thigh, slim leg opening",
      "Fabric": "99% Cotton, 1% Elastane",
      "Waist": "Sits below waist",
      "Sizes Available": ["30W x 32L", "32W x 32L", "34W x 32L", "36W x 32L"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["levis", "jeans", "denim", "fashion"]
  },
  {
    id: 14,
    title: "Tommy Hilfiger Men's Classic Pique Polo Shirt (Navy Blue)",
    brand: "Tommy Hilfiger",
    category: "Fashion & Apparel",
    price: 2299,
    original_price: 4599,
    discount: 50,
    rating: 4.5,
    reviews_count: 1780,
    image: "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Signature classic regular-fit polo in breathable pure cotton pique, finished with the iconic embroidered flag emblem on the chest.",
    specs: {
      "Material": "100% Breathable Pique Cotton",
      "Collar": "Ribbed polo collar with 2-button placket",
      "Sizes Available": ["S", "M", "L", "XL", "XXL"]
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 88,
    tags: ["polo", "casual", "luxury", "tommy"]
  },
  {
    id: 15,
    title: "Sony Alpha 7 IV Full-Frame Hybrid Mirrorless Camera (Body Only)",
    brand: "Sony",
    category: "Cameras & Photography",
    price: 199990,
    original_price: 224990,
    discount: 11,
    rating: 4.8,
    reviews_count: 670,
    image: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Groundbreaking 33MP Exmor R back-illuminated sensor, 4K 60p 10-bit 4:2:2 video, Real-time Eye AF for humans, animals, and birds.",
    specs: {
      "Sensor": "33.0 Megapixel 35mm full-frame Exmor R CMOS",
      "Video": "4K 60p recording with S-Cinetone profile",
      "Stabilization": "5-axis in-body optical image stabilization (5.5 stops)",
      "Autofocus": "759 phase-detection points covering 94% of frame"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: false,
    is_assured: true,
    fast_delivery: false,
    tags: ["camera", "sony", "fullframe", "mirrorless"]
  },
  {
    id: 16,
    title: "Philips Air Fryer XL 4.1L with Rapid Air Technology & Digital Touch",
    brand: "Philips",
    category: "Home & Kitchen",
    price: 8999,
    original_price: 13995,
    discount: 36,
    rating: 4.6,
    reviews_count: 9800,
    image: "https://images.unsplash.com/photo-1586208958839-06c17cacdf08?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1586208958839-06c17cacdf08?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Fry with up to 90% less fat. Rapid Air Technology circulates hot air around food for crispy, tasty meals without oil.",
    specs: {
      "Capacity": "4.1 Liters (Ideal for family of 4-5)",
      "Power": "1400 Watts",
      "Preset Programs": "7 Touch presets for fries, chicken, baking, defrost",
      "Cleaning": "Dishwasher safe removable basket"
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 81,
    tags: ["kitchen", "airfryer", "cooking", "health"]
  },
  {
    id: 17,
    title: "Dyson V12 Detect Slim Total Clean Cordless Vacuum Cleaner",
    brand: "Dyson",
    category: "Home & Kitchen",
    price: 49900,
    original_price: 55900,
    discount: 11,
    rating: 4.7,
    reviews_count: 1420,
    image: "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Laser illumination reveals invisible microscopic dust on hard floors. Piezo sensor continuously measures and counts dust particles.",
    specs: {
      "Suction Power": "150 AW powerful suction",
      "Run Time": "Up to 60 minutes fade-free power",
      "Weight": "Ultra-lightweight 2.2 kg",
      "Filtration": "Fully-sealed 5-stage filtration captures 99.99% particles"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["dyson", "vacuum", "cleaning", "home"]
  },
  {
    id: 18,
    title: "Nespresso Essenza Mini Coffee Machine with Aeroccino Milk Frother",
    brand: "Nespresso",
    category: "Home & Kitchen",
    price: 15499,
    original_price: 19999,
    discount: 22,
    rating: 4.8,
    reviews_count: 2300,
    image: "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Compact design without compromise. 19-bar high-pressure extraction extracts the rich aromas and delivers barista-quality espresso and velvety cappuccinos.",
    specs: {
      "Pressure": "19-bar extraction pump",
      "Heat-up Time": "Fast 25-second preheat",
      "Cup Sizes": "Espresso (40ml) and Lungo (110ml)",
      "Includes": "Aeroccino 3 frother + 14 complimentary capsule kit"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 68,
    tags: ["coffee", "espresso", "nespresso", "kitchen"]
  },
  {
    id: 19,
    title: "Fossil Gen 6 Smartwatch with Alexa Built-in (Smoke Stainless Steel)",
    brand: "Fossil",
    category: "Smart Watches & Wearables",
    price: 12495,
    original_price: 24995,
    discount: 50,
    rating: 4.1,
    reviews_count: 3100,
    image: "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Snapdragon Wear 4100+ platform for 30% boosted performance. Track SpO2, heart rate, cardio fitness score, and fast charge 80% in 30 minutes.",
    specs: {
      "Case Size": "44mm Smoke Stainless Steel",
      "Display": "1.28-inch Color AMOLED Touchscreen (326 ppi)",
      "Battery": "24+ Hr multi-day Extended Battery Modes"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 92,
    tags: ["fossil", "smartwatch", "wearables"]
  },
  {
    id: 20,
    title: "Ray-Ban Classic Aviator Polarized Sunglasses (Gold Frame / Green G-15)",
    brand: "Ray-Ban",
    category: "Fashion & Apparel",
    price: 9890,
    original_price: 12290,
    discount: 20,
    rating: 4.8,
    reviews_count: 4200,
    image: "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80"
    ],
    description: "The timeless American aviator designed in 1937 for aviators. Polarized crystal lenses eliminate 99% of reflected glare with 100% UV400 protection.",
    specs: {
      "Frame Material": "Metal Alloy (Polished Gold)",
      "Lenses": "Crystal Green Polarized G-15",
      "Size": "Standard 58mm lens / 14mm bridge"
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["sunglasses", "rayban", "aviator", "luxury"]
  },
  {
    id: 21,
    title: "Dell XPS 13 Plus Laptop (13.4\" 3.5K OLED Touch, Intel i7-1360P, 16GB/1TB)",
    brand: "Dell",
    category: "Laptops & Computers",
    price: 169990,
    original_price: 198900,
    discount: 15,
    rating: 4.5,
    reviews_count: 530,
    image: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Seamless glass touch pad, zero-lattice keyboard, capacitive touch function row, and jaw-dropping 3.5K OLED InfinityEdge touch screen.",
    specs: {
      "Display": "13.4-inch 3.5K (3456x2160) OLED Touch Anti-Reflective 400-nit",
      "Processor": "13th Gen Intel Core i7-1360P (12 cores, up to 5.0 GHz)",
      "RAM & SSD": "16GB LPDDR5 6000MHz / 1TB M.2 PCIe NVMe SSD",
      "Weight": "1.23 kg"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 45,
    tags: ["dell", "xps", "ultrabook", "oled"]
  },
  {
    id: 22,
    title: "Sony PlayStation 5 Console (Slim Disc Edition)",
    brand: "Sony",
    category: "Laptops & Computers",
    price: 54990,
    original_price: 59990,
    discount: 8,
    rating: 4.9,
    reviews_count: 12400,
    image: "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Experience lightning-fast loading with an ultra-high speed SSD, deeper immersion with haptic feedback, adaptive triggers and 3D Audio.",
    specs: {
      "Storage": "1TB Custom High-Speed NVMe SSD",
      "Graphics": "Ray Tracing Acceleration up to 4K 120Hz & 8K output",
      "Audio": "Tempest 3D AudioTech",
      "Includes": "DualSense Wireless Controller & Astro's Playroom game"
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["ps5", "playstation", "gaming", "console"]
  },
  {
    id: 23,
    title: "Puma Men's Smash v2 Leather Sneakers (White & Black)",
    brand: "Puma",
    category: "Footwear & Sneakers",
    price: 2199,
    original_price: 4499,
    discount: 51,
    rating: 4.3,
    reviews_count: 6200,
    image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Tennis-inspired look designed for everyday street style. Soft leather upper with clean stitching and durable non-marking rubber outsole.",
    specs: {
      "Upper": "Soft genuine leather",
      "Insole": "SoftFoam+ sockliner for instantaneous step-in comfort",
      "Outsole": "Herringbone pattern traction rubber",
      "Sizes Available": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10"]
    },
    in_stock: true,
    is_bestseller: true,
    is_deal: true,
    is_assured: true,
    fast_delivery: true,
    deal_claimed_percent: 76,
    tags: ["puma", "sneakers", "casual", "white"]
  },
  {
    id: 24,
    title: "Canon EOS R50 Mirrorless Camera with RF-S 18-45mm IS STM Lens",
    brand: "Canon",
    category: "Cameras & Photography",
    price: 58990,
    original_price: 68995,
    discount: 15,
    rating: 4.6,
    reviews_count: 890,
    image: "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=800&q=80",
    additional_images: [
      "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=800&q=80"
    ],
    description: "Compact and lightweight content creator camera. 24.2 MP APS-C sensor, uncropped 6K oversampled 4K 30p, and Dual Pixel CMOS AF II.",
    specs: {
      "Sensor": "24.2 Megapixel APS-C CMOS",
      "AF System": "Dual Pixel CMOS AF II with vehicle, animal and human detection",
      "Burst Rate": "Up to 15 fps electronic shutter",
      "Screen": "3.0-inch 1.62M dot Vari-angle Touch LCD"
    },
    in_stock: true,
    is_bestseller: false,
    is_deal: false,
    is_assured: true,
    fast_delivery: true,
    tags: ["canon", "vlogging", "camera", "mirrorless"]
  }
];

// Sample customer reviews data
const INITIAL_REVIEWS = {
  1: [
    { author: "Vikram Malhotra", rating: 5, date: "2 days ago", verified: true, title: "Best iPhone ever! Titanium feel is incredible", comment: "The weight reduction compared to the 14 Pro is noticeable immediately. The camera is pin sharp, battery lasts all day, and USB-C is finally here!" },
    { author: "Sneha Roy", rating: 4, date: "1 week ago", verified: true, title: "Premium phone, smooth 120Hz", comment: "Very happy with the purchase. Action button is super handy. Price is steep but trade-in made it reasonable." }
  ],
  6: [
    { author: "Aditya Sharma", rating: 5, date: "3 days ago", verified: true, title: "Unbeatable noise cancellation for flights & office", comment: "The XM5 is astonishingly quiet. Multipoint connects seamlessly between my laptop and phone. Very comfortable headband." },
    { author: "Kavita Rao", rating: 5, date: "2 weeks ago", verified: true, title: "Audio clarity 10/10", comment: "Listened to lossless audio and couldn't believe the separation. Call quality with mic is crisp." }
  ],
  11: [
    { author: "Rahul Verma", rating: 5, date: "Yesterday", verified: true, title: "Grail sneaker acquired!", comment: "Authentic pair with ShopX Assured tag. The vintage cracked leather accents look phenomenal in person." }
  ]
};

// Available coupons for checkout
const VALID_COUPONS = {
  "SHOPX100": { discountType: "fixed", value: 100, minOrder: 500, description: "Flat ₹100 OFF on orders above ₹500" },
  "FESTIVE20": { discountType: "percent", value: 20, maxDiscount: 1000, minOrder: 1500, description: "20% OFF up to ₹1,000" },
  "WELCOME50": { discountType: "fixed", value: 50, minOrder: 299, description: "Flat ₹50 OFF on first purchase" },
  "PRIMEPLUS": { discountType: "percent", value: 10, maxDiscount: 500, minOrder: 999, description: "10% OFF for ShopX Plus members" }
};
