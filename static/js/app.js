/**
 * ShopX - Core Application Logic
 * Amazon / Flipkart Inspired E-Commerce Application
 */

// Application State
const AppState = {
  products: [],
  filteredProducts: [],
  cart: [],
  wishlist: [],
  orders: [],
  categories: [],
  brands: [],
  
  // Active Filters & Sorting
  filters: {
    searchQuery: "",
    category: "All",
    minPrice: 0,
    maxPrice: 250000,
    minRating: 0,
    selectedBrands: new Set(),
    assuredOnly: false,
    dealsOnly: false
  },
  sortBy: "relevance",
  viewMode: "grid", // 'grid' or 'list'
  
  // Cart & Pricing
  activeCoupon: null,
  deliveryPincode: "110001",
  deliveryCity: "New Delhi",
  
  // Carousel State
  carouselIndex: 0,
  carouselTimer: null,
  
  // Theme
  theme: "light"
};

// Initial Setup on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  loadSavedState();
  initHeroCarousel();
  initDealsCountdown();
  initEventListeners();
  fetchProductsAndCategories();
});

/* ==========================================================================
   STATE PERSISTENCE (LOCAL STORAGE)
   ========================================================================== */
function loadSavedState() {
  try {
    const savedCart = localStorage.getItem("shopx_cart");
    if (savedCart) AppState.cart = JSON.parse(savedCart);

    const savedWishlist = localStorage.getItem("shopx_wishlist");
    if (savedWishlist) AppState.wishlist = JSON.parse(savedWishlist);

    const savedOrders = localStorage.getItem("shopx_orders");
    if (savedOrders) AppState.orders = JSON.parse(savedOrders);

    const savedPincode = localStorage.getItem("shopx_pincode");
    if (savedPincode) AppState.deliveryPincode = savedPincode;

    const savedCity = localStorage.getItem("shopx_city");
    if (savedCity) AppState.deliveryCity = savedCity;

    const savedUser = localStorage.getItem("shopx_logged_user");
    if (savedUser) {
      try {
        AppState.user = JSON.parse(savedUser);
      } catch (e) {
        AppState.user = null;
      }
    } else {
      AppState.user = null;
    }

    updateHeaderLocation();
    updateCartBadge();
    updateHeaderUserAuth();
  } catch (e) {
    console.error("Error loading localStorage state:", e);
  }
}

function updateHeaderUserAuth() {
  const container = document.getElementById("headerAccountBtn");
  if (!container) return;
  if (AppState.user && AppState.user.isLoggedIn) {
    const firstName = (AppState.user.name || "Shopper").split(" ")[0];
    container.innerHTML = `
      <span class="action-subtext">Hello, ${escapeHtml(firstName)}</span>
      <span class="action-maintext">Account & Lists ▾</span>
    `;
    container.onclick = toggleAccountMenu;
  } else {
    container.innerHTML = `
      <span class="action-subtext">Hello, sign in</span>
      <span class="action-maintext">Account & Lists ▾</span>
    `;
    container.onclick = () => { 
      window.location.href = window.location.pathname.endsWith(".html") ? "login.html" : "/login"; 
    };
  }
}

function toggleAccountMenu(event) {
  if (event) event.stopPropagation();
  let menu = document.getElementById("accountDropdownMenu");
  if (!menu) {
    menu = document.createElement("div");
    menu.id = "accountDropdownMenu";
    menu.className = "account-dropdown-menu";
    document.body.appendChild(menu);
  }

  const isVisible = menu.classList.contains("active");
  if (isVisible) {
    menu.classList.remove("active");
    return;
  }

  const btn = document.getElementById("headerAccountBtn");
  const rect = btn.getBoundingClientRect();
  menu.style.top = `${rect.bottom + window.scrollY + 6}px`;
  menu.style.right = `${window.innerWidth - rect.right}px`;

  menu.innerHTML = `
    <div style="padding: 12px 16px; border-bottom: 1px solid var(--border-subtle);">
      <div style="font-weight: 700; font-size: 13px;">${escapeHtml(AppState.user ? AppState.user.name : "User")}</div>
      <div style="font-size: 11px; color: var(--text-muted);">${escapeHtml(AppState.user ? AppState.user.email_phone : "")}</div>
    </div>
    <div style="padding: 6px 0;">
      <a href="#" onclick="openOrdersModal(); closeAccountMenu(); return false;" class="menu-item-link">📦 Your Orders</a>
      <a href="#" onclick="openWishlistModal(); closeAccountMenu(); return false;" class="menu-item-link">❤️ Your Wishlist</a>
      <a href="/admin" class="menu-item-link" style="color: #16a34a; font-weight: 700;">📊 View Excel Data Center</a>
      <a href="/admin/export-excel" class="menu-item-link" style="font-size: 12px;">📥 Download Excel Sheet (.xlsx)</a>
      <div style="border-top: 1px solid var(--border-subtle); margin: 6px 0;"></div>
      <a href="#" onclick="signOutUser(); return false;" class="menu-item-link" style="color: #dc2626;">Sign Out</a>
    </div>
  `;

  menu.classList.add("active");
}

function closeAccountMenu() {
  const menu = document.getElementById("accountDropdownMenu");
  if (menu) menu.classList.remove("active");
}

document.addEventListener("click", (e) => {
  if (!e.target.closest("#headerAccountBtn") && !e.target.closest("#accountDropdownMenu")) {
    closeAccountMenu();
  }
});

function signOutUser() {
  AppState.user = null;
  localStorage.removeItem("shopx_logged_user");
  document.cookie = "shopx_user_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;";
  closeAccountMenu();
  updateHeaderUserAuth();
  showToast("You have been signed out. Redirecting...", "info");
  setTimeout(() => {
    var isFileMode = window.location.protocol === "file:" || window.location.pathname.endsWith(".html");
    window.location.href = isFileMode ? "login.html" : "/login";
  }, 600);
}

function saveCartState() {
  localStorage.setItem("shopx_cart", JSON.stringify(AppState.cart));
  updateCartBadge();
}

function saveWishlistState() {
  localStorage.setItem("shopx_wishlist", JSON.stringify(AppState.wishlist));
}

function saveOrdersState() {
  localStorage.setItem("shopx_orders", JSON.stringify(AppState.orders));
}

/* ==========================================================================
   THEME TOGGLING (DARK / LIGHT)
   ========================================================================== */
function initTheme() {
  const savedTheme = localStorage.getItem("shopx_theme") || "light";
  AppState.theme = savedTheme;
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon();
}

function toggleTheme() {
  AppState.theme = AppState.theme === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", AppState.theme);
  localStorage.setItem("shopx_theme", AppState.theme);
  updateThemeIcon();
  showToast(`Switched to ${AppState.theme} mode`, "info");
}

function updateThemeIcon() {
  const btn = document.getElementById("themeToggleBtn");
  if (!btn) return;
  if (AppState.theme === "dark") {
    btn.innerHTML = `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>`;
  } else {
    btn.innerHTML = `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>`;
  }
}

/* ==========================================================================
   DATA FETCHING & INITIALIZATION
   ========================================================================== */
async function fetchProductsAndCategories() {
  renderLoadingState();
  try {
    // Attempt Flask API fetch
    const response = await fetch("/api/products");
    if (response.ok) {
      const data = await response.json();
      AppState.products = data.products || [];
    } else {
      throw new Error("API not available, fallback to client dataset");
    }
  } catch (err) {
    // Graceful fallback to client-side INITIAL_PRODUCTS
    console.log("Using client-side catalog dataset:", err.message);
    if (typeof INITIAL_PRODUCTS !== "undefined") {
      AppState.products = [...INITIAL_PRODUCTS];
    }
  }

  // Populate dynamic category and brand lists
  extractCategoriesAndBrands();
  renderCategoryRibbon();
  renderSidebarFilters();
  applyFiltersAndSort();
  renderDealsStrip();
  renderRecommendations();
  initShopbot();
}

function extractCategoriesAndBrands() {
  const catMap = new Map();
  const brandSet = new Set();

  AppState.products.forEach(p => {
    catMap.set(p.category, (catMap.get(p.category) || 0) + 1);
    if (p.brand) brandSet.add(p.brand);
  });

  AppState.categories = Array.from(catMap.entries()).map(([name, count]) => ({ name, count }));
  AppState.brands = Array.from(brandSet).sort();
}

/* ==========================================================================
   HERO CAROUSEL & LIGHTNING DEALS
   ========================================================================== */
function initHeroCarousel() {
  const slides = document.querySelectorAll(".carousel-slide");
  const dotsContainer = document.getElementById("carouselDots");
  if (!slides.length) return;

  // Create dot indicators
  if (dotsContainer) {
    dotsContainer.innerHTML = "";
    slides.forEach((_, idx) => {
      const dot = document.createElement("div");
      dot.className = `carousel-dot ${idx === 0 ? "active" : ""}`;
      dot.onclick = () => goToSlide(idx);
      dotsContainer.appendChild(dot);
    });
  }

  // Setup auto-play
  startCarouselAutoPlay();
}

function goToSlide(index) {
  const slides = document.querySelectorAll(".carousel-slide");
  const dots = document.querySelectorAll(".carousel-dot");
  if (!slides.length) return;

  slides.forEach(s => s.classList.remove("active"));
  dots.forEach(d => d.classList.remove("active"));

  AppState.carouselIndex = (index + slides.length) % slides.length;
  slides[AppState.carouselIndex].classList.add("active");
  if (dots[AppState.carouselIndex]) {
    dots[AppState.carouselIndex].classList.add("active");
  }
}

function nextSlide() {
  goToSlide(AppState.carouselIndex + 1);
}

function prevSlide() {
  goToSlide(AppState.carouselIndex - 1);
}

function startCarouselAutoPlay() {
  if (AppState.carouselTimer) clearInterval(AppState.carouselTimer);
  AppState.carouselTimer = setInterval(nextSlide, 5000);
}

// Lightning Deals Live Countdown Timer
function initDealsCountdown() {
  const timerElem = document.getElementById("dealsCountdownTimer");
  if (!timerElem) return;

  // Set deal end time to 4 hours from now
  let remainingSeconds = 4 * 3600 + 24 * 60 + 15;

  setInterval(() => {
    if (remainingSeconds > 0) {
      remainingSeconds--;
      const hours = Math.floor(remainingSeconds / 3600);
      const minutes = Math.floor((remainingSeconds % 3600) / 60);
      const seconds = remainingSeconds % 60;
      timerElem.textContent = `${padZero(hours)}h : ${padZero(minutes)}m : ${padZero(seconds)}s`;
    }
  }, 1000);
}

function padZero(num) {
  return num < 10 ? "0" + num : num;
}

function renderDealsStrip() {
  const container = document.getElementById("dealsHorizontalScroll");
  if (!container) return;

  const deals = AppState.products.filter(p => p.is_deal || p.discount >= 20).slice(0, 10);
  if (!deals.length) return;

  container.innerHTML = deals.map(p => `
    <div class="deal-card" onclick="openProductQuickView(${p.id})">
      <div class="deal-card-badge">${p.discount}% OFF</div>
      <img src="${p.image}" alt="${escapeHtml(p.title)}" class="deal-card-image" loading="lazy" />
      <div class="deal-card-title">${escapeHtml(p.title)}</div>
      <div class="deal-card-price-row">
        <span class="deal-card-price">₹${p.price.toLocaleString("en-IN")}</span>
        <span class="deal-card-mrp">₹${p.original_price.toLocaleString("en-IN")}</span>
      </div>
      <div class="deal-progress-bar-container">
        <div class="deal-progress-meta">
          <span>${p.deal_claimed_percent || 75}% Claimed</span>
          <span style="color: var(--discount-red);">Ends Soon</span>
        </div>
        <div class="deal-progress-track">
          <div class="deal-progress-fill" style="width: ${p.deal_claimed_percent || 75}%;"></div>
        </div>
      </div>
    </div>
  `).join("");
}

/* ==========================================================================
   CATEGORY RIBBON
   ========================================================================== */
function renderCategoryRibbon() {
  const container = document.getElementById("categoryRibbonList");
  if (!container) return;

  const categoryIcons = {
    "All": "⚡",
    "Mobiles & Tablets": "📱",
    "Laptops & Computers": "💻",
    "Audio & Headphones": "🎧",
    "Smart Watches & Wearables": "⌚",
    "Footwear & Sneakers": "👟",
    "Fashion & Apparel": "👕",
    "Cameras & Photography": "📷",
    "Home & Kitchen": "☕"
  };

  const categories = [{ name: "All", count: AppState.products.length }, ...AppState.categories];

  container.innerHTML = categories.map(cat => {
    const isActive = AppState.filters.category === cat.name;
    const icon = categoryIcons[cat.name] || "🛍️";
    return `
      <div class="category-pill-item ${isActive ? "active" : ""}" onclick="selectCategory('${cat.name}')">
        <div class="category-icon-circle">${icon}</div>
        <span class="category-name">${cat.name}</span>
      </div>
    `;
  }).join("");
}

function selectCategory(categoryName) {
  AppState.filters.category = categoryName;
  const select = document.getElementById("searchCategorySelect");
  if (select) select.value = categoryName;

  renderCategoryRibbon();
  renderSidebarFilters();
  applyFiltersAndSort();

  // Scroll smoothly to products section
  const catalogElem = document.getElementById("productsCatalogAnchor");
  if (catalogElem) {
    catalogElem.scrollIntoView({ behavior: "smooth" });
  }
}

/* ==========================================================================
   SIDEBAR FILTERS RENDERING
   ========================================================================== */
function renderSidebarFilters() {
  // 1. Categories Filter List
  const catList = document.getElementById("sidebarCategoryFilterList");
  if (catList) {
    const categories = [{ name: "All", count: AppState.products.length }, ...AppState.categories];
    catList.innerHTML = categories.map(cat => {
      const active = AppState.filters.category === cat.name ? "active" : "";
      return `
        <div class="category-filter-item ${active}" onclick="selectCategory('${cat.name}')">
          <span>${cat.name}</span>
          <span class="category-filter-count">${cat.count}</span>
        </div>
      `;
    }).join("");
  }

  // 2. Brands Checkboxes
  const brandsList = document.getElementById("sidebarBrandsList");
  if (brandsList) {
    brandsList.innerHTML = AppState.brands.map(brand => {
      const isChecked = AppState.filters.selectedBrands.has(brand) ? "checked" : "";
      return `
        <label class="checkbox-label">
          <input type="checkbox" value="${brand}" ${isChecked} onchange="toggleBrandFilter('${brand}')" />
          <span>${brand}</span>
        </label>
      `;
    }).join("");
  }

  // 3. Price inputs
  const minInput = document.getElementById("priceMinInput");
  const maxInput = document.getElementById("priceMaxInput");
  const rangeInput = document.getElementById("priceRangeSlider");
  if (minInput && maxInput && rangeInput) {
    minInput.value = AppState.filters.minPrice;
    maxInput.value = AppState.filters.maxPrice;
    rangeInput.value = AppState.filters.maxPrice;
  }
}

function toggleBrandFilter(brand) {
  if (AppState.filters.selectedBrands.has(brand)) {
    AppState.filters.selectedBrands.delete(brand);
  } else {
    AppState.filters.selectedBrands.add(brand);
  }
  applyFiltersAndSort();
}

function onPriceRangeChange(val) {
  AppState.filters.maxPrice = Number(val);
  const maxInput = document.getElementById("priceMaxInput");
  if (maxInput) maxInput.value = val;
  applyFiltersAndSort();
}

function onMinPriceInputChange(val) {
  AppState.filters.minPrice = Number(val) || 0;
  applyFiltersAndSort();
}

function onMaxPriceInputChange(val) {
  AppState.filters.maxPrice = Number(val) || 250000;
  const slider = document.getElementById("priceRangeSlider");
  if (slider) slider.value = AppState.filters.maxPrice;
  applyFiltersAndSort();
}

function setRatingFilter(minStars) {
  AppState.filters.minRating = AppState.filters.minRating === minStars ? 0 : minStars;
  applyFiltersAndSort();
}

function toggleAssuredFilter() {
  const checkbox = document.getElementById("assuredToggleCheckbox");
  AppState.filters.assuredOnly = checkbox ? checkbox.checked : !AppState.filters.assuredOnly;
  applyFiltersAndSort();
}

function clearAllFilters() {
  AppState.filters.searchQuery = "";
  AppState.filters.category = "All";
  AppState.filters.minPrice = 0;
  AppState.filters.maxPrice = 250000;
  AppState.filters.minRating = 0;
  AppState.filters.selectedBrands.clear();
  AppState.filters.assuredOnly = false;
  AppState.filters.dealsOnly = false;

  const searchInput = document.getElementById("searchInputField");
  if (searchInput) searchInput.value = "";
  const clearBtn = document.getElementById("clearSearchBtn");
  if (clearBtn) clearBtn.style.display = "none";

  const assuredBox = document.getElementById("assuredToggleCheckbox");
  if (assuredBox) assuredBox.checked = false;

  renderCategoryRibbon();
  renderSidebarFilters();
  applyFiltersAndSort();
  showToast("All filters cleared", "info");
}

/* ==========================================================================
   FILTERING & SORTING LOGIC
   ========================================================================== */
function applyFiltersAndSort() {
  let list = [...AppState.products];

  // 1. Search Query Filter
  if (AppState.filters.searchQuery) {
    const q = AppState.filters.searchQuery.toLowerCase().trim();
    list = list.filter(p => {
      const matchTitle = p.title.toLowerCase().includes(q);
      const matchBrand = p.brand.toLowerCase().includes(q);
      const matchCategory = p.category.toLowerCase().includes(q);
      const matchTags = (p.tags || []).some(t => t.toLowerCase().includes(q));
      return matchTitle || matchBrand || matchCategory || matchTags;
    });
  }

  // 2. Category Filter
  if (AppState.filters.category && AppState.filters.category !== "All") {
    list = list.filter(p => p.category === AppState.filters.category);
  }

  // 3. Price Range Filter
  list = list.filter(p => p.price >= AppState.filters.minPrice && p.price <= AppState.filters.maxPrice);

  // 4. Rating Filter
  if (AppState.filters.minRating > 0) {
    list = list.filter(p => p.rating >= AppState.filters.minRating);
  }

  // 5. Brands Filter
  if (AppState.filters.selectedBrands.size > 0) {
    list = list.filter(p => AppState.filters.selectedBrands.has(p.brand));
  }

  // 6. ShopX Assured
  if (AppState.filters.assuredOnly) {
    list = list.filter(p => p.is_assured);
  }

  // 7. Deals Only
  if (AppState.filters.dealsOnly) {
    list = list.filter(p => p.is_deal);
  }

  // 8. Sorting
  if (AppState.sortBy === "price_asc") {
    list.sort((a, b) => a.price - b.price);
  } else if (AppState.sortBy === "price_desc") {
    list.sort((a, b) => b.price - a.price);
  } else if (AppState.sortBy === "rating") {
    list.sort((a, b) => b.rating - a.rating || b.reviews_count - a.reviews_count);
  } else if (AppState.sortBy === "discount") {
    list.sort((a, b) => b.discount - a.discount);
  } else if (AppState.sortBy === "newest") {
    list.sort((a, b) => b.id - a.id);
  } else {
    // Relevance: bestsellers & deals on top
    list.sort((a, b) => (b.is_bestseller ? 1 : 0) - (a.is_bestseller ? 1 : 0) || b.rating - a.rating);
  }

  AppState.filteredProducts = list;
  renderActiveFilterChips();
  renderProductsGrid();
}

function onSortChange(newSort) {
  AppState.sortBy = newSort;
  applyFiltersAndSort();
}

function setViewMode(mode) {
  AppState.viewMode = mode;
  const gridBtn = document.getElementById("viewGridBtn");
  const listBtn = document.getElementById("viewListBtn");
  const gridContainer = document.getElementById("productsGrid");

  if (gridBtn && listBtn && gridContainer) {
    if (mode === "list") {
      listBtn.classList.add("active");
      gridBtn.classList.remove("active");
      gridContainer.classList.add("list-view");
    } else {
      gridBtn.classList.add("active");
      listBtn.classList.remove("active");
      gridContainer.classList.remove("list-view");
    }
  }
}

/* ==========================================================================
   ACTIVE FILTER CHIPS BAR
   ========================================================================== */
function renderActiveFilterChips() {
  const container = document.getElementById("activeFilterChipsBar");
  if (!container) return;

  const chips = [];

  if (AppState.filters.category !== "All") {
    chips.push({ label: `Category: ${AppState.filters.category}`, onRemove: () => selectCategory("All") });
  }

  if (AppState.filters.searchQuery) {
    chips.push({ label: `Search: "${AppState.filters.searchQuery}"`, onRemove: () => onSearchClear() });
  }

  if (AppState.filters.maxPrice < 250000 || AppState.filters.minPrice > 0) {
    chips.push({
      label: `Price: ₹${AppState.filters.minPrice.toLocaleString("en-IN")} - ₹${AppState.filters.maxPrice.toLocaleString("en-IN")}`,
      onRemove: () => {
        AppState.filters.minPrice = 0;
        AppState.filters.maxPrice = 250000;
        renderSidebarFilters();
        applyFiltersAndSort();
      }
    });
  }

  if (AppState.filters.minRating > 0) {
    chips.push({ label: `${AppState.filters.minRating}★ & above`, onRemove: () => setRatingFilter(0) });
  }

  AppState.filters.selectedBrands.forEach(brand => {
    chips.push({ label: brand, onRemove: () => toggleBrandFilter(brand) });
  });

  if (AppState.filters.assuredOnly) {
    chips.push({ label: "ShopX Assured", onRemove: () => toggleAssuredFilter() });
  }

  if (chips.length === 0) {
    container.innerHTML = "";
    return;
  }

  container.innerHTML = chips.map((c, i) => `
    <div class="filter-chip">
      <span>${escapeHtml(c.label)}</span>
      <button onclick="window.activeChipRemoveCallbacks[${i}]()">×</button>
    </div>
  `).join("") + `
    <button class="clear-all-filters-btn" style="margin-left: 8px;" onclick="clearAllFilters()">Clear all</button>
  `;

  window.activeChipRemoveCallbacks = chips.map(c => c.onRemove);
}

/* ==========================================================================
   PRODUCT GRID RENDERING
   ========================================================================== */
function renderProductsGrid() {
  const countElem = document.getElementById("resultsCountDisplay");
  const gridContainer = document.getElementById("productsGrid");
  if (!gridContainer) return;

  const count = AppState.filteredProducts.length;
  if (countElem) {
    countElem.innerHTML = `Showing <b>${count}</b> ${count === 1 ? "product" : "products"}`;
  }

  if (count === 0) {
    gridContainer.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 60px 20px; text-align: center; background: var(--bg-surface); border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
        <div style="font-size: 48px; margin-bottom: 12px;">🔍</div>
        <h3 style="font-size: 18px; font-weight: 700; margin-bottom: 8px;">No matching products found</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px;">Try adjusting your search terms or clearing some filters.</p>
        <button class="slide-cta-btn" onclick="clearAllFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  gridContainer.innerHTML = AppState.filteredProducts.map(p => {
    const isWishlisted = AppState.wishlist.some(w => w.id === p.id);
    const cartItem = AppState.cart.find(c => c.id === p.id);
    const qty = cartItem ? cartItem.quantity : 0;

    let badgeHtml = "";
    if (p.is_bestseller) {
      badgeHtml = `<span class="card-badge-tag bestseller">Bestseller</span>`;
    } else if (p.is_deal) {
      badgeHtml = `<span class="card-badge-tag deal">Deal of the Day</span>`;
    }

    return `
      <div class="product-card" id="productCard-${p.id}">
        <button class="wishlist-toggle-btn ${isWishlisted ? "active" : ""}" title="Add to Wishlist" onclick="toggleWishlist(${p.id}, event)">
          <svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
        </button>

        <div class="product-image-container" onclick="openProductQuickView(${p.id})">
          ${badgeHtml}
          <img src="${p.image}" alt="${escapeHtml(p.title)}" class="product-thumb-img" loading="lazy" />
          <button class="quick-view-overlay-btn">Quick View</button>
        </div>

        <div class="product-info-box">
          <div class="product-brand-tag">${escapeHtml(p.brand)}</div>
          <div class="product-card-title" onclick="openProductQuickView(${p.id})">${escapeHtml(p.title)}</div>

          <div class="product-card-rating-row">
            <span class="rating-pill-green">
              ${p.rating}
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </span>
            <span class="review-count-text">(${p.reviews_count.toLocaleString()})</span>
            ${p.is_assured ? `<span class="assured-inline-badge">Shop<b>X</b> <span>Assured</span></span>` : ""}
          </div>

          <div class="product-price-block">
            <span class="product-current-price">₹${p.price.toLocaleString("en-IN")}</span>
            <span class="product-original-mrp">₹${p.original_price.toLocaleString("en-IN")}</span>
            <span class="product-discount-percentage">${p.discount}% off</span>
          </div>

          <div class="delivery-badge-text">
            <span>🚚</span>
            <span>Get it by <b>Tomorrow</b></span>
          </div>

          <div class="product-card-actions" id="cardActions-${p.id}">
            ${qty > 0 ? `
              <div class="quantity-stepper">
                <button class="qty-step-btn" onclick="updateCartItemQty(${p.id}, ${qty - 1})">-</button>
                <span class="qty-display-num">${qty}</span>
                <button class="qty-step-btn" onclick="updateCartItemQty(${p.id}, ${qty + 1})">+</button>
              </div>
            ` : `
              <button class="add-to-cart-btn" onclick="addToCart(${p.id})">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
                Add to Cart
              </button>
            `}
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function renderLoadingState() {
  const gridContainer = document.getElementById("productsGrid");
  if (!gridContainer) return;
  gridContainer.innerHTML = Array(8).fill(0).map(() => `
    <div class="product-card" style="opacity: 0.6; min-height: 380px;">
      <div class="product-image-container" style="background-color: var(--border-subtle); animation: pulse 1.5s infinite;"></div>
      <div class="product-info-box">
        <div style="height: 14px; width: 40%; background: var(--border-subtle); margin-bottom: 8px; border-radius: 4px;"></div>
        <div style="height: 18px; width: 90%; background: var(--border-subtle); margin-bottom: 8px; border-radius: 4px;"></div>
        <div style="height: 18px; width: 60%; background: var(--border-subtle); margin-bottom: 12px; border-radius: 4px;"></div>
        <div style="height: 24px; width: 50%; background: var(--border-subtle); margin-top: auto; border-radius: 4px;"></div>
      </div>
    </div>
  `).join("");
}

/* ==========================================================================
   PRODUCT DETAILS & QUICK VIEW MODAL
   ========================================================================== */
function openProductQuickView(productId) {
  const product = AppState.products.find(p => p.id === productId);
  if (!product) return;

  const modal = document.getElementById("quickViewModal");
  const content = document.getElementById("quickViewModalContent");
  if (!modal || !content) return;

  const images = [product.image, ...(product.additional_images || [])];
  const reviews = (typeof INITIAL_REVIEWS !== "undefined" && INITIAL_REVIEWS[product.id]) ? INITIAL_REVIEWS[product.id] : [
    { author: "Rohan Khanna", rating: 5, date: "3 days ago", verified: true, title: "Superb product!", comment: "Delivered within 24 hours. Pristine packaging and exactly as described." }
  ];

  content.innerHTML = `
    <div class="quickview-layout">
      <!-- Gallery Column -->
      <div class="quickview-gallery">
        <div class="quickview-main-image-wrap">
          <img id="quickviewMainImg" src="${product.image}" alt="${escapeHtml(product.title)}" class="quickview-main-img" />
        </div>
        <div class="quickview-thumbnails-row">
          ${images.map((img, idx) => `
            <div class="quickview-thumb-item ${idx === 0 ? "active" : ""}" onclick="switchQuickViewImage('${img}', this)">
              <img src="${img}" alt="Thumbnail ${idx}" />
            </div>
          `).join("")}
        </div>
      </div>

      <!-- Details Column -->
      <div class="quickview-details">
        <div>
          <span class="product-brand-tag">${escapeHtml(product.brand)}</span>
          <h2 class="quickview-title">${escapeHtml(product.title)}</h2>
        </div>

        <div class="product-card-rating-row">
          <span class="rating-pill-green">
            ${product.rating} ★
          </span>
          <span class="review-count-text">(${product.reviews_count.toLocaleString()} customer ratings)</span>
          ${product.is_assured ? `<span class="assured-inline-badge">Shop<b>X</b> <span>Assured</span></span>` : ""}
        </div>

        <div class="product-price-block" style="margin: 8px 0;">
          <span class="product-current-price" style="font-size: 26px;">₹${product.price.toLocaleString("en-IN")}</span>
          <span class="product-original-mrp" style="font-size: 16px;">₹${product.original_price.toLocaleString("en-IN")}</span>
          <span class="product-discount-percentage" style="font-size: 16px;">${product.discount}% OFF</span>
        </div>

        <p style="color: var(--text-muted); font-size: 13px; line-height: 1.5;">${escapeHtml(product.description)}</p>

        <!-- Variants (Colors / Sizes) -->
        ${product.specs && product.specs.Colors ? `
          <div>
            <div style="font-size: 12px; font-weight: 700; margin-bottom: 6px;">Available Colors:</div>
            <div class="variants-row">
              ${product.specs.Colors.map((color, i) => `
                <div class="variant-pill ${i === 0 ? "active" : ""}" onclick="selectVariant(this)">${color}</div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        ${product.specs && product.specs["Sizes Available"] ? `
          <div>
            <div style="font-size: 12px; font-weight: 700; margin-bottom: 6px;">Select Size:</div>
            <div class="variants-row">
              ${product.specs["Sizes Available"].map((sz, i) => `
                <div class="variant-pill ${i === 0 ? "active" : ""}" onclick="selectVariant(this)">${sz}</div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Pincode Delivery Check -->
        <div class="pincode-check-card">
          <div style="font-size: 12px; font-weight: 700;">Check Delivery & Services:</div>
          <div class="pincode-form-row">
            <input type="text" id="quickviewPincodeInput" class="pincode-input-box" placeholder="Enter 6 digit pincode" value="${AppState.deliveryPincode}" maxlength="6" />
            <button class="pincode-check-btn" onclick="checkProductPincode()">Check</button>
          </div>
          <div id="pincodeFeedback" class="pincode-feedback-msg">
            ✓ Delivery by <b>Tomorrow, 11:00 AM</b> | <span style="color: var(--rating-green);">FREE Delivery</span>
          </div>
        </div>

        <!-- Specifications Table -->
        ${product.specs ? `
          <div>
            <div style="font-size: 13px; font-weight: 700; margin-bottom: 6px;">Key Highlights:</div>
            <table class="specs-table">
              ${Object.entries(product.specs).map(([k, v]) => Array.isArray(v) ? "" : `
                <tr>
                  <td>${k}</td>
                  <td>${v}</td>
                </tr>
              `).join("")}
            </table>
          </div>
        ` : ""}

        <!-- Action CTA Buttons -->
        <div class="quickview-actions-row">
          <button class="add-to-cart-btn" style="padding: 14px; font-size: 14px;" onclick="addToCart(${product.id}); closeQuickViewModal();">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
            Add to Cart
          </button>
          <button class="btn-buy-now" onclick="buyNowDirect(${product.id})">
            ⚡ Buy Now
          </button>
        </div>
      </div>

      <!-- Customer Reviews Section -->
      <div class="customer-reviews-section">
        <div class="reviews-header">
          <h3 style="font-size: 16px; font-weight: 800;">Customer Reviews (${reviews.length})</h3>
          <button class="write-review-btn" onclick="openWriteReviewBox(${product.id})">+ Write a Review</button>
        </div>

        <!-- Write Review Form Container (Hidden by default) -->
        <div id="writeReviewFormWrap" style="display: none; background: var(--bg-page); padding: 16px; border-radius: var(--radius-md); margin-bottom: 20px;">
          <h4 style="font-size: 14px; font-weight: 700; margin-bottom: 10px;">Share your experience with this product</h4>
          <div style="display: flex; gap: 8px; margin-bottom: 12px; align-items: center;">
            <span style="font-size: 12px; font-weight: 600;">Your Rating:</span>
            <div id="newReviewStarRating" style="cursor: pointer; font-size: 20px; color: var(--amazon-amber);">
              <span onclick="setReviewRating(1)">★</span>
              <span onclick="setReviewRating(2)">★</span>
              <span onclick="setReviewRating(3)">★</span>
              <span onclick="setReviewRating(4)">★</span>
              <span onclick="setReviewRating(5)">★</span>
            </div>
          </div>
          <input type="text" id="newReviewTitle" class="form-field-group input" placeholder="Review Headline" style="width: 100%; padding: 8px; margin-bottom: 8px; border-radius: 4px; border: 1px solid var(--border-strong);" />
          <textarea id="newReviewComment" rows="3" placeholder="Write your review comments here..." style="width: 100%; padding: 8px; margin-bottom: 12px; border-radius: 4px; border: 1px solid var(--border-strong); font-family: inherit;"></textarea>
          <div style="display: flex; gap: 8px; justify-content: flex-end;">
            <button onclick="document.getElementById('writeReviewFormWrap').style.display='none'" style="padding: 6px 12px; border-radius: 4px; background: var(--border-subtle);">Cancel</button>
            <button onclick="submitProductReview(${product.id})" style="padding: 6px 16px; border-radius: 4px; background: var(--flipkart-blue); color: #fff; font-weight: 700;">Submit Review</button>
          </div>
        </div>

        <div class="reviews-list-container" id="productReviewsList">
          ${reviews.map(r => `
            <div class="review-item-card">
              <div class="review-author-row">
                <span class="rating-pill-green">${r.rating} ★</span>
                <span class="review-author-name">${escapeHtml(r.author)}</span>
                ${r.verified ? `<span class="verified-buyer-tag">✓ Verified Purchase</span>` : ""}
                <span style="margin-left: auto; font-size: 11px; color: var(--text-muted);">${r.date}</span>
              </div>
              <div class="review-title">${escapeHtml(r.title)}</div>
              <div class="review-comment">${escapeHtml(r.comment)}</div>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeQuickViewModal() {
  const modal = document.getElementById("quickViewModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
}

function switchQuickViewImage(imgSrc, thumbElem) {
  const mainImg = document.getElementById("quickviewMainImg");
  if (mainImg) mainImg.src = imgSrc;
  document.querySelectorAll(".quickview-thumb-item").forEach(t => t.classList.remove("active"));
  if (thumbElem) thumbElem.classList.add("active");
}

function selectVariant(pillElem) {
  const parent = pillElem.parentElement;
  parent.querySelectorAll(".variant-pill").forEach(p => p.classList.remove("active"));
  pillElem.classList.add("active");
}

function checkProductPincode() {
  const input = document.getElementById("quickviewPincodeInput");
  const feedback = document.getElementById("pincodeFeedback");
  if (!input || !feedback) return;
  const pin = input.value.trim();

  if (/^\d{6}$/.test(pin)) {
    AppState.deliveryPincode = pin;
    saveCartState();
    feedback.innerHTML = `✓ Fast Delivery to <b>${pin}</b> by <b>Tomorrow</b> | <span style="color: var(--rating-green);">Eligible for FREE Delivery</span>`;
    showToast(`Pincode ${pin} is serviceable!`, "success");
  } else {
    feedback.innerHTML = `<span style="color: var(--discount-red);">Please enter a valid 6-digit postal pincode.</span>`;
  }
}

let selectedReviewRating = 5;
function setReviewRating(stars) {
  selectedReviewRating = stars;
  const starElems = document.querySelectorAll("#newReviewStarRating span");
  starElems.forEach((elem, idx) => {
    elem.style.color = idx < stars ? "var(--amazon-amber)" : "var(--border-strong)";
  });
}

function openWriteReviewBox() {
  const wrap = document.getElementById("writeReviewFormWrap");
  if (wrap) wrap.style.display = wrap.style.display === "none" ? "block" : "none";
}

function submitProductReview(productId) {
  const title = document.getElementById("newReviewTitle").value.trim();
  const comment = document.getElementById("newReviewComment").value.trim();
  if (!comment) {
    showToast("Please enter review comments", "warning");
    return;
  }

  const newReview = {
    author: "Raghav (You)",
    rating: selectedReviewRating,
    date: "Just now",
    verified: true,
    title: title || "Great experience",
    comment: comment
  };

  const list = document.getElementById("productReviewsList");
  if (list) {
    const revHtml = `
      <div class="review-item-card" style="animation: toastIn 0.3s ease;">
        <div class="review-author-row">
          <span class="rating-pill-green">${newReview.rating} ★</span>
          <span class="review-author-name">${newReview.author}</span>
          <span class="verified-buyer-tag">✓ Verified Purchase</span>
          <span style="margin-left: auto; font-size: 11px; color: var(--text-muted);">${newReview.date}</span>
        </div>
        <div class="review-title">${escapeHtml(newReview.title)}</div>
        <div class="review-comment">${escapeHtml(newReview.comment)}</div>
      </div>
    `;
    list.insertAdjacentHTML("afterbegin", revHtml);
  }

  document.getElementById("writeReviewFormWrap").style.display = "none";
  showToast("Thank you! Your review has been published.", "success");
}

/* ==========================================================================
   SHOPPING CART LOGIC & DRAWER
   ========================================================================== */
function addToCart(productId) {
  const product = AppState.products.find(p => p.id === productId);
  if (!product) return;

  const existing = AppState.cart.find(item => item.id === productId);
  if (existing) {
    existing.quantity += 1;
  } else {
    AppState.cart.push({
      id: product.id,
      title: product.title,
      price: product.price,
      original_price: product.original_price,
      image: product.image,
      brand: product.brand,
      quantity: 1
    });
  }

  saveCartState();
  updateProductCardAction(productId);
  renderCartDrawer();
  renderRecommendations();
  showToast(`Added "${product.title.slice(0, 30)}..." to Cart!`, "success");

  // Real-time Excel Logging on host PC!
  try {
    fetch("/api/track/cart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customer_name: AppState.user ? AppState.user.name : "Guest Shopper",
        product_id: product.id,
        title: product.title,
        brand: product.brand,
        quantity: 1,
        price: product.price,
        action: "ADDED"
      })
    });
  } catch (err) {
    console.log("Cart log offline:", err);
  }
}

function buyNowDirect(productId) {
  addToCart(productId);
  closeQuickViewModal();
  openCheckoutModal();
}

function updateCartItemQty(productId, newQty) {
  if (newQty <= 0) {
    removeFromCart(productId);
    return;
  }
  const item = AppState.cart.find(i => i.id === productId);
  if (item) {
    item.quantity = newQty;
    saveCartState();
    updateProductCardAction(productId);
    renderCartDrawer();
  }
}

function removeFromCart(productId) {
  const item = AppState.cart.find(i => i.id === productId);
  AppState.cart = AppState.cart.filter(item => item.id !== productId);
  saveCartState();
  updateProductCardAction(productId);
  renderCartDrawer();
  showToast("Item removed from cart", "info");

  // Real-time Excel Logging of item removal
  if (item) {
    try {
      fetch("/api/track/cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_name: AppState.user ? AppState.user.name : "Guest Shopper",
          product_id: productId,
          title: item.title,
          brand: item.brand,
          quantity: 0,
          price: item.price,
          action: "REMOVED"
        })
      });
    } catch (err) {}
  }
}

function updateProductCardAction(productId) {
  const container = document.getElementById(`cardActions-${productId}`);
  if (!container) return;

  const cartItem = AppState.cart.find(c => c.id === productId);
  const qty = cartItem ? cartItem.quantity : 0;

  if (qty > 0) {
    container.innerHTML = `
      <div class="quantity-stepper">
        <button class="qty-step-btn" onclick="updateCartItemQty(${productId}, ${qty - 1})">-</button>
        <span class="qty-display-num">${qty}</span>
        <button class="qty-step-btn" onclick="updateCartItemQty(${productId}, ${qty + 1})">+</button>
      </div>
    `;
  } else {
    container.innerHTML = `
      <button class="add-to-cart-btn" onclick="addToCart(${productId})">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
        Add to Cart
      </button>
    `;
  }
}

function updateCartBadge() {
  const totalCount = AppState.cart.reduce((sum, item) => sum + item.quantity, 0);
  const badges = document.querySelectorAll(".cart-badge-count");
  badges.forEach(b => {
    b.textContent = totalCount;
  });
}

function toggleCartDrawer() {
  const drawer = document.getElementById("cartDrawerOverlay");
  if (!drawer) return;
  const isOpen = drawer.classList.contains("active");
  if (isOpen) {
    drawer.classList.remove("active");
    document.body.style.overflow = "";
  } else {
    renderCartDrawer();
    drawer.classList.add("active");
    document.body.style.overflow = "hidden";
  }
}

function renderCartDrawer() {
  const itemsContainer = document.getElementById("cartItemsList");
  const countBadge = document.getElementById("cartDrawerItemsCount");
  const meterElem = document.getElementById("freeDeliveryMeter");
  const billWrap = document.getElementById("cartBillSummary");
  if (!itemsContainer) return;

  const totalCount = AppState.cart.reduce((s, i) => s + i.quantity, 0);
  if (countBadge) countBadge.textContent = `(${totalCount} ${totalCount === 1 ? "item" : "items"})`;

  if (AppState.cart.length === 0) {
    itemsContainer.innerHTML = `
      <div class="empty-cart-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
        <h3 style="font-size: 16px; font-weight: 700; color: var(--text-main);">Your ShopX Cart is empty</h3>
        <p style="font-size: 13px;">Explore today's top picks and add deals to your cart.</p>
        <button class="slide-cta-btn" onclick="toggleCartDrawer()" style="margin-top: 8px;">Start Shopping</button>
      </div>
    `;
    if (meterElem) meterElem.style.display = "none";
    if (billWrap) billWrap.style.display = "none";
    return;
  }

  // Render items
  itemsContainer.innerHTML = AppState.cart.map(item => `
    <div class="cart-item-row">
      <img src="${item.image}" alt="${escapeHtml(item.title)}" class="cart-item-thumb" />
      <div class="cart-item-details">
        <div class="cart-item-title">${escapeHtml(item.title)}</div>
        <div class="cart-item-price">₹${item.price.toLocaleString("en-IN")}</div>
        <div class="cart-item-controls">
          <div class="quantity-stepper" style="padding: 2px 6px;">
            <button class="qty-step-btn" style="width: 22px; height: 22px; font-size: 13px;" onclick="updateCartItemQty(${item.id}, ${item.quantity - 1})">-</button>
            <span class="qty-display-num" style="font-size: 12px; margin: 0 8px;">${item.quantity}</span>
            <button class="qty-step-btn" style="width: 22px; height: 22px; font-size: 13px;" onclick="updateCartItemQty(${item.id}, ${item.quantity + 1})">+</button>
          </div>
          <button class="cart-remove-item-btn" onclick="removeFromCart(${item.id})">Delete</button>
        </div>
      </div>
    </div>
  `).join("");

  // Price Calculation
  const subtotal = AppState.cart.reduce((s, i) => s + (i.price * i.quantity), 0);
  const totalMrp = AppState.cart.reduce((s, i) => s + ((i.original_price || i.price * 1.25) * i.quantity), 0);
  const productDiscount = totalMrp - subtotal;
  const isFreeDelivery = subtotal >= 499;
  const deliveryFee = isFreeDelivery ? 0 : 49;

  let couponDiscount = 0;
  if (AppState.activeCoupon) {
    if (AppState.activeCoupon.discountType === "fixed") {
      couponDiscount = AppState.activeCoupon.value;
    } else if (AppState.activeCoupon.discountType === "percent") {
      couponDiscount = Math.min((subtotal * AppState.activeCoupon.value) / 100, AppState.activeCoupon.maxDiscount || 1000);
    }
  }

  const finalTotal = Math.max(0, subtotal - couponDiscount + deliveryFee);
  const totalSavings = productDiscount + couponDiscount;

  // Free delivery meter
  if (meterElem) {
    meterElem.style.display = "flex";
    if (isFreeDelivery) {
      meterElem.innerHTML = `<span>🎉</span> <span>Your order qualifies for <b>FREE Delivery!</b></span>`;
    } else {
      const remaining = 499 - subtotal;
      meterElem.innerHTML = `<span>🚚</span> <span>Add <b>₹${remaining.toLocaleString("en-IN")}</b> more for <b>FREE Delivery</b>!</span>`;
    }
  }

  // Bill Breakdown
  if (billWrap) {
    billWrap.style.display = "flex";
    billWrap.innerHTML = `
      <div class="cart-bill-row">
        <span>Total MRP (${totalCount} items)</span>
        <span>₹${Math.round(totalMrp).toLocaleString("en-IN")}</span>
      </div>
      <div class="cart-bill-row" style="color: var(--rating-green);">
        <span>Product Discount</span>
        <span>- ₹${Math.round(productDiscount).toLocaleString("en-IN")}</span>
      </div>
      ${couponDiscount > 0 ? `
        <div class="cart-bill-row" style="color: var(--rating-green);">
          <span>Coupon (${AppState.activeCoupon.code})</span>
          <span>- ₹${Math.round(couponDiscount).toLocaleString("en-IN")}</span>
        </div>
      ` : ""}
      <div class="cart-bill-row">
        <span>Delivery Charges</span>
        <span>${isFreeDelivery ? '<span style="color: var(--rating-green); font-weight: 700;">FREE</span>' : '₹49'}</span>
      </div>
      <div class="cart-bill-row total">
        <span>Total Amount</span>
        <span>₹${Math.round(finalTotal).toLocaleString("en-IN")}</span>
      </div>
      <div style="font-size: 11px; font-weight: 700; color: var(--rating-green); text-align: center;">
        You will save ₹${Math.round(totalSavings).toLocaleString("en-IN")} on this order
      </div>
    `;
  }
}

/* ==========================================================================
   COUPONS
   ========================================================================== */
function applyCouponCode(manualCode) {
  const input = document.getElementById("couponInputBox");
  const code = (manualCode || (input ? input.value : "")).trim().toUpperCase();
  if (!code) {
    showToast("Please enter a coupon code", "warning");
    return;
  }

  const subtotal = AppState.cart.reduce((s, i) => s + (i.price * i.quantity), 0);

  const couponsMap = (typeof VALID_COUPONS !== "undefined") ? VALID_COUPONS : {
    "SHOPX100": { discountType: "fixed", value: 100, minOrder: 500, description: "Flat ₹100 OFF on orders above ₹500" },
    "FESTIVE20": { discountType: "percent", value: 20, maxDiscount: 1000, minOrder: 1500, description: "20% OFF up to ₹1,000" },
    "WELCOME50": { discountType: "fixed", value: 50, minOrder: 299, description: "Flat ₹50 OFF on first purchase" },
    "PRIMEPLUS": { discountType: "percent", value: 10, maxDiscount: 500, minOrder: 999, description: "10% OFF for ShopX Plus members" }
  };

  const coupon = couponsMap[code];
  if (!coupon) {
    showToast("Invalid coupon code", "warning");
    return;
  }

  if (subtotal < coupon.minOrder) {
    showToast(`Coupon valid on orders above ₹${coupon.minOrder}`, "warning");
    return;
  }

  AppState.activeCoupon = { ...coupon, code };
  if (input) input.value = code;
  renderCartDrawer();
  showToast(`Coupon "${code}" applied successfully!`, "success");
}

/* ==========================================================================
   CHECKOUT FLOW & CELEBRATION
   ========================================================================== */
function openCheckoutModal() {
  if (AppState.cart.length === 0) {
    showToast("Your cart is empty!", "warning");
    return;
  }

  // Close cart drawer if open
  const drawer = document.getElementById("cartDrawerOverlay");
  if (drawer) drawer.classList.remove("active");

  const modal = document.getElementById("checkoutModal");
  if (!modal) return;

  if (AppState.user) {
    if (AppState.user.name) checkoutFormData.name = AppState.user.name;
    if (AppState.user.email_phone) checkoutFormData.phone = AppState.user.email_phone;
  }

  renderCheckoutStep(1);
  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
}

let checkoutCurrentStep = 1;
const checkoutFormData = {
  name: "Raghav Sharma",
  phone: "9876543210",
  address: "Flat 402, Highline Greens, Tech Zone 4",
  city: "New Delhi",
  state: "Delhi",
  pincode: "110001",
  paymentMethod: "UPI"
};

function renderCheckoutStep(step) {
  checkoutCurrentStep = step;
  const container = document.getElementById("checkoutModalBody");
  const subtotal = AppState.cart.reduce((s, i) => s + (i.price * i.quantity), 0);
  const finalTotal = Math.max(0, subtotal - (AppState.activeCoupon ? 100 : 0));

  // Update step indicators
  for (let s = 1; s <= 3; s++) {
    const ind = document.getElementById(`checkoutStepInd-${s}`);
    if (ind) {
      ind.className = `step-indicator ${s === step ? "active" : (s < step ? "completed" : "")}`;
    }
  }

  if (step === 1) {
    // Delivery Address
    container.innerHTML = `
      <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 16px;">1. Enter Delivery Address</h3>
      <div class="form-grid">
        <div class="form-field-group">
          <label>Full Name *</label>
          <input type="text" id="chkName" value="${escapeHtml(checkoutFormData.name)}" placeholder="John Doe" />
        </div>
        <div class="form-field-group">
          <label>Mobile Number (for delivery SMS) *</label>
          <input type="tel" id="chkPhone" value="${escapeHtml(checkoutFormData.phone)}" placeholder="10-digit mobile number" />
        </div>
        <div class="form-field-group full-width">
          <label>Street Address / Flat / Building *</label>
          <input type="text" id="chkAddress" value="${escapeHtml(checkoutFormData.address)}" placeholder="House no., street name, landmark" />
        </div>
        <div class="form-field-group">
          <label>City *</label>
          <input type="text" id="chkCity" value="${escapeHtml(checkoutFormData.city)}" />
        </div>
        <div class="form-field-group">
          <label>Pincode *</label>
          <input type="text" id="chkPincode" value="${escapeHtml(checkoutFormData.pincode)}" maxlength="6" />
        </div>
      </div>
      <div style="margin-top: 24px; display: flex; justify-content: flex-end;">
        <button class="slide-cta-btn" onclick="saveAddressAndProceed()">Deliver to this Address →</button>
      </div>
    `;
  } else if (step === 2) {
    // Payment Method
    container.innerHTML = `
      <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 16px;">2. Select Payment Method</h3>
      <div class="payment-methods-list">
        <label class="payment-method-card ${checkoutFormData.paymentMethod === "UPI" ? "active" : ""}" onclick="selectPaymentMethod('UPI', this)">
          <input type="radio" name="payMethod" value="UPI" ${checkoutFormData.paymentMethod === "UPI" ? "checked" : ""} />
          <div>
            <div style="font-weight: 700; font-size: 14px;">⚡ UPI (Google Pay, PhonePe, Paytm, BHIM)</div>
            <div style="font-size: 12px; color: var(--text-muted);">Instant zero-fee payment with UPI QR or ID</div>
          </div>
        </label>

        <label class="payment-method-card ${checkoutFormData.paymentMethod === "Card" ? "active" : ""}" onclick="selectPaymentMethod('Card', this)">
          <input type="radio" name="payMethod" value="Card" ${checkoutFormData.paymentMethod === "Card" ? "checked" : ""} />
          <div>
            <div style="font-weight: 700; font-size: 14px;">💳 Credit / Debit Card</div>
            <div style="font-size: 12px; color: var(--text-muted);">Visa, MasterCard, RuPay, Amex</div>
          </div>
        </label>

        <label class="payment-method-card ${checkoutFormData.paymentMethod === "NetBanking" ? "active" : ""}" onclick="selectPaymentMethod('NetBanking', this)">
          <input type="radio" name="payMethod" value="NetBanking" ${checkoutFormData.paymentMethod === "NetBanking" ? "checked" : ""} />
          <div>
            <div style="font-weight: 700; font-size: 14px;">🏦 Net Banking</div>
            <div style="font-size: 12px; color: var(--text-muted);">All major Indian banks supported</div>
          </div>
        </label>

        <label class="payment-method-card ${checkoutFormData.paymentMethod === "COD" ? "active" : ""}" onclick="selectPaymentMethod('COD', this)">
          <input type="radio" name="payMethod" value="COD" ${checkoutFormData.paymentMethod === "COD" ? "checked" : ""} />
          <div>
            <div style="font-weight: 700; font-size: 14px;">💵 Cash on Delivery (COD)</div>
            <div style="font-size: 12px; color: var(--text-muted);">Pay by cash or QR code when item arrives</div>
          </div>
        </label>
      </div>

      <div style="margin-top: 24px; display: flex; justify-content: space-between;">
        <button style="padding: 10px 18px; border-radius: var(--radius-md); background: var(--bg-page); font-weight: 700;" onclick="renderCheckoutStep(1)">← Back to Address</button>
        <button class="slide-cta-btn" onclick="renderCheckoutStep(3)">Continue to Order Review →</button>
      </div>
    `;
  } else if (step === 3) {
    // Order Review & Confirmation
    container.innerHTML = `
      <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 16px;">3. Review Items and Delivery</h3>
      
      <div style="background: var(--bg-page); padding: 14px; border-radius: var(--radius-md); margin-bottom: 16px; font-size: 13px;">
        <div style="font-weight: 700; margin-bottom: 4px;">Delivering to:</div>
        <div>${escapeHtml(checkoutFormData.name)} | Ph: ${escapeHtml(checkoutFormData.phone)}</div>
        <div style="color: var(--text-muted);">${escapeHtml(checkoutFormData.address)}, ${escapeHtml(checkoutFormData.city)} - ${escapeHtml(checkoutFormData.pincode)}</div>
        <div style="margin-top: 6px; font-weight: 600; color: var(--flipkart-blue);">Payment: ${checkoutFormData.paymentMethod}</div>
      </div>

      <div style="max-height: 180px; overflow-y: auto; margin-bottom: 16px;">
        ${AppState.cart.map(item => `
          <div style="display: flex; gap: 12px; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
            <img src="${item.image}" alt="" style="width: 44px; height: 44px; object-fit: contain; background: #fff; border-radius: 4px;" />
            <div style="flex: 1; font-size: 12px;">
              <div style="font-weight: 600;">${escapeHtml(item.title)}</div>
              <div style="color: var(--text-muted);">Qty: ${item.quantity} × ₹${item.price.toLocaleString("en-IN")}</div>
            </div>
            <div style="font-weight: 700; font-size: 13px;">₹${(item.price * item.quantity).toLocaleString("en-IN")}</div>
          </div>
        `).join("")}
      </div>

      <div style="background: #ecfdf5; padding: 12px; border-radius: var(--radius-md); margin-bottom: 20px; font-size: 14px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; color: var(--rating-green);">
        <span>Total Payable:</span>
        <span style="font-size: 20px;">₹${Math.round(finalTotal).toLocaleString("en-IN")}</span>
      </div>

      <div style="display: flex; justify-content: space-between;">
        <button style="padding: 10px 18px; border-radius: var(--radius-md); background: var(--bg-page); font-weight: 700;" onclick="renderCheckoutStep(2)">← Back</button>
        <button class="slide-cta-btn" id="placeOrderFinalBtn" onclick="processPlaceOrder()" style="background-color: var(--accent-saffron); color: #ffffff;">
          ⚡ Place Order & Pay
        </button>
      </div>
    `;
  }
}

function saveAddressAndProceed() {
  const name = document.getElementById("chkName").value.trim();
  const phone = document.getElementById("chkPhone").value.trim();
  const address = document.getElementById("chkAddress").value.trim();
  const city = document.getElementById("chkCity").value.trim();
  const pincode = document.getElementById("chkPincode").value.trim();

  if (!name || !phone || !address || !pincode) {
    showToast("Please fill all required address fields", "warning");
    return;
  }

  checkoutFormData.name = name;
  checkoutFormData.phone = phone;
  checkoutFormData.address = address;
  checkoutFormData.city = city;
  checkoutFormData.pincode = pincode;
  AppState.deliveryPincode = pincode;
  AppState.deliveryCity = city;
  updateHeaderLocation();

  renderCheckoutStep(2);
}

function selectPaymentMethod(method, cardElem) {
  checkoutFormData.paymentMethod = method;
  document.querySelectorAll(".payment-method-card").forEach(c => c.classList.remove("active"));
  if (cardElem) cardElem.classList.add("active");
}

async function processPlaceOrder() {
  const btn = document.getElementById("placeOrderFinalBtn");
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span style="display: inline-block; animation: spin 1s infinite linear;">⏳</span> Processing Order...`;
  }

  const subtotal = AppState.cart.reduce((s, i) => s + (i.price * i.quantity), 0);
  const total = Math.max(0, subtotal - (AppState.activeCoupon ? 100 : 0));

  const customerName = AppState.user ? AppState.user.name : (checkoutFormData.name || "Customer");
  const customerPhone = AppState.user ? AppState.user.email_phone : (checkoutFormData.phone || "9876543210");

  const orderPayload = {
    ...checkoutFormData,
    name: customerName,
    phone: customerPhone,
    customer_name: customerName,
    customer_phone: customerPhone,
    items: [...AppState.cart],
    subtotal: subtotal,
    discount: AppState.activeCoupon ? 100 : 0,
    delivery_fee: 0,
    coupon_applied: AppState.activeCoupon ? AppState.activeCoupon.code : "",
    total: total
  };

  let placedOrderInfo = null;

  try {
    const res = await fetch("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(orderPayload)
    });
    if (res.ok) {
      const data = await res.json();
      placedOrderInfo = data.order;
    }
  } catch (err) {
    console.log("Offline mode, generating client order id");
  }

  // Client fallback order generation
  if (!placedOrderInfo) {
    placedOrderInfo = {
      order_id: `SX-${Math.floor(100000 + Math.random() * 900000)}-${Math.floor(10 + Math.random() * 90)}`,
      created_at: new Date().toLocaleString(),
      status: "Order Confirmed",
      expected_delivery: "Within 2 Days",
      total: total
    };
  }

  // Save to AppState orders
  AppState.orders.unshift({
    ...placedOrderInfo,
    items: [...AppState.cart],
    delivery_address: `${checkoutFormData.address}, ${checkoutFormData.city}`
  });
  saveOrdersState();

  // Clear cart
  AppState.cart = [];
  AppState.activeCoupon = null;
  saveCartState();
  AppState.products.forEach(p => updateProductCardAction(p.id));

  // Render Celebration / Success Screen
  renderOrderSuccess(placedOrderInfo);
  fireConfettiAnimation();
}

function renderOrderSuccess(orderInfo) {
  const container = document.getElementById("checkoutModalBody");
  container.innerHTML = `
    <div class="order-success-container">
      <div class="success-checkmark-circle">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
      </div>
      <h2 style="font-size: 24px; font-weight: 800;">Order Placed Successfully!</h2>
      <p style="color: var(--text-muted); font-size: 14px;">Thank you for shopping on ShopX. A confirmation SMS & email have been sent.</p>
      
      <div class="order-id-badge">Order ID: ${orderInfo.order_id}</div>

      <div style="background: var(--bg-page); padding: 16px 24px; border-radius: var(--radius-md); max-width: 400px; width: 100%; text-align: left; font-size: 13px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="color: var(--text-muted);">Estimated Delivery:</span>
          <b>${orderInfo.expected_delivery || "Tomorrow"}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="color: var(--text-muted);">Amount Paid:</span>
          <b>₹${Math.round(orderInfo.total).toLocaleString("en-IN")}</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <span style="color: var(--text-muted);">Status:</span>
          <span style="color: var(--rating-green); font-weight: 700;">● Confirmed</span>
        </div>
      </div>

      <div style="display: flex; gap: 12px; margin-top: 12px;">
        <button class="slide-cta-btn" onclick="openOrderTrackingModal('${orderInfo.order_id}')" style="background-color: var(--flipkart-blue); color: #fff;">
          📍 Track Order
        </button>
        <button style="padding: 12px 20px; border-radius: var(--radius-md); background: var(--bg-page); font-weight: 700;" onclick="closeCheckoutModal()">
          Continue Shopping
        </button>
      </div>
    </div>
  `;
}

// Confetti Cannon Animation Effect
function fireConfettiAnimation() {
  const canvas = document.getElementById("confettiCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  canvas.style.display = "block";

  const pieces = [];
  const colors = ["#2874f0", "#ff9900", "#fb641b", "#ffe500", "#388e3c", "#ec4899", "#8b5cf6"];

  for (let i = 0; i < 150; i++) {
    pieces.push({
      x: canvas.width / 2,
      y: canvas.height / 2,
      vx: (Math.random() - 0.5) * 20,
      vy: (Math.random() - 0.7) * 20,
      size: Math.random() * 8 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      rotationSpeed: (Math.random() - 0.5) * 10,
      gravity: 0.35,
      alpha: 1
    });
  }

  let frames = 0;
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let alive = false;

    pieces.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += p.gravity;
      p.rotation += p.rotationSpeed;
      if (frames > 40) p.alpha -= 0.015;

      if (p.alpha > 0) {
        alive = true;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();
      }
    });

    frames++;
    if (alive && frames < 140) {
      requestAnimationFrame(animate);
    } else {
      canvas.style.display = "none";
    }
  }

  animate();
}

/* ==========================================================================
   ORDERS & LIVE TRACKING MODAL
   ========================================================================== */
function openOrdersModal() {
  const modal = document.getElementById("ordersModal");
  const listContainer = document.getElementById("ordersListContainer");
  if (!modal || !listContainer) return;

  if (AppState.orders.length === 0) {
    listContainer.innerHTML = `
      <div style="text-align: center; padding: 40px 20px;">
        <div style="font-size: 40px; margin-bottom: 12px;">📦</div>
        <h4 style="font-weight: 700; margin-bottom: 6px;">No orders placed yet</h4>
        <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 16px;">Once you place orders on ShopX, they will show up here.</p>
        <button class="slide-cta-btn" onclick="closeOrdersModal()">Browse Products</button>
      </div>
    `;
  } else {
    listContainer.innerHTML = AppState.orders.map(order => `
      <div style="border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px; margin-bottom: 14px; background: var(--bg-surface);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px; margin-bottom: 10px;">
          <div>
            <div style="font-weight: 800; font-size: 14px;">Order ID: ${order.order_id}</div>
            <div style="font-size: 11px; color: var(--text-muted);">${order.created_at}</div>
          </div>
          <button class="pincode-check-btn" onclick="openOrderTrackingModal('${order.order_id}')" style="font-size: 12px; padding: 6px 14px;">
            Track Package
          </button>
        </div>
        <div style="font-size: 13px; margin-bottom: 8px;">
          <b>Total:</b> ₹${Math.round(order.total).toLocaleString("en-IN")} | <b>Status:</b> <span style="color: var(--rating-green);">${order.status}</span>
        </div>
        <div style="font-size: 12px; color: var(--text-muted);">
          <b>Items:</b> ${(order.items || []).map(i => `${i.title.slice(0, 30)} (x${i.quantity})`).join(", ")}
        </div>
      </div>
    `).join("");
  }

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeOrdersModal() {
  const modal = document.getElementById("ordersModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
}

function openOrderTrackingModal(orderId) {
  closeOrdersModal();
  closeCheckoutModal();

  const modal = document.getElementById("trackingModal");
  const content = document.getElementById("trackingModalContent");
  if (!modal || !content) return;

  const order = AppState.orders.find(o => o.order_id === orderId) || {
    order_id: orderId,
    created_at: "Today, 11:30 AM",
    expected_delivery: "Tomorrow, 11:00 AM",
    total: 12999
  };

  content.innerHTML = `
    <div style="padding: 24px;">
      <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 4px;">Tracking: ${order.order_id}</h3>
      <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 16px;">Expected delivery: <b>${order.expected_delivery || "Tomorrow by 11:00 AM"}</b></p>
      
      <div class="tracking-timeline-list">
        <div class="tracking-step-item completed">
          <div class="tracking-step-bullet"></div>
          <div class="tracking-step-title">Order Placed & Confirmed</div>
          <div class="tracking-step-time">${order.created_at}</div>
          <div class="tracking-step-desc">Payment confirmed. Seller has received and acknowledged your order.</div>
        </div>

        <div class="tracking-step-item completed">
          <div class="tracking-step-bullet"></div>
          <div class="tracking-step-title">Packed at ShopX Mega Warehouse</div>
          <div class="tracking-step-time">Fulfillment Center 7, Gurugram</div>
          <div class="tracking-step-desc">Items safely packaged with tamper-proof security seal.</div>
        </div>

        <div class="tracking-step-item in_progress">
          <div class="tracking-step-bullet"></div>
          <div class="tracking-step-title">In Transit (ShopX Express Air)</div>
          <div class="tracking-step-time">On route to Hub - New Delhi 110001</div>
          <div class="tracking-step-desc">Shipment has left the national sorting facility.</div>
        </div>

        <div class="tracking-step-item">
          <div class="tracking-step-bullet"></div>
          <div class="tracking-step-title">Out for Delivery</div>
          <div class="tracking-step-time">Pending arrival at local hub</div>
          <div class="tracking-step-desc">Our delivery partner will call before arriving at your door.</div>
        </div>

        <div class="tracking-step-item">
          <div class="tracking-step-bullet"></div>
          <div class="tracking-step-title">Delivered</div>
          <div class="tracking-step-time">${order.expected_delivery || "Tomorrow"}</div>
          <div class="tracking-step-desc">Package handed to customer.</div>
        </div>
      </div>
    </div>
  `;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeTrackingModal() {
  const modal = document.getElementById("trackingModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
}

/* ==========================================================================
   WISHLIST DRAWER
   ========================================================================== */
function toggleWishlist(productId, event) {
  if (event) event.stopPropagation();
  const product = AppState.products.find(p => p.id === productId);
  if (!product) return;

  const existsIdx = AppState.wishlist.findIndex(w => w.id === productId);
  if (existsIdx !== -1) {
    AppState.wishlist.splice(existsIdx, 1);
    showToast("Removed from Wishlist", "info");
  } else {
    AppState.wishlist.push(product);
    showToast("Added to Wishlist ❤️", "success");
  }

  saveWishlistState();
  renderProductsGrid();
}

function openWishlistModal() {
  const modal = document.getElementById("wishlistModal");
  const listContainer = document.getElementById("wishlistItemsList");
  if (!modal || !listContainer) return;

  if (AppState.wishlist.length === 0) {
    listContainer.innerHTML = `
      <div style="text-align: center; padding: 40px 20px;">
        <div style="font-size: 40px; margin-bottom: 12px;">❤️</div>
        <h4 style="font-weight: 700; margin-bottom: 6px;">Your Wishlist is empty</h4>
        <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 16px;">Save your favorite deals and discover them here anytime.</p>
        <button class="slide-cta-btn" onclick="closeWishlistModal()">Explore Products</button>
      </div>
    `;
  } else {
    listContainer.innerHTML = AppState.wishlist.map(item => `
      <div style="display: flex; gap: 14px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--border-subtle);">
        <img src="${item.image}" alt="${escapeHtml(item.title)}" style="width: 60px; height: 60px; object-fit: contain; background: #f9fafb; border-radius: 4px;" />
        <div style="flex: 1;">
          <div style="font-weight: 600; font-size: 13px;">${escapeHtml(item.title)}</div>
          <div style="font-weight: 800; font-size: 15px; margin-top: 4px;">₹${item.price.toLocaleString("en-IN")}</div>
        </div>
        <button class="add-to-cart-btn" style="width: auto; padding: 8px 14px; font-size: 12px;" onclick="addToCart(${item.id}); toggleWishlist(${item.id});">
          Move to Cart
        </button>
        <button onclick="toggleWishlist(${item.id})" style="color: var(--discount-red); font-size: 18px; padding: 4px;">×</button>
      </div>
    `).join("");
  }

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeWishlistModal() {
  const modal = document.getElementById("wishlistModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
}

/* ==========================================================================
   DELIVERY LOCATION MODAL
   ========================================================================== */
function openLocationModal() {
  const modal = document.getElementById("locationModal");
  if (modal) {
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }
}

function closeLocationModal() {
  const modal = document.getElementById("locationModal");
  if (modal) {
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }
}

function saveDeliveryLocation() {
  const pinInput = document.getElementById("headerPincodeInput");
  const cityInput = document.getElementById("headerCityInput");
  const pin = pinInput ? pinInput.value.trim() : "";
  const city = cityInput ? cityInput.value.trim() : "";

  if (/^\d{6}$/.test(pin)) {
    AppState.deliveryPincode = pin;
    AppState.deliveryCity = city || "New Delhi";
    localStorage.setItem("shopx_pincode", pin);
    localStorage.setItem("shopx_city", AppState.deliveryCity);
    updateHeaderLocation();
    closeLocationModal();
    showToast(`Delivery location set to ${AppState.deliveryCity} (${pin})`, "success");
  } else {
    showToast("Please enter a valid 6-digit postal code", "warning");
  }
}

function updateHeaderLocation() {
  const locElem = document.getElementById("headerDeliveryLocation");
  if (locElem) {
    locElem.textContent = `${AppState.deliveryCity} ${AppState.deliveryPincode}`;
  }
}

/* ==========================================================================
   SEARCH AUTOCOMPLETE & FORM HANDLING
   ========================================================================== */
function initEventListeners() {
  const searchInput = document.getElementById("searchInputField");
  const clearBtn = document.getElementById("clearSearchBtn");
  const dropdown = document.getElementById("searchAutocompleteDropdown");
  const searchForm = document.getElementById("searchForm");
  const catSelect = document.getElementById("searchCategorySelect");

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const val = e.target.value;
      if (clearBtn) clearBtn.style.display = val ? "block" : "none";
      handleAutocompleteSearch(val);
    });

    searchInput.addEventListener("focus", (e) => {
      if (e.target.value.trim().length > 0) {
        handleAutocompleteSearch(e.target.value);
      }
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".search-bar-wrapper")) {
        if (dropdown) dropdown.classList.remove("active");
      }
    });
  }

  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      executeSearch();
    });
  }

  if (catSelect) {
    catSelect.addEventListener("change", (e) => {
      selectCategory(e.target.value);
    });
  }
}

function handleAutocompleteSearch(query) {
  const dropdown = document.getElementById("searchAutocompleteDropdown");
  if (!dropdown) return;
  const q = query.trim().toLowerCase();

  if (q.length < 1) {
    dropdown.classList.remove("active");
    return;
  }

  const matches = AppState.products.filter(p => {
    return p.title.toLowerCase().includes(q) ||
           p.brand.toLowerCase().includes(q) ||
           p.category.toLowerCase().includes(q);
  }).slice(0, 6);

  if (matches.length === 0) {
    dropdown.innerHTML = `
      <div style="padding: 12px 16px; font-size: 13px; color: var(--text-muted);">
        No immediate results for "<b>${escapeHtml(query)}</b>". Press enter to search catalog.
      </div>
    `;
    dropdown.classList.add("active");
    return;
  }

  dropdown.innerHTML = matches.map(p => `
    <div class="autocomplete-item" onclick="onAutocompleteSelect(${p.id})">
      <img src="${p.image}" alt="" class="autocomplete-thumb" />
      <div class="autocomplete-text">
        <div class="autocomplete-title">${highlightMatch(p.title, q)}</div>
        <div class="autocomplete-meta">${escapeHtml(p.brand)} in ${escapeHtml(p.category)}</div>
      </div>
      <div class="autocomplete-price">₹${p.price.toLocaleString("en-IN")}</div>
    </div>
  `).join("");

  dropdown.classList.add("active");
}

function highlightMatch(text, query) {
  const index = text.toLowerCase().indexOf(query.toLowerCase());
  if (index === -1) return escapeHtml(text);
  const before = text.substring(0, index);
  const match = text.substring(index, index + query.length);
  const after = text.substring(index + query.length);
  return `${escapeHtml(before)}<b style="color: var(--flipkart-blue);">${escapeHtml(match)}</b>${escapeHtml(after)}`;
}

function onAutocompleteSelect(productId) {
  const dropdown = document.getElementById("searchAutocompleteDropdown");
  if (dropdown) dropdown.classList.remove("active");
  openProductQuickView(productId);
}

function executeSearch() {
  const input = document.getElementById("searchInputField");
  const dropdown = document.getElementById("searchAutocompleteDropdown");
  if (dropdown) dropdown.classList.remove("active");

  AppState.filters.searchQuery = input ? input.value.trim() : "";
  applyFiltersAndSort();

  const anchor = document.getElementById("productsCatalogAnchor");
  if (anchor) anchor.scrollIntoView({ behavior: "smooth" });
}

function onSearchClear() {
  const input = document.getElementById("searchInputField");
  const clearBtn = document.getElementById("clearSearchBtn");
  const dropdown = document.getElementById("searchAutocompleteDropdown");

  if (input) input.value = "";
  if (clearBtn) clearBtn.style.display = "none";
  if (dropdown) dropdown.classList.remove("active");

  AppState.filters.searchQuery = "";
  applyFiltersAndSort();
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ==========================================================================
   TOAST NOTIFICATION UTILITY
   ========================================================================== */
function showToast(message, type = "info") {
  let container = document.getElementById("toastContainer");
  if (!container) {
    container = document.createElement("div");
    container.id = "toastContainer";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const icons = {
    success: "✓",
    info: "ℹ",
    warning: "⚠️"
  };

  const toast = document.createElement("div");
  toast.className = `toast-msg ${type}`;
  toast.innerHTML = `<span>${icons[type] || "ℹ"}</span> <span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 4000);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}


/* ==========================================================================
   SMART RECOMMENDATION ENGINE
   ========================================================================== */
function getSmartRecommendations(limit = 8) {
  if (!AppState.products || AppState.products.length === 0) return [];
  
  // Gather categories currently in cart
  const cartCategories = new Set(AppState.cart.map(c => {
    const full = AppState.products.find(p => p.id === c.id);
    return full ? full.category : null;
  }).filter(Boolean));

  const cartProductIds = new Set(AppState.cart.map(c => c.id));

  // Score products based on rating, discount, bestseller, and cart synergy
  const scored = AppState.products.map(p => {
    let score = (p.rating || 4) * 10 + (p.discount || 0);
    if (p.is_bestseller) score += 25;
    if (p.is_deal) score += 20;
    if (cartCategories.has(p.category)) score += 35;
    if (cartProductIds.has(p.id)) score -= 100;
    return { product: p, score };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, limit).map(s => s.product);
}

function renderRecommendations() {
  const container = document.getElementById("recommendationsScrollContainer");
  if (!container) return;

  const recs = getSmartRecommendations(10);
  if (recs.length === 0) {
    container.innerHTML = `<p style="padding: 20px; color: var(--text-muted);">Explore products to see personalized recommendations!</p>`;
    return;
  }

  container.innerHTML = recs.map(p => `
    <div class="rec-card">
      <img src="${p.image}" alt="${escapeHtml(p.title)}" class="rec-card-image" onclick="openQuickViewModal(${p.id})" loading="lazy" />
      <div class="rec-card-category">${escapeHtml(p.category)}</div>
      <div class="rec-card-title" onclick="openQuickViewModal(${p.id})" title="${escapeHtml(p.title)}">
        ${escapeHtml(p.title)}
      </div>
      <div class="rec-card-price-row">
        <span class="rec-card-price">₹${p.price.toLocaleString("en-IN")}</span>
        ${p.original_price > p.price ? `<span class="rec-card-original">₹${p.original_price.toLocaleString("en-IN")}</span>` : ''}
        ${p.discount > 0 ? `<span class="rec-card-discount">${p.discount}% off</span>` : ''}
      </div>
      <button class="rec-add-btn" onclick="addToCart(${p.id})">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
        Add to Cart
      </button>
    </div>
  `).join("");
}

function scrollRecommendations(direction) {
  const container = document.getElementById("recommendationsScrollContainer");
  if (container) {
    const scrollAmount = 350 * direction;
    container.scrollBy({ left: scrollAmount, behavior: "smooth" });
  }
}

/* ==========================================================================
   SHOPBOT AI SHOPPING ASSISTANT & CHATBOT
   ========================================================================== */
let shopbotInitialized = false;

function initShopbot() {
  if (shopbotInitialized) return;
  shopbotInitialized = true;

  const msgContainer = document.getElementById("shopbotMessagesContainer");
  if (!msgContainer) return;

  // Add initial friendly greeting
  const greeting = `
    Hi there! 👋 I'm <b>ShopBot</b>, your personal ShopX AI Shopping Assistant.<br/><br/>
    I can help you:
    <ul style="margin: 6px 0 0 16px; padding: 0;">
      <li>🔍 Find products within your budget</li>
      <li>🔥 Discover today's top deals</li>
      <li>📦 Track active orders</li>
      <li>🎟️ Apply promo coupon codes</li>
    </ul>
    <br/>What are you looking for today?
  `;
  appendShopbotMessage(greeting, "bot");
}

function toggleShopbot() {
  const win = document.getElementById("shopbotWindow");
  if (!win) return;
  const isActive = win.classList.contains("active");
  if (isActive) {
    win.classList.remove("active");
  } else {
    win.classList.add("active");
    if (!shopbotInitialized) initShopbot();
    setTimeout(() => {
      const input = document.getElementById("shopbotInput");
      if (input) input.focus();
    }, 150);
  }
}

function appendShopbotMessage(htmlContent, sender = "bot") {
  const container = document.getElementById("shopbotMessagesContainer");
  if (!container) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerHTML = htmlContent;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function handleShopbotChip(chipText) {
  const input = document.getElementById("shopbotInput");
  if (input) {
    input.value = chipText;
    processShopbotQuery(chipText);
    input.value = "";
  }
}

function handleShopbotSubmit(event) {
  if (event) event.preventDefault();
  const input = document.getElementById("shopbotInput");
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;

  processShopbotQuery(text);
  input.value = "";
}

function clearShopbotChat() {
  const container = document.getElementById("shopbotMessagesContainer");
  if (container) container.innerHTML = "";
  shopbotInitialized = false;
  initShopbot();
}

function processShopbotQuery(userText) {
  appendShopbotMessage(escapeHtml(userText), "user");

  // Show typing indicator
  const typingId = "shopbotTypingIndicator";
  appendShopbotMessage(`<span id="${typingId}" style="color: var(--text-muted); font-style: italic;">ShopBot is thinking...</span>`, "bot");

  setTimeout(() => {
    const typingElem = document.getElementById(typingId);
    if (typingElem && typingElem.closest(".chat-bubble")) {
      typingElem.closest(".chat-bubble").remove();
    }

    const responseHtml = generateShopbotResponse(userText);
    appendShopbotMessage(responseHtml, "bot");
  }, 400);
}

function generateShopbotResponse(query) {
  const q = query.toLowerCase();

  // 1. Coupon queries
  if (q.includes("coupon") || q.includes("promo") || q.includes("discount code") || q.includes("offer")) {
    return `
      Here are the active promo coupons you can apply at checkout:<br/><br/>
      🎟️ <b>SHOPX100</b> — Flat ₹100 OFF on orders above ₹500<br/>
      🎟️ <b>FESTIVE20</b> — 20% OFF (up to ₹1,000) on orders above ₹1,500<br/>
      🎟️ <b>WELCOME50</b> — Flat ₹50 OFF on your first purchase<br/>
      🎟️ <b>PRIMEPLUS</b> — 10% OFF for ShopX Plus members<br/><br/>
      <i>Just enter the code in your cart drawer to save instantly!</i>
    `;
  }

  // 2. Order Tracking
  if (q.includes("track") || q.includes("order") || q.includes("delivery") || q.includes("shipping")) {
    if (AppState.orders && AppState.orders.length > 0) {
      const latest = AppState.orders[0];
      return `
        📦 Found your latest order: <b>${latest.order_id}</b><br/>
        Status: <b style="color: #16a34a;">${latest.status || "Order Confirmed"}</b><br/>
        Expected Delivery: <b>${latest.expected_delivery || "Tomorrow by 11:00 AM"}</b><br/>
        Total Amount: <b>₹${(latest.total || 0).toLocaleString("en-IN")}</b><br/><br/>
        <button class="chat-add-btn" onclick="openOrderTrackingModal('${latest.order_id}')" style="width: 100%;">
          📍 View Full Live Tracking Timeline
        </button>
      `;
    } else {
      return `
        📦 You don't have any placed orders yet.<br/>
        Once you place an order, you can track it live right here or via the <b>Track Orders</b> menu in the top bar!
      `;
    }
  }

  // 3. Return / Refund Policy
  if (q.includes("return") || q.includes("refund") || q.includes("exchange") || q.includes("replacement")) {
    return `
      🛡️ <b>ShopX 7-Day Hassle-Free Returns:</b><br/>
      All electronics, smartphones, and fashion items come with a 7-day doorstep replacement or full refund policy.<br/><br/>
      Simply keep the original box and invoice ready.
    `;
  }

  // 4. Greetings
  if (q === "hi" || q === "hello" || q === "hey" || q.includes("how are you")) {
    return `
      Hello! 😊 How can I help you find what you need today? You can ask me for phones under a budget, best laptops, wireless headphones, or trending sneakers!
    `;
  }

  // 5. Budget / Price queries
  let maxBudget = null;
  const budgetMatch = q.match(/(?:under|below|less than|within|upto|budget)\s*(?:₹|rs\.?|inr)?\s*(\d+)(?:\s*(?:k|thousand|lakh|lac))?/i);
  if (budgetMatch) {
    let num = parseInt(budgetMatch[1], 10);
    const unit = (budgetMatch[0] || "").toLowerCase();
    if (unit.includes("k") || unit.includes("thousand")) num *= 1000;
    else if (unit.includes("lakh") || unit.includes("lac")) num *= 100000;
    else if (num < 1000) num *= 1000;
    maxBudget = num;
  }

  // 6. Product Searches & Recommendations
  let matched = AppState.products.filter(p => {
    const text = `${p.title} ${p.brand} ${p.category} ${(p.tags || []).join(" ")}`.toLowerCase();
    
    // Check budget condition
    if (maxBudget && p.price > maxBudget) return false;

    // Check keyword matching
    if (q.includes("phone") || q.includes("mobile")) return p.category === "Mobiles & Tablets";
    if (q.includes("laptop") || q.includes("macbook") || q.includes("pc") || q.includes("computer")) return p.category === "Laptops & Computers";
    if (q.includes("earbuds") || q.includes("headphone") || q.includes("audio") || q.includes("speaker") || q.includes("anc") || q.includes("noise cancell")) return p.category === "Audio & Headphones";
    if (q.includes("watch") || q.includes("smartwatch") || q.includes("fitness")) return p.category === "Smart Watches & Wearables";
    if (q.includes("shoe") || q.includes("sneaker") || q.includes("jordan") || q.includes("running")) return p.category === "Footwear & Sneakers";
    if (q.includes("camera") || q.includes("photo") || q.includes("vlog")) return p.category === "Cameras & Photography";
    if (q.includes("home") || q.includes("kitchen") || q.includes("vacuum") || q.includes("airfryer")) return p.category === "Home & Kitchen";
    if (q.includes("deal") || q.includes("best deal") || q.includes("offer")) return p.is_deal;
    if (q.includes("bestseller") || q.includes("popular") || q.includes("top")) return p.is_bestseller;

    // Direct brand matching
    if (p.brand && q.includes(p.brand.toLowerCase())) return true;

    // Word intersection
    const words = q.split(/\s+/).filter(w => w.length > 2);
    return words.some(w => text.includes(w));
  });

  if (matched.length === 0) {
    matched = AppState.products.filter(p => p.is_deal || p.is_bestseller).slice(0, 3);
    return `
      I couldn't find an exact match for <i>"${escapeHtml(query)}"</i>, but here are our highest-rated recommendations right now:<br/>
      ${renderChatProductCards(matched)}
    `;
  }

  matched.sort((a, b) => b.rating - a.rating);
  const topResults = matched.slice(0, 3);

  const budgetText = maxBudget ? ` under ₹${maxBudget.toLocaleString("en-IN")}` : "";
  return `
    ✨ Found <b>${matched.length}</b> great options${budgetText}! Here are the top picks for you:
    ${renderChatProductCards(topResults)}
  `;
}

function renderChatProductCards(products) {
  return products.map(p => `
    <div class="chat-product-card">
      <img src="${p.image}" alt="${escapeHtml(p.title)}" class="chat-product-img" onclick="openQuickViewModal(${p.id})" />
      <div class="chat-product-info">
        <div class="chat-product-title" onclick="openQuickViewModal(${p.id})" title="${escapeHtml(p.title)}">${escapeHtml(p.title)}</div>
        <div class="chat-product-price">
          ₹${p.price.toLocaleString("en-IN")}
          ${p.discount > 0 ? `<span style="color: #16a34a; font-size: 11px; font-weight: 700; margin-left: 4px;">(${p.discount}% OFF)</span>` : ''}
        </div>
        <div style="font-size: 10px; color: var(--text-muted);">⭐ ${p.rating} (${p.reviews_count || 500}+ reviews)</div>
      </div>
      <div class="chat-product-actions">
        <button class="chat-add-btn" onclick="addToCart(${p.id})">+ Cart</button>
        <button class="chat-view-btn" onclick="openQuickViewModal(${p.id})">Details</button>
      </div>
    </div>
  `).join("");
}
