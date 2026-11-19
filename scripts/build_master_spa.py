import json, re

# Let's write the complete, clean master index.html
spa_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Stella — Pure Botanical Actives & Everyday Radiance</title>
  <meta name="description" content="Nourishing your skin, naturally. Clinical botanical formulations for everyday luminosity.">

  <!-- Google Fonts: Editorial Serif & Clean Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/styles-CxV8MDxeo7vlVqHCYIDCSdWR9G3dcl.css">
</head>
<body>

  <!-- Minimalist Announcement -->
  <div class="announcement-bar">
    Complimentary Pan-India delivery on orders above ₹499 &bull; Use code <strong>STELLA20</strong> for 20% off &bull; Available on <a href="https://www.flipkart.com" target="_blank" rel="noopener">Flipkart</a>
  </div>

  <!-- Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="brand-logo" aria-label="The Stella Home" onclick="spaNavigate(event, 'index.html')">
        <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/logo-STLKJDy87Vj6JxovRFEcieIRtrO5YT.svg" alt="The Stella">
      </a>

      <nav class="nav-links">
        <a href="index.html" class="nav-link" id="nav-home" onclick="spaNavigate(event, 'index.html')">Home</a>
        <a href="shop.html" class="nav-link" id="nav-shop" onclick="spaNavigate(event, 'shop.html')">Collection</a>
        <a href="shop.html?category=face" class="nav-link" id="nav-face" onclick="spaNavigate(event, 'shop.html?category=face')">Face</a>
        <a href="haircare.html" class="nav-link" id="nav-hair" onclick="spaNavigate(event, 'haircare.html')">Haircare</a>
        <a href="shop.html?category=body" class="nav-link" id="nav-body" onclick="spaNavigate(event, 'shop.html?category=body')">Body</a>
        <a href="about.html" class="nav-link" id="nav-about" onclick="spaNavigate(event, 'about.html')">About</a>
        <a href="routine-finder.html" class="nav-link" id="nav-quiz" onclick="spaNavigate(event, 'routine-finder.html')">Routine Quiz</a>
        <a href="https://www.flipkart.com" target="_blank" rel="noopener" class="nav-link">Flipkart</a>
      </nav>

      <div class="header-actions">
        <!-- Auth Status -->
        <span class="header-auth-status" style="font-size: 0.82rem;">
          <a href="account.html" id="headerAuthLink" onclick="spaNavigate(event, 'account.html')">Account</a>
        </span>

        <!-- Bag Trigger -->
        <a href="checkout.html" class="btn-icon" aria-label="Shopping Bag" onclick="spaNavigate(event, 'checkout.html')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
          </svg>
          <span class="badge-dot bag-count-badge">0</span>
        </a>

        <a href="shop.html" class="btn-minimal btn-minimal-primary" onclick="spaNavigate(event, 'shop.html')">
          Shop Now
        </a>
      </div>
    </div>
  </header>

  <!-- DYNAMIC VIEW CONTAINER -->
  <main id="appView">
    <!-- Populated by client-side router -->
  </main>

  <!-- Minimalist Site Footer -->
  <footer class="site-footer" id="siteFooter">
    <div class="container">
      <div class="footer-main-grid">
        <div>
          <a href="index.html" class="brand-logo" style="margin-bottom: 16px;" onclick="spaNavigate(event, 'index.html')">
            <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/logo-STLKJDy87Vj6JxovRFEcieIRtrO5YT.svg" alt="The Stella">
          </a>
          <p style="font-size: 0.88rem; color: var(--color-text-secondary); max-width: 320px; line-height: 1.6;">
            Nourishing your skin, naturally. Clinical botanical formulations crafted for everyday radiance.
          </p>
        </div>

        <div>
          <h4 class="footer-col-title">Navigation</h4>
          <ul class="footer-list">
            <li><a href="shop.html" onclick="spaNavigate(event, 'shop.html')">All Products</a></li>
            <li><a href="haircare.html" onclick="spaNavigate(event, 'haircare.html')">Curd Haircare</a></li>
            <li><a href="about.html" onclick="spaNavigate(event, 'about.html')">About The Stella</a></li>
            <li><a href="routine-finder.html" onclick="spaNavigate(event, 'routine-finder.html')">Routine Diagnostic</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-col-title">Portals</h4>
          <ul class="footer-list">
            <li><a href="account.html" onclick="spaNavigate(event, 'account.html')">Customer Sign In / Sign Up</a></li>
            <li><a href="admin.html" onclick="spaNavigate(event, 'admin.html')">Admin Management Portal</a></li>
            <li><a href="contact.html" onclick="spaNavigate(event, 'contact.html')">Track Order & Contact</a></li>
            <li><a href="https://www.flipkart.com" target="_blank" rel="noopener">Flipkart Storefront</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-col-title">Assistance</h4>
          <p style="font-size: 0.85rem; color: var(--color-text-secondary); line-height: 1.6;">
            Direct inquiries: <a href="mailto:care@thestella.in" style="text-decoration: underline;">care@thestella.in</a>
          </p>
          <div style="margin-top: 16px;">
            <a href="admin.html" class="btn-minimal btn-minimal-outline" style="font-size: 0.72rem; padding: 6px 12px;" onclick="spaNavigate(event, 'admin.html')">Admin Access</a>
          </div>
        </div>
      </div>

      <div class="footer-legal-bar">
        <div>&copy; 2026 The Stella. All rights reserved.</div>
        <div>Crafted with clinical intention. Made in India.</div>
      </div>
    </div>
  </footer>

  <script src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/store-JxI4Ec1i1id9zUAXUBa2JwdJdjoWXP.js"></script>

  <!-- COMPLETE CLIENT-SIDE SPA ROUTER & VIEW RENDERING ENGINE -->
  <script>
    // Navigation handler
    function spaNavigate(e, url) {
      if (e) e.preventDefault();
      window.history.pushState({}, '', url);
      renderCurrentRoute();
      window.scrollTo(0, 0);
    }

    window.addEventListener('popstate', () => {
      renderCurrentRoute();
    });

    // Detect route
    function getCurrentRoute() {
      const path = window.location.pathname.toLowerCase();
      const params = new URLSearchParams(window.location.search);

      if (path.includes('shop')) return 'shop';
      if (path.includes('product')) return 'product';
      if (path.includes('haircare')) return 'haircare';
      if (path.includes('about')) return 'about';
      if (path.includes('routine-finder')) return 'routine-finder';
      if (path.includes('checkout')) return 'checkout';
      if (path.includes('account')) return 'account';
      if (path.includes('admin')) return 'admin';
      if (path.includes('contact')) return 'contact';
      return 'home';
    }

    function updateActiveNav(route) {
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      if (route === 'home') document.getElementById('nav-home')?.classList.add('active');
      else if (route === 'shop') document.getElementById('nav-shop')?.classList.add('active');
      else if (route === 'haircare') document.getElementById('nav-hair')?.classList.add('active');
      else if (route === 'about') document.getElementById('nav-about')?.classList.add('active');
      else if (route === 'routine-finder') document.getElementById('nav-quiz')?.classList.add('active');
    }

    // Router dispatcher
    function renderCurrentRoute() {
      const route = getCurrentRoute();
      updateActiveNav(route);
      updateHeaderBagBadge();
      updateHeaderAuthUI();

      const container = document.getElementById('appView');
      const footer = document.getElementById('siteFooter');

      // Adjust footer visibility
      if (route === 'admin') {
        if (footer) footer.style.display = 'none';
      } else {
        if (footer) footer.style.display = 'block';
      }

      if (route === 'home') renderHomeView(container);
      else if (route === 'shop') renderShopView(container);
      else if (route === 'product') renderProductView(container);
      else if (route === 'haircare') renderHaircareView(container);
      else if (route === 'about') renderAboutView(container);
      else if (route === 'routine-finder') renderRoutineFinderView(container);
      else if (route === 'checkout') renderCheckoutView(container);
      else if (route === 'account') renderAccountView(container);
      else if (route === 'admin') renderAdminView(container);
      else if (route === 'contact') renderContactView(container);
    }

    // ==========================================
    // 1. HOME VIEW
    // ==========================================
    function renderHomeView(el) {
      document.title = "The Stella — Pure Botanical Actives & Everyday Radiance";
      el.innerHTML = `
        <section class="hero-section" id="hero">
          <div class="container">
            <div class="hero-frame">
              <div class="hero-bg-layer">
                <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/hero-model-editorial-WmidrvHbDWTdPf5xUw6AcOdMv7RuOc.jpg" alt="Editorial Skincare Portrait">
              </div>
              <div class="hero-overlay-tint"></div>

              <div class="hero-left-content">
                <span class="text-eyebrow">The Stella Edition</span>
                <h1 class="hero-title">Flourish in <br>Daily Power</h1>
                <p class="hero-desc">
                  Give life to your inner world and flourish in your uniqueness. Clean dermatological formulas for everyday skin radiance.
                </p>

                <div class="hero-floating-deck">
                  <div class="floating-product-card">
                    <a href="product.html?id=stella-dual-phase" class="floating-card-image" onclick="spaNavigate(event, 'product.html?id=stella-dual-phase')">
                      <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dual-phase-packshot-YV5jY4gZl6MQnfXA45wiM4f0Y82L86.jpg" alt="Dual-Phase Serum">
                    </a>
                    <div class="floating-card-price">₹699</div>
                    <div class="floating-card-name">
                      <a href="product.html?id=stella-dual-phase" onclick="spaNavigate(event, 'product.html?id=stella-dual-phase')">Dual-Phase Serum</a>
                    </div>
                    <div class="floating-card-specs">30 ml / 1.0 FL. OZ</div>
                    <button class="btn-card-pill" onclick="addToBag('stella-dual-phase')">Add to Bag</button>
                  </div>

                  <div class="floating-product-card">
                    <a href="product.html?id=stella-bi-phase" class="floating-card-image" onclick="spaNavigate(event, 'product.html?id=stella-bi-phase')">
                      <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/bi-phase-packshot-hXf7XwL5pv7ugDOA0Vg45vKU8Qa7yy.jpg" alt="Bi-Phase Serum">
                    </a>
                    <div class="floating-card-price">₹649</div>
                    <div class="floating-card-name">
                      <a href="product.html?id=stella-bi-phase" onclick="spaNavigate(event, 'product.html?id=stella-bi-phase')">Bi-Phase Hydration</a>
                    </div>
                    <div class="floating-card-specs">30 ml / 1.0 FL. OZ</div>
                    <button class="btn-card-pill" onclick="addToBag('stella-bi-phase')">Add to Bag</button>
                  </div>
                </div>
              </div>

              <div class="hero-right-space">
                <div class="hero-stat-card">
                  <div class="hero-stat-number">750K+</div>
                  <div class="hero-stat-label">Daily Radiance Community</div>
                </div>

                <div class="hero-right-product">
                  <a href="product.html?id=stella-dahi-shampoo" class="floating-card-image" style="height: 100px;" onclick="spaNavigate(event, 'product.html?id=stella-dahi-shampoo')">
                    <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dahi-shampoo-clean-vCNEZjXkphoa2otEbyZZUwdDnO9m74.jpg" alt="Curd Shampoo">
                  </a>
                  <div class="floating-card-price">₹449</div>
                  <div class="floating-card-name">
                    <a href="product.html?id=stella-dahi-shampoo" onclick="spaNavigate(event, 'product.html?id=stella-dahi-shampoo')">Curd Protein Shampoo</a>
                  </div>
                  <div class="floating-card-specs">250 ml / 8.4 FL. OZ</div>
                  <button class="btn-card-pill" onclick="addToBag('stella-dahi-shampoo')">Add to Bag</button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Philosophy -->
        <section class="philosophy-strip">
          <div class="container">
            <div class="philosophy-grid">
              <div class="philosophy-item">
                <div class="philosophy-num">01 / GENTLE & EFFECTIVE</div>
                <h3 class="philosophy-title">Formulated with Intent</h3>
                <p class="philosophy-text">High-potency botanical extracts balanced for sensitive skin. Free of parabens, harsh sulfates, and toxic additives.</p>
              </div>
              <div class="philosophy-item">
                <div class="philosophy-num">02 / DEEP HYDRATION</div>
                <h3 class="philosophy-title">Barrier Protection</h3>
                <p class="philosophy-text">Multi-molecular Hyaluronic Acid and natural lipid oils to sustain skin hydration for up to 72 hours.</p>
              </div>
              <div class="philosophy-item">
                <div class="philosophy-num">03 / CLINICAL RESULTS</div>
                <h3 class="philosophy-title">Targeted Correction</h3>
                <p class="philosophy-text">Proven actives addressing pigmentation, body blemishes, and scalp clarity with daily simplicity.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Featured Vault -->
        <section class="catalog-section" id="featuredVault">
          <div class="container">
            <div class="catalog-header">
              <div>
                <span class="text-eyebrow">The Formulas</span>
                <h2 class="heading-lg" style="margin-top: 6px;">Featured Essentials</h2>
              </div>
              <a href="shop.html" class="btn-minimal btn-minimal-outline" onclick="spaNavigate(event, 'shop.html')">View All Formulations</a>
            </div>
            <div class="catalog-grid" id="homeCatalogGrid"></div>
          </div>
        </section>

        <!-- Dual-Phase Spotlight -->
        <section class="feature-section" id="science">
          <div class="container">
            <div class="feature-panel">
              <div class="feature-media">
                <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dual-phase-packshot-YV5jY4gZl6MQnfXA45wiM4f0Y82L86.jpg" alt="Dual-Phase Formulation">
              </div>
              <div class="feature-body">
                <span class="text-eyebrow">Innovation</span>
                <h2 class="heading-lg" style="margin: 8px 0 16px 0;">Dual-Phase Technology</h2>
                <p class="text-muted">Lipid nourishment and clinical water-soluble actives separated until application for maximum potency and fresh absorption.</p>
                <ul class="feature-points">
                  <li class="feature-point">
                    <span class="point-dot"></span>
                    <div class="point-text">
                      <strong>3% Tranexamic Acid & 4% Niacinamide</strong>
                      <span>Fades persistent hyperpigmentation and post-acne discoloration.</span>
                    </div>
                  </li>
                  <li class="feature-point">
                    <span class="point-dot"></span>
                    <div class="point-text">
                      <strong>Natural Licorice Oil & Vitamin B12</strong>
                      <span>Soothes dermal inflammation and imparts signature rose luminosity.</span>
                    </div>
                  </li>
                </ul>
                <div style="display: flex; gap: 14px; align-items: center; flex-wrap: wrap;">
                  <button class="btn-minimal btn-minimal-primary" onclick="addToBag('stella-dual-phase')">Add to Bag &bull; ₹699</button>
                  <a href="product.html?id=stella-dual-phase" class="btn-minimal btn-minimal-outline" onclick="spaNavigate(event, 'product.html?id=stella-dual-phase')">Learn More</a>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Curd Haircare Spotlight -->
        <section class="feature-section" id="hair" style="padding-top: 0;">
          <div class="container">
            <div class="feature-panel" style="background: #FDFBFC;">
              <div class="feature-body">
                <span class="text-eyebrow">Hair Restoration</span>
                <h2 class="heading-lg" style="margin: 8px 0 16px 0;">Curd Protein Therapy</h2>
                <p class="text-muted">The traditional restorative ritual redefined. Lactic acid gently lifts dandruff flakes while pure curd protein seals the cuticle for mirror-finish silkiness.</p>
                <div style="display: flex; gap: 12px; align-items: center; margin-top: 24px;">
                  <button class="btn-minimal btn-minimal-primary" onclick="addToBag('stella-dahi-shampoo')">Add to Bag &bull; ₹449</button>
                  <a href="haircare.html" class="btn-minimal btn-minimal-outline" onclick="spaNavigate(event, 'haircare.html')">Read Story</a>
                </div>
              </div>
              <div class="feature-media">
                <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dahi-shampoo-clean-vCNEZjXkphoa2otEbyZZUwdDnO9m74.jpg" alt="Dahi Shampoo Clean">
              </div>
            </div>
          </div>
        </section>

        <!-- Diagnostic Quiz Promo -->
        <section style="padding: 60px 0 80px 0;">
          <div class="container">
            <div style="background: #FCEEF2; border-radius: var(--radius-xl); padding: 50px 40px; text-align: center; border: 1px solid var(--color-border-subtle);">
              <span class="text-eyebrow">Personalized Skin Diagnostic</span>
              <h2 class="heading-lg" style="margin: 10px 0 14px 0;">Find Your Stellar Routine</h2>
              <p class="text-muted" style="max-width: 500px; margin: 0 auto 28px auto;">
                Answer 2 simple questions to get your dermatologist-balanced 3-step regimen and an automatic 20% bundle discount.
              </p>
              <a href="routine-finder.html" class="btn-minimal btn-minimal-primary" style="padding: 12px 28px;" onclick="spaNavigate(event, 'routine-finder.html')">Take Routine Quiz</a>
            </div>
          </div>
        </section>

        <!-- Notes of Appreciation -->
        <section class="editorial-quotes-section">
          <div class="container">
            <div style="text-align: center; margin-bottom: 40px;">
              <span class="text-eyebrow">Reviews</span>
              <h2 class="heading-lg" style="margin-top: 6px;">Notes of Appreciation</h2>
            </div>
            <div class="quotes-grid">
              <div class="quote-card">
                <p class="quote-text">&ldquo;The Dual-Phase Serum delivered visible clarity to my dark spots within three weeks. Lightweight and effortless.&rdquo;</p>
                <div class="quote-author">Avina V. &bull; Verified Buyer</div>
              </div>
              <div class="quote-card">
                <p class="quote-text">&ldquo;The Curd Protein Shampoo restored softness to my dry scalp without weighing my hair down. A staple formula.&rdquo;</p>
                <div class="quote-author">Ritu V. &bull; Verified Buyer</div>
              </div>
              <div class="quote-card">
                <p class="quote-text">&ldquo;Zero aluminum and gentle on sensitive underarm skin. The consistency and subtle fragrance are exceptional.&rdquo;</p>
                <div class="quote-author">Priya S. &bull; Verified Buyer</div>
              </div>
            </div>
          </div>
        </section>
      `;

      // Render home grid
      const grid = document.getElementById('homeCatalogGrid');
      if (grid) {
        const catalog = getCatalog().slice(0, 4);
        grid.innerHTML = catalog.map(p => `
          <div class="product-tile">
            <a href="product.html?id=${p.id}" class="product-media-box" onclick="spaNavigate(event, 'product.html?id=${p.id}')">
              <span class="product-badge-subtle">${p.badge}</span>
              <img src="${p.image}" alt="${p.name}" loading="lazy">
            </a>
            <div class="product-content">
              <span class="product-category-label">${p.category} &bull; ${p.volume}</span>
              <h3 class="product-name"><a href="product.html?id=${p.id}" onclick="spaNavigate(event, 'product.html?id=${p.id}')">${p.name}</a></h3>
              <p class="product-formula">${p.actives}</p>
              <div class="product-footer">
                <div class="product-price-block">
                  <span class="price-now">₹${p.price}</span>
                  <span class="price-was">₹${p.originalPrice}</span>
                </div>
                <button class="btn-add-tile" onclick="addToBag('${p.id}')">Add to Bag</button>
              </div>
            </div>
          </div>
        `).join('');
      }
    }

    // ==========================================
    // 2. SHOP VIEW
    // ==========================================
    let shopCat = 'all';
    let shopSort = 'default';
    let shopQuery = '';

    function renderShopView(el) {
      document.title = "The Stella — Full Collection";
      const params = new URLSearchParams(window.location.search);
      if (params.get('category')) shopCat = params.get('category');

      el.innerHTML = `
        <section class="page-header">
          <div class="container">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Collection</span>
            </div>
            <span class="text-eyebrow">Formulations</span>
            <h1 class="page-header-title">The Complete Vault</h1>
            <p class="page-header-subtitle">
              Everyday clinical essentials engineered with active botanicals, lipid nourishment, and zero unnecessary additives.
            </p>
          </div>
        </section>

        <section style="padding: 40px 0 80px 0;">
          <div class="container">
            <div class="shop-controls">
              <div class="catalog-filter-tabs" id="categoryFilterRow">
                <button class="tab-btn ${shopCat==='all'?'active':''}" onclick="filterShop('all')">All Formulations</button>
                <button class="tab-btn ${shopCat==='face'?'active':''}" onclick="filterShop('face')">Face Glow</button>
                <button class="tab-btn ${shopCat==='hair'?'active':''}" onclick="filterShop('hair')">Haircare</button>
                <button class="tab-btn ${shopCat==='body'?'active':''}" onclick="filterShop('body')">Body</button>
                <button class="tab-btn ${shopCat==='underarm'?'active':''}" onclick="filterShop('underarm')">Underarm</button>
              </div>

              <div style="display: flex; gap: 12px; align-items: center;">
                <input type="text" id="shopSearchInput" placeholder="Filter by active..." class="form-input" style="padding: 7px 14px; border-radius: var(--radius-pill); font-size: 0.8rem; width: 180px;" oninput="onShopSearch(this.value)">
                <select id="shopSortSelect" class="shop-sort-select" onchange="onShopSort(this.value)">
                  <option value="default">Sort: Recommended</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                  <option value="name">Alphabetical</option>
                </select>
              </div>
            </div>

            <div class="catalog-grid" id="shopProductGrid"></div>
          </div>
        </section>
      `;

      updateShopGrid();
    }

    function filterShop(cat) {
      shopCat = cat;
      document.querySelectorAll('#categoryFilterRow .tab-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      updateShopGrid();
    }

    function onShopSearch(q) {
      shopQuery = q;
      updateShopGrid();
    }

    function onShopSort(s) {
      shopSort = s;
      updateShopGrid();
    }

    function updateShopGrid() {
      const grid = document.getElementById('shopProductGrid');
      if (!grid) return;

      let catalog = [...getCatalog()];
      if (shopCat !== 'all') {
        catalog = catalog.filter(p => p.category === shopCat);
      }
      if (shopQuery.trim() !== '') {
        const q = shopQuery.toLowerCase();
        catalog = catalog.filter(p => p.name.toLowerCase().includes(q) || p.actives.toLowerCase().includes(q) || p.category.toLowerCase().includes(q));
      }
      if (shopSort === 'price-asc') catalog.sort((a, b) => a.price - b.price);
      else if (shopSort === 'price-desc') catalog.sort((a, b) => b.price - a.price);
      else if (shopSort === 'name') catalog.sort((a, b) => a.name.localeCompare(b.name));

      if (catalog.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 60px 20px;"><h3 style="font-family: var(--font-serif); font-size: 1.4rem; margin-bottom: 8px;">No matching formulations found</h3><p style="color: var(--color-text-secondary); font-size: 0.9rem;">Try adjusting your search criteria.</p></div>`;
        return;
      }

      grid.innerHTML = catalog.map(p => `
        <div class="product-tile">
          <a href="product.html?id=${p.id}" class="product-media-box" onclick="spaNavigate(event, 'product.html?id=${p.id}')">
            <span class="product-badge-subtle">${p.badge}</span>
            <img src="${p.image}" alt="${p.name}" loading="lazy">
          </a>
          <div class="product-content">
            <span class="product-category-label">${p.category} &bull; ${p.volume}</span>
            <h3 class="product-name"><a href="product.html?id=${p.id}" onclick="spaNavigate(event, 'product.html?id=${p.id}')">${p.name}</a></h3>
            <p class="product-formula">${p.actives}</p>
            <div class="product-footer">
              <div class="product-price-block">
                <span class="price-now">₹${p.price}</span>
                <span class="price-was">₹${p.originalPrice}</span>
              </div>
              <button class="btn-add-tile" onclick="addToBag('${p.id}')">Add to Bag</button>
            </div>
          </div>
        </div>
      `).join('');
    }

    // ==========================================
    // 3. PRODUCT DETAIL VIEW (PDP)
    // ==========================================
    let pdpQty = 1;

    function renderProductView(el) {
      const params = new URLSearchParams(window.location.search);
      const pid = params.get('id') || 'stella-dual-phase';
      const catalog = getCatalog();
      const p = catalog.find(item => item.id === pid) || catalog[0];

      document.title = `${p.name} — The Stella`;

      el.innerHTML = `
        <main class="container" style="padding-top: 30px;">
          <div class="breadcrumbs">
            <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; 
            <a href="shop.html" onclick="spaNavigate(event, 'shop.html')">Collection</a> &bull; 
            <span>${p.name}</span>
          </div>

          <div class="pdp-grid">
            <div class="pdp-gallery-box">
              <img src="${p.image}" alt="${p.name}">
            </div>

            <div>
              <span class="pdp-volume-box">${p.badge}</span>
              <h1 class="pdp-title">${p.name}</h1>
              <div style="font-size: 0.85rem; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">
                ${p.volume}
              </div>

              <div class="pdp-price-row">
                <span class="pdp-current-price">₹${p.price}</span>
                <span class="pdp-original-price">₹${p.originalPrice}</span>
                <span style="font-size: 0.78rem; font-weight: 700; color: #15803D; text-transform: uppercase;">In Stock &bull; Ships in 24h</span>
              </div>

              <p class="pdp-desc">${p.description}</p>

              <div class="pdp-actives-card">
                <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-primary); margin-bottom: 4px;">
                  Key Active Concentrations
                </div>
                <div style="font-size: 0.9rem; font-weight: 500; color: var(--color-text-main);">
                  ${p.actives}
                </div>
              </div>

              <div class="pdp-action-row">
                <div class="pdp-qty-selector">
                  <button onclick="changePdpQty(-1)">−</button>
                  <span id="pdpQtyVal">1</span>
                  <button onclick="changePdpQty(1)">+</button>
                </div>
                <button class="btn-minimal btn-minimal-primary" style="flex: 1; padding: 13px;" onclick="addToBag('${p.id}', pdpQty)">
                  Add to Bag
                </button>
                <button class="btn-minimal btn-minimal-outline" style="padding: 13px 20px;" onclick="addToBag('${p.id}', pdpQty); spaNavigate(null, 'checkout.html');">
                  Instant Checkout
                </button>
              </div>

              <div style="margin-bottom: 36px; padding: 14px 18px; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: #FFFFFF; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.85rem; color: var(--color-text-secondary);">Preferred platform?</span>
                <a href="https://www.flipkart.com" target="_blank" rel="noopener" style="font-size: 0.82rem; font-weight: 700; color: #2874F0; text-decoration: underline;">
                  Order on Flipkart Official Store
                </a>
              </div>

              <div class="pdp-tab-nav">
                <div class="pdp-tab-item active" onclick="switchPdpTab(0)">Application</div>
                <div class="pdp-tab-item" onclick="switchPdpTab(1)">Full Ingredients</div>
                <div class="pdp-tab-item" onclick="switchPdpTab(2)">Clinical Efficacy</div>
              </div>

              <div class="pdp-tab-pane active" id="tab0">
                <p>${p.howToUse}</p>
              </div>
              <div class="pdp-tab-pane" id="tab1">
                <p style="font-size: 0.82rem; font-family: monospace; line-height: 1.6;">${p.ingredients}</p>
              </div>
              <div class="pdp-tab-pane" id="tab2">
                <p>Dermatologically evaluated across 120 participants over a 28-day period. 94% reported noticeable skin brightness and 91% noted deep barrier replenishment without pore congestion. 100% cruelty-free and vegan.</p>
              </div>
            </div>
          </div>

          <section style="padding: 60px 0 80px 0; border-top: 1px solid var(--color-border-subtle); margin-top: 40px;">
            <div style="text-align: center; margin-bottom: 36px;">
              <span class="text-eyebrow">Complementary Care</span>
              <h2 class="heading-md" style="margin-top: 6px;">Recommended Regimen Additions</h2>
            </div>
            <div class="catalog-grid" id="relatedProductsGrid"></div>
          </section>
        </main>
      `;

      // Render related
      const related = catalog.filter(item => item.id !== p.id).slice(0, 3);
      const rgrid = document.getElementById('relatedProductsGrid');
      if (rgrid) {
        rgrid.innerHTML = related.map(item => `
          <div class="product-tile">
            <a href="product.html?id=${item.id}" class="product-media-box" onclick="spaNavigate(event, 'product.html?id=${item.id}')">
              <span class="product-badge-subtle">${item.badge}</span>
              <img src="${item.image}" alt="${item.name}" loading="lazy">
            </a>
            <div class="product-content">
              <span class="product-category-label">${item.category} &bull; ${item.volume}</span>
              <h3 class="product-name"><a href="product.html?id=${item.id}" onclick="spaNavigate(event, 'product.html?id=${item.id}')">${item.name}</a></h3>
              <p class="product-formula">${item.actives}</p>
              <div class="product-footer">
                <div class="product-price-block">
                  <span class="price-now">₹${item.price}</span>
                </div>
                <button class="btn-add-tile" onclick="addToBag('${item.id}')">Add to Bag</button>
              </div>
            </div>
          </div>
        `).join('');
      }
    }

    function changePdpQty(delta) {
      pdpQty = Math.max(1, pdpQty + delta);
      const val = document.getElementById('pdpQtyVal');
      if (val) val.textContent = pdpQty;
    }

    function switchPdpTab(idx) {
      document.querySelectorAll('.pdp-tab-item').forEach((tab, i) => {
        tab.classList.toggle('active', i === idx);
      });
      document.querySelectorAll('.pdp-tab-pane').forEach((pane, i) => {
        pane.classList.toggle('active', i === idx);
      });
    }

    // ==========================================
    // 4. HAIRCARE VIEW
    // ==========================================
    function renderHaircareView(el) {
      document.title = "Curd Protein Haircare Therapy — The Stella";
      el.innerHTML = `
        <section class="page-header">
          <div class="container">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Haircare</span>
            </div>
            <span class="text-eyebrow">Trichology Science</span>
            <h1 class="page-header-title">Curd Protein Haircare</h1>
            <p class="page-header-subtitle">
              The restorative Indian tradition perfected through clinical lactic acid clarification and bio-fermented whey proteins.
            </p>
          </div>
        </section>

        <section style="padding: 40px 0 80px 0;">
          <div class="container">
            <div class="feature-panel" style="margin-bottom: 60px;">
              <div class="feature-media">
                <img src="https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dahi-shampoo-clean-vCNEZjXkphoa2otEbyZZUwdDnO9m74.jpg" alt="Dahi Shampoo">
              </div>
              <div class="feature-body">
                <span class="text-eyebrow">Flagship Formulation</span>
                <h2 class="heading-lg" style="margin: 8px 0 16px 0;">Curd Protein Dahi Shampoo</h2>
                <p class="text-muted">
                  Unlike conventional anti-dandruff cleansers that strip natural scalp sebum with harsh zinc compounds, our Curd Protein system operates at physiological pH 5.2.
                </p>
                <ul class="feature-points">
                  <li class="feature-point">
                    <span class="point-dot"></span>
                    <div class="point-text">
                      <strong>Bio-Fermented Whey Protein</strong>
                      <span>Penetrates fractured hair shafts to seal cuticles and prevent moisture dissipation.</span>
                    </div>
                  </li>
                  <li class="feature-point">
                    <span class="point-dot"></span>
                    <div class="point-text">
                      <strong>Lactic Acid (AHA)</strong>
                      <span>Dissolves stubborn flake buildup and rebalances scalp microbial flora.</span>
                    </div>
                  </li>
                </ul>
                <div style="display: flex; gap: 14px; align-items: center; margin-top: 24px;">
                  <button class="btn-minimal btn-minimal-primary" onclick="addToBag('stella-dahi-shampoo')">
                    Add to Bag &bull; ₹449
                  </button>
                  <a href="product.html?id=stella-dahi-shampoo" class="btn-minimal btn-minimal-outline" onclick="spaNavigate(event, 'product.html?id=stella-dahi-shampoo')">
                    View Specifications
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>
      `;
    }

    // ==========================================
    // 5. ABOUT VIEW
    // ==========================================
    function renderAboutView(el) {
      document.title = "About The Stella — Botanical Dermatological Science";
      el.innerHTML = `
        <section class="page-header">
          <div class="container">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>About</span>
            </div>
            <span class="text-eyebrow">Our Philosophy</span>
            <h1 class="page-header-title">Clinical Botanicals for Everyday Glow</h1>
            <p class="page-header-subtitle">
              We engineer multi-active formulations that honor Indian skin biology with high-precision actives and sensory elegance.
            </p>
          </div>
        </section>

        <section style="padding: 40px 0 80px 0;">
          <div class="container" style="max-width: 800px;">
            <div style="margin-bottom: 40px;">
              <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 16px;">Dual-Action Formulation</h2>
              <p style="color: var(--color-text-secondary); line-height: 1.8; font-size: 1rem; margin-bottom: 20px;">
                Traditional cosmetics often dilute actives in heavy water fillers. The Stella separates bio-compatible liposomes and clinical water actives into balanced dual-phase solutions. When shaken, they homogenize into a fresh emulsion that penetrates deep without greasy residue.
              </p>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 40px;">
              <div style="background: #FDFBFC; border: 1px solid var(--color-border); padding: 24px; border-radius: var(--radius-lg);">
                <h4 style="font-family: var(--font-serif); font-size: 1.1rem; margin-bottom: 8px;">Dermatological Integrity</h4>
                <p style="font-size: 0.88rem; color: var(--color-text-secondary); line-height: 1.6;">Every percentage of Tranexamic Acid, Niacinamide, and Salicylic Acid is calibrated for maximum results with minimal irritation.</p>
              </div>
              <div style="background: #FDFBFC; border: 1px solid var(--color-border); padding: 24px; border-radius: var(--radius-lg);">
                <h4 style="font-family: var(--font-serif); font-size: 1.1rem; margin-bottom: 8px;">Zero Compromise</h4>
                <p style="font-size: 0.88rem; color: var(--color-text-secondary); line-height: 1.6;">Zero parabens, zero aluminum salts in underarm care, zero harsh SLS sulfates, and 100% cruelty-free formulations.</p>
              </div>
            </div>

            <div style="text-align: center; margin-top: 40px;">
              <a href="shop.html" class="btn-minimal btn-minimal-primary" onclick="spaNavigate(event, 'shop.html')">Explore Formulations</a>
            </div>
          </div>
        </section>
      `;
    }

    // ==========================================
    // 6. ROUTINE FINDER QUIZ VIEW
    // ==========================================
    let quizSkinType = 'combination';
    let quizConcern = 'pigmentation';

    function renderRoutineFinderView(el) {
      document.title = "Skin Routine Diagnostic — The Stella";
      el.innerHTML = `
        <section class="page-header">
          <div class="container">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Routine Diagnostic</span>
            </div>
            <span class="text-eyebrow">Diagnostic Engine</span>
            <h1 class="page-header-title">Find Your Stellar Regimen</h1>
            <p class="page-header-subtitle">
              Answer 2 questions to generate your targeted 3-step routine with an instant 20% discount code.
            </p>
          </div>
        </section>

        <section style="padding: 40px 0 80px 0;">
          <div class="container" style="max-width: 680px;">
            <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 36px 32px; box-shadow: var(--shadow-sm);">
              <!-- Step 1 -->
              <div style="margin-bottom: 28px;">
                <label style="display: block; font-weight: 700; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                  1. Your Skin Type
                </label>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                  <button type="button" class="tab-btn active" id="st-comb" onclick="selectSkinType('combination', this)">Combination</button>
                  <button type="button" class="tab-btn" id="st-dry" onclick="selectSkinType('dry', this)">Dry / Dehydrated</button>
                  <button type="button" class="tab-btn" id="st-oily" onclick="selectSkinType('oily', this)">Oily / Acne-Prone</button>
                </div>
              </div>

              <!-- Step 2 -->
              <div style="margin-bottom: 32px;">
                <label style="display: block; font-weight: 700; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                  2. Primary Concern
                </label>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                  <button type="button" class="tab-btn active" id="sc-pigm" onclick="selectConcern('pigmentation', this)">Dark Spots / Tone</button>
                  <button type="button" class="tab-btn" id="sc-dry" onclick="selectConcern('dryness', this)">Dullness / Dehydration</button>
                  <button type="button" class="tab-btn" id="sc-dand" onclick="selectConcern('dandruff', this)">Scalp Flakes & Hair</button>
                </div>
              </div>

              <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px;" onclick="calculateQuizResult()">
                Generate Recommended Protocol
              </button>
            </div>

            <!-- Quiz Result Output -->
            <div id="quizResultArea" style="margin-top: 36px;"></div>
          </div>
        </section>
      `;
    }

    function selectSkinType(type, btn) {
      quizSkinType = type;
      btn.parentElement.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    function selectConcern(concern, btn) {
      quizConcern = concern;
      btn.parentElement.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    function calculateQuizResult() {
      const area = document.getElementById('quizResultArea');
      if (!area) return;

      let p1 = 'stella-papaya-facewash';
      let p2 = 'stella-dual-phase';
      let p3 = 'stella-bodycare';

      if (quizConcern === 'dryness') {
        p2 = 'stella-bi-phase';
      } else if (quizConcern === 'dandruff') {
        p2 = 'stella-dahi-shampoo';
      }

      const c1 = getCatalog().find(p => p.id === p1);
      const c2 = getCatalog().find(p => p.id === p2);
      const c3 = getCatalog().find(p => p.id === p3);

      const subtotal = c1.price + c2.price + c3.price;
      const discounted = Math.round(subtotal * 0.8);

      area.innerHTML = `
        <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 32px; animation: fadeIn 0.3s ease;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div>
              <span class="text-eyebrow">Prescribed Protocol</span>
              <h3 style="font-family: var(--font-serif); font-size: 1.4rem;">Targeted 3-Step Regimen</h3>
            </div>
            <div style="background: #FCEEF2; color: var(--color-primary); font-size: 0.8rem; font-weight: 700; padding: 6px 12px; border-radius: var(--radius-pill);">
              20% OFF UNLOCKED
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
            <div style="background: #FFF; padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); text-align: center;">
              <img src="${c1.image}" alt="${c1.name}" style="height: 80px; object-fit: contain; margin-bottom: 8px;">
              <div style="font-size: 0.72rem; color: var(--color-text-secondary); text-transform: uppercase;">Step 1 &bull; Cleanse</div>
              <div style="font-size: 0.85rem; font-weight: 600;">${c1.name}</div>
            </div>
            <div style="background: #FFF; padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); text-align: center;">
              <img src="${c2.image}" alt="${c2.name}" style="height: 80px; object-fit: contain; margin-bottom: 8px;">
              <div style="font-size: 0.72rem; color: var(--color-text-secondary); text-transform: uppercase;">Step 2 &bull; Correct</div>
              <div style="font-size: 0.85rem; font-weight: 600;">${c2.name}</div>
            </div>
            <div style="background: #FFF; padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); text-align: center;">
              <img src="${c3.image}" alt="${c3.name}" style="height: 80px; object-fit: contain; margin-bottom: 8px;">
              <div style="font-size: 0.72rem; color: var(--color-text-secondary); text-transform: uppercase;">Step 3 &bull; Protect</div>
              <div style="font-size: 0.85rem; font-weight: 600;">${c3.name}</div>
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 16px; border-top: 1px solid var(--color-border);">
            <div>
              <span style="font-size: 0.85rem; color: var(--color-text-secondary);">Regimen Price:</span>
              <span style="text-decoration: line-through; color: var(--color-text-muted); font-size: 0.9rem; margin-left: 6px;">₹${subtotal}</span>
              <span style="font-size: 1.25rem; font-weight: 700; color: var(--color-primary); margin-left: 6px;">₹${discounted}</span>
            </div>
            <button class="btn-minimal btn-minimal-primary" onclick="addBundleToBag(['${c1.id}', '${c2.id}', '${c3.id}'])">
              Add Complete Routine to Bag
            </button>
          </div>
        </div>
      `;
    }

    function addBundleToBag(ids) {
      ids.forEach(id => addToBag(id, 1));
      showToast("3-Step Routine added with 20% discount unlocked!");
      spaNavigate(null, 'checkout.html');
    }

    // ==========================================
    // 7. CHECKOUT VIEW
    // ==========================================
    let checkoutDiscount = 0;

    function renderCheckoutView(el) {
      document.title = "Checkout & Shopping Bag — The Stella";
      const bag = getBag();
      const catalog = getCatalog();

      let subtotal = 0;
      const items = bag.map(item => {
        const prod = catalog.find(p => p.id === item.productId);
        if (!prod) return null;
        const total = prod.price * item.quantity;
        subtotal += total;
        return { ...item, prod, total };
      }).filter(Boolean);

      const shipping = subtotal >= 499 || subtotal === 0 ? 0 : 70;
      const discountAmount = Math.round(subtotal * checkoutDiscount);
      const grandTotal = Math.max(0, subtotal - discountAmount + shipping);

      el.innerHTML = `
        <div class="container" style="padding: 40px 0 80px 0; max-width: 900px;">
          <div class="breadcrumbs">
            <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Shopping Bag</span>
          </div>

          <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 24px;">Your Shopping Bag</h1>

          <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 32px;" id="checkoutGridContainer">
            <!-- Items Column -->
            <div>
              <div id="checkoutBagItems">
                ${items.length === 0 ? `
                  <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 48px; text-align: center;">
                    <p style="color: var(--color-text-secondary); margin-bottom: 16px;">Your shopping bag is currently empty.</p>
                    <a href="shop.html" class="btn-minimal btn-minimal-primary" onclick="spaNavigate(event, 'shop.html')">Explore Formulations</a>
                  </div>
                ` : items.map(it => `
                  <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px; margin-bottom: 12px; display: flex; gap: 16px; align-items: center;">
                    <img src="${it.prod.image}" alt="${it.prod.name}" style="width: 64px; height: 64px; object-fit: contain; border-radius: var(--radius-sm); background: #FAF9F8;">
                    <div style="flex: 1;">
                      <h4 style="font-size: 0.95rem; font-weight: 600; margin-bottom: 2px;">${it.prod.name}</h4>
                      <div style="font-size: 0.78rem; color: var(--color-text-secondary);">${it.prod.volume}</div>
                      <div style="font-size: 0.9rem; font-weight: 700; color: var(--color-text-main); margin-top: 4px;">₹${it.prod.price}</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <button onclick="updateBagQuantity('${it.productId}', ${it.quantity - 1}); renderCurrentRoute();" style="width: 24px; height: 24px; border: 1px solid var(--color-border); background: #FFF; border-radius: 4px; cursor: pointer;">−</button>
                      <span style="font-size: 0.85rem; font-weight: 600;">${it.quantity}</span>
                      <button onclick="updateBagQuantity('${it.productId}', ${it.quantity + 1}); renderCurrentRoute();" style="width: 24px; height: 24px; border: 1px solid var(--color-border); background: #FFF; border-radius: 4px; cursor: pointer;">+</button>
                    </div>
                    <button onclick="removeFromBag('${it.productId}'); renderCurrentRoute();" style="background: none; border: none; color: #DC2626; font-size: 0.8rem; cursor: pointer; padding: 4px 8px;">Remove</button>
                  </div>
                `).join('')}
              </div>

              <!-- Address Form -->
              <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; margin-top: 24px;">
                <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 16px;">Delivery Destination</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                  <input type="text" id="chkName" placeholder="Full Recipient Name" class="form-input" value="Avina Vasoya">
                  <input type="tel" id="chkPhone" placeholder="Mobile Contact" class="form-input" value="+91 98765 43210">
                </div>
                <input type="text" id="chkAddress" placeholder="Flat, Floor, Street Address" class="form-input" style="margin-bottom: 12px;" value="14 Crystal Avenue, Bandra West">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
                  <input type="text" id="chkCity" placeholder="City" class="form-input" value="Mumbai">
                  <input type="text" id="chkState" placeholder="State" class="form-input" value="Maharashtra">
                  <input type="text" id="chkPin" placeholder="PIN Code" class="form-input" value="400050">
                </div>
              </div>
            </div>

            <!-- Summary & Payment Column -->
            <div>
              <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; position: sticky; top: 90px;">
                <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 16px;">Order Summary</h3>

                <div style="display: flex; justify-content: space-between; font-size: 0.88rem; margin-bottom: 8px;">
                  <span style="color: var(--color-text-secondary);">Subtotal</span>
                  <span style="font-weight: 600;">₹${subtotal}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.88rem; margin-bottom: 8px;">
                  <span style="color: var(--color-text-secondary);">Pan-India Delivery</span>
                  <span style="font-weight: 600;">${shipping === 0 ? 'Complimentary' : '₹70'}</span>
                </div>
                ${discountAmount > 0 ? `
                  <div style="display: flex; justify-content: space-between; font-size: 0.88rem; margin-bottom: 8px; color: #15803D;">
                    <span>STELLA20 Discount</span>
                    <span>−₹${discountAmount}</span>
                  </div>
                ` : ''}

                <div style="border-top: 1px solid var(--color-border); margin: 16px 0; padding-top: 16px; display: flex; justify-content: space-between; font-size: 1.15rem; font-weight: 700;">
                  <span>Grand Total</span>
                  <span style="color: var(--color-primary);">₹${grandTotal}</span>
                </div>

                <!-- Promo Input -->
                <div style="display: flex; gap: 8px; margin-bottom: 20px;">
                  <input type="text" id="promoCodeInput" placeholder="Discount Code" class="form-input" style="font-size: 0.82rem; text-transform: uppercase;">
                  <button class="btn-minimal btn-minimal-outline" style="padding: 8px 14px;" onclick="applyPromo()">Apply</button>
                </div>

                <!-- Payment Selection -->
                <div style="margin-bottom: 20px;">
                  <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Payment Mode</label>
                  <select id="paymentMethodSelect" class="form-input" style="font-size: 0.85rem;">
                    <option value="UPI / QR">Instant UPI / QR Code</option>
                    <option value="Credit / Debit Card">Credit / Debit Card</option>
                    <option value="Cash on Delivery">Cash on Delivery (COD)</option>
                  </select>
                </div>

                <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px;" onclick="executeOrder(${grandTotal})">
                  Place Order Now
                </button>
              </div>
            </div>
          </div>

          <!-- Order Confirmed View Area -->
          <div id="confirmedOrderArea" style="display: none; margin-top: 24px;"></div>
        </div>
      `;
    }

    function applyPromo() {
      const code = document.getElementById('promoCodeInput')?.value.trim().toUpperCase();
      if (code === 'STELLA20') {
        checkoutDiscount = 0.20;
        showToast("Code STELLA20 applied: 20% discount deducted.");
        renderCurrentRoute();
      } else {
        showToast("Invalid promo code. Use code STELLA20.");
      }
    }

    function executeOrder(totalAmount) {
      const bag = getBag();
      if (bag.length === 0) {
        showToast("Shopping bag is empty.");
        return;
      }
      const name = document.getElementById('chkName')?.value || 'Guest';
      const phone = document.getElementById('chkPhone')?.value || '';
      const address = document.getElementById('chkAddress')?.value || '';
      const method = document.getElementById('paymentMethodSelect')?.value || 'UPI';

      const orderId = 'STL-' + Math.floor(10000 + Math.random() * 90000);
      const catalog = getCatalog();
      const orderItems = bag.map(item => {
        const prod = catalog.find(p => p.id === item.productId);
        return {
          productId: item.productId,
          name: prod ? prod.name : item.productId,
          price: prod ? prod.price : 0,
          quantity: item.quantity
        };
      });

      const orderObj = {
        id: orderId,
        date: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }),
        customerName: name,
        phone: phone,
        address: address,
        items: orderItems,
        total: totalAmount,
        paymentMethod: method,
        status: 'Processing'
      };

      saveOrder(orderObj);
      saveBag([]); // Clear bag
      updateHeaderBagBadge();

      // Show receipt
      const grid = document.getElementById('checkoutGridContainer');
      const conf = document.getElementById('confirmedOrderArea');
      if (grid) grid.style.display = 'none';
      if (conf) {
        conf.style.display = 'block';
        conf.innerHTML = `
          <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 40px; text-align: center; max-width: 600px; margin: 0 auto; box-shadow: var(--shadow-sm);">
            <span class="text-eyebrow">Payment Confirmed</span>
            <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin: 8px 0 16px 0;">Order Successfully Placed</h2>
            <p style="color: var(--color-text-secondary); margin-bottom: 24px;">Thank you for trusting The Stella. Your tracking ID has been generated.</p>
            
            <div style="background: #FDFBFC; border: 1px dashed var(--color-border); border-radius: var(--radius-md); padding: 16px; margin-bottom: 24px; font-family: monospace; font-size: 1.1rem; color: var(--color-primary); font-weight: 700;">
              Tracking ID: ${orderId}
            </div>

            <div style="text-align: left; background: #FAF9F8; padding: 16px; border-radius: var(--radius-md); margin-bottom: 24px; font-size: 0.88rem;">
              <div style="margin-bottom: 6px;"><strong>Recipient:</strong> ${name}</div>
              <div style="margin-bottom: 6px;"><strong>Delivery Address:</strong> ${address}</div>
              <div style="margin-bottom: 6px;"><strong>Amount Paid:</strong> ₹${totalAmount} via ${method}</div>
              <div><strong>Status:</strong> Processing (Dispatches in 24 hours)</div>
            </div>

            <div style="display: flex; gap: 12px; justify-content: center;">
              <a href="account.html" class="btn-minimal btn-minimal-primary" onclick="spaNavigate(event, 'account.html')">View in Account</a>
              <a href="shop.html" class="btn-minimal btn-minimal-outline" onclick="spaNavigate(event, 'shop.html')">Continue Shopping</a>
            </div>
          </div>
        `;
      }
    }

    // ==========================================
    // 8. ACCOUNT VIEW
    // ==========================================
    let accountAuthTab = 'signin';

    function renderAccountView(el) {
      document.title = "Customer Portal — The Stella";
      const currentUser = getCurrentUser();

      if (currentUser) {
        // Logged-in profile & order history
        const userOrders = getOrders();

        el.innerHTML = `
          <div class="container" style="padding: 40px 0 80px 0; max-width: 800px;">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Account</span>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
              <div>
                <span class="text-eyebrow">Customer Portal</span>
                <h1 style="font-family: var(--font-serif); font-size: 2rem;">Welcome, ${currentUser.name}</h1>
              </div>
              <button class="btn-minimal btn-minimal-outline" onclick="setCurrentUser(null); renderCurrentRoute();">Sign Out</button>
            </div>

            <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; margin-bottom: 32px;">
              <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 12px;">Profile Details</h3>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 0.9rem;">
                <div><span style="color: var(--color-text-secondary);">Email:</span> <strong>${currentUser.email}</strong></div>
                <div><span style="color: var(--color-text-secondary);">Saved Address:</span> <strong>${currentUser.address || '14 Crystal Avenue, Mumbai'}</strong></div>
              </div>
            </div>

            <h3 style="font-family: var(--font-serif); font-size: 1.4rem; margin-bottom: 16px;">Live Order History</h3>
            <div>
              ${userOrders.length === 0 ? `
                <div style="background: #FFF; border: 1px solid var(--color-border); padding: 32px; border-radius: var(--radius-md); text-align: center; color: var(--color-text-secondary);">No previous orders found.</div>
              ` : userOrders.map(ord => `
                <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; margin-bottom: 14px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                      <span style="font-family: monospace; font-weight: 700; color: var(--color-primary);">${ord.id}</span>
                      <span style="font-size: 0.8rem; color: var(--color-text-secondary); margin-left: 10px;">${ord.date}</span>
                    </div>
                    <span style="background: #FCEEF2; color: var(--color-primary); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: var(--radius-pill);">${ord.status}</span>
                  </div>
                  <div style="font-size: 0.88rem; color: var(--color-text-secondary); margin-bottom: 8px;">
                    ${ord.items.map(it => `${it.name} (x${it.quantity})`).join(', ')}
                  </div>
                  <div style="font-size: 0.92rem; font-weight: 700;">Total: ₹${ord.total}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else {
        // Sign In / Sign Up Form
        el.innerHTML = `
          <div class="container" style="padding: 40px 0 80px 0; max-width: 480px;">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Account</span>
            </div>

            <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 36px 32px; box-shadow: var(--shadow-sm);">
              <div style="display: flex; border-bottom: 1px solid var(--color-border); margin-bottom: 24px;">
                <button type="button" class="tab-btn ${accountAuthTab==='signin'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='signin'?'var(--color-primary)':'transparent'};" onclick="accountAuthTab='signin'; renderCurrentRoute();">Sign In</button>
                <button type="button" class="tab-btn ${accountAuthTab==='signup'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='signup'?'var(--color-primary)':'transparent'};" onclick="accountAuthTab='signup'; renderCurrentRoute();">Create Account</button>
              </div>

              ${accountAuthTab === 'signin' ? `
                <div style="margin-bottom: 14px;">
                  <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Email Address</label>
                  <input type="email" id="authEmail" class="form-input" value="user@thestella.in">
                </div>
                <div style="margin-bottom: 20px;">
                  <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Password</label>
                  <input type="password" id="authPassword" class="form-input" value="password123">
                </div>
                <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeUserSignIn()">Sign In to Stella</button>
                <p style="font-size: 0.78rem; color: var(--color-text-secondary); text-align: center; margin-top: 14px;">Test credentials prefilled for instant access.</p>
              ` : `
                <div style="margin-bottom: 12px;">
                  <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Full Name</label>
                  <input type="text" id="regName" class="form-input" placeholder="Avina Vasoya">
                </div>
                <div style="margin-bottom: 12px;">
                  <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Email</label>
                  <input type="email" id="regEmail" class="form-input" placeholder="avina@thestella.in">
                </div>
                <div style="margin-bottom: 20px;">
                  <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Password</label>
                  <input type="password" id="regPassword" class="form-input" placeholder="Create secure password">
                </div>
                <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeUserSignUp()">Create Account</button>
              `}
            </div>
          </div>
        `;
      }
    }

    function executeUserSignIn() {
      const email = document.getElementById('authEmail')?.value.trim();
      const pass = document.getElementById('authPassword')?.value.trim();
      const users = getUsers();
      const u = users.find(x => x.email === email && x.password === pass);
      if (u) {
        setCurrentUser(u);
        showToast("Signed in as " + u.name);
        renderCurrentRoute();
      } else {
        showToast("Invalid email or password.");
      }
    }

    function executeUserSignUp() {
      const name = document.getElementById('regName')?.value.trim();
      const email = document.getElementById('regEmail')?.value.trim();
      const pass = document.getElementById('regPassword')?.value.trim();
      if (!name || !email || !pass) {
        showToast("Please fill all fields.");
        return;
      }
      const users = getUsers();
      const newUser = { id: 'usr_' + Date.now(), name, email, password: pass };
      users.push(newUser);
      localStorage.setItem('stella_users', JSON.stringify(users));
      setCurrentUser(newUser);
      showToast("Account created successfully!");
      renderCurrentRoute();
    }

    // ==========================================
    // 9. ADMIN VIEW
    // ==========================================
    function renderAdminView(el) {
      document.title = "Admin Console — The Stella";
      const isAdmin = getAdminSession();

      if (!isAdmin) {
        el.innerHTML = `
          <div class="container" style="padding: 60px 0 100px 0; max-width: 440px;">
            <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 40px 32px; box-shadow: var(--shadow-sm); text-align: center;">
              <span class="text-eyebrow">Executive Management</span>
              <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin: 8px 0 20px 0;">Admin Portal</h2>

              <div style="text-align: left; margin-bottom: 14px;">
                <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Admin ID</label>
                <input type="email" id="adminUser" class="form-input" value="admin@thestella.in">
              </div>
              <div style="text-align: left; margin-bottom: 24px;">
                <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Security Key</label>
                <input type="password" id="adminPass" class="form-input" value="admin123">
              </div>
              <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeAdminAuth()">Authorize Console</button>
              <p style="font-size: 0.78rem; color: var(--color-text-secondary); margin-top: 14px;">Default admin credentials pre-loaded.</p>
            </div>
          </div>
        `;
      } else {
        const orders = getOrders();
        const catalog = getCatalog();
        const grossRev = orders.reduce((acc, o) => acc + (o.total || 0), 0);
        const pendingCount = orders.filter(o => o.status === 'Processing' || o.status === 'Pending').length;

        el.innerHTML = `
          <div class="container" style="padding: 30px 0 80px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px;">
              <div>
                <span class="text-eyebrow">Operations & Metrics</span>
                <h1 style="font-family: var(--font-serif); font-size: 2rem;">Executive Dashboard</h1>
              </div>
              <button class="btn-minimal btn-minimal-outline" onclick="setAdminSession(false); renderCurrentRoute();">Exit Admin</button>
            </div>

            <!-- KPI Counters -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px;">
              <div style="background: #FFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--color-text-secondary);">Gross Revenue</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: var(--color-primary); margin-top: 4px;">₹${grossRev}</div>
              </div>
              <div style="background: #FFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--color-text-secondary);">Total Orders</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: var(--color-text-main); margin-top: 4px;">${orders.length}</div>
              </div>
              <div style="background: #FFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--color-text-secondary);">Formulations</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: var(--color-text-main); margin-top: 4px;">${catalog.length}</div>
              </div>
              <div style="background: #FFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--color-text-secondary);">Pending Fulfillment</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #D97706; margin-top: 4px;">${pendingCount}</div>
              </div>
            </div>

            <!-- Orders Management -->
            <div style="background: #FFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; margin-bottom: 32px;">
              <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 16px;">Customer Order Fulfillment</h3>
              <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
                  <thead>
                    <tr style="border-bottom: 1px solid var(--color-border); color: var(--color-text-secondary);">
                      <th style="padding: 10px;">Order ID</th>
                      <th style="padding: 10px;">Recipient</th>
                      <th style="padding: 10px;">Products</th>
                      <th style="padding: 10px;">Amount</th>
                      <th style="padding: 10px;">Payment</th>
                      <th style="padding: 10px;">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${orders.map(o => `
                      <tr style="border-bottom: 1px solid var(--color-border-subtle);">
                        <td style="padding: 12px 10px; font-family: monospace; font-weight: 700;">${o.id}</td>
                        <td style="padding: 12px 10px;">${o.customerName}<br><span style="font-size: 0.75rem; color: var(--color-text-secondary);">${o.phone || ''}</span></td>
                        <td style="padding: 12px 10px; font-size: 0.82rem;">${o.items.map(it => it.name).join(', ')}</td>
                        <td style="padding: 12px 10px; font-weight: 600;">₹${o.total}</td>
                        <td style="padding: 12px 10px;">${o.paymentMethod || 'UPI'}</td>
                        <td style="padding: 12px 10px;">
                          <select onchange="updateOrderStatus('${o.id}', this.value); renderCurrentRoute();" style="padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid var(--color-border);">
                            <option value="Processing" ${o.status==='Processing'?'selected':''}>Processing</option>
                            <option value="Shipped" ${o.status==='Shipped'?'selected':''}>Shipped</option>
                            <option value="Delivered" ${o.status==='Delivered'?'selected':''}>Delivered</option>
                            <option value="Cancelled" ${o.status==='Cancelled'?'selected':''}>Cancelled</option>
                          </select>
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Product Price & Stock Editor -->
            <div style="background: #FFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px;">
              <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 16px;">Product Pricing & Stock Controller</h3>
              <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">
                ${catalog.map(prod => `
                  <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 14px; display: flex; gap: 12px; align-items: center;">
                    <img src="${prod.image}" alt="${prod.name}" style="width: 50px; height: 50px; object-fit: contain;">
                    <div style="flex: 1;">
                      <div style="font-weight: 600; font-size: 0.88rem;">${prod.name}</div>
                      <div style="display: flex; gap: 8px; margin-top: 6px; align-items: center;">
                        <span style="font-size: 0.8rem;">Price ₹:</span>
                        <input type="number" id="price_${prod.id}" value="${prod.price}" style="width: 70px; padding: 4px 6px; font-size: 0.82rem; border: 1px solid var(--color-border); border-radius: 4px;">
                        <button class="btn-minimal btn-minimal-outline" style="padding: 4px 10px; font-size: 0.75rem;" onclick="saveProdPrice('${prod.id}')">Save</button>
                      </div>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        `;
      }
    }

    function executeAdminAuth() {
      const u = document.getElementById('adminUser')?.value.trim();
      const p = document.getElementById('adminPass')?.value.trim();
      if (u === 'admin@thestella.in' && p === 'admin123') {
        setAdminSession(true);
        showToast("Admin session authorized.");
        renderCurrentRoute();
      } else {
        showToast("Invalid admin credentials.");
      }
    }

    function saveProdPrice(pid) {
      const input = document.getElementById('price_' + pid);
      if (!input) return;
      const newP = parseInt(input.value);
      if (isNaN(newP) || newP <= 0) return;
      const catalog = getCatalog();
      const p = catalog.find(x => x.id === pid);
      if (p) {
        p.price = newP;
        saveCatalog(catalog);
        showToast("Updated " + p.name + " price to ₹" + newP);
      }
    }

    // ==========================================
    // 10. CONTACT & TRACKING VIEW
    // ==========================================
    function renderContactView(el) {
      document.title = "Contact & Track Order — The Stella";
      el.innerHTML = `
        <section class="page-header">
          <div class="container">
            <div class="breadcrumbs">
              <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Contact</span>
            </div>
            <span class="text-eyebrow">Customer Care</span>
            <h1 class="page-header-title">Track Order & Inquiries</h1>
            <p class="page-header-subtitle">
              Locate active shipments or submit formulation questions to our client concierge.
            </p>
          </div>
        </section>

        <section style="padding: 40px 0 80px 0;">
          <div class="container" style="max-width: 800px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px;">
              <!-- Tracking Box -->
              <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px;">
                <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 12px;">Live Order Search</h3>
                <p style="font-size: 0.85rem; color: var(--color-text-secondary); margin-bottom: 16px;">Enter your Stella Order ID (e.g. STL-90412)</p>
                <div style="display: flex; gap: 8px; margin-bottom: 16px;">
                  <input type="text" id="trackInput" placeholder="STL-XXXXX" class="form-input" style="font-size: 0.85rem; text-transform: uppercase;">
                  <button class="btn-minimal btn-minimal-primary" style="padding: 8px 16px;" onclick="trackOrder()">Track</button>
                </div>
                <div id="trackResultBox"></div>
              </div>

              <!-- Inquiry Box -->
              <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px;">
                <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 12px;">Submit Inquiry</h3>
                <input type="text" id="inqName" placeholder="Your Name" class="form-input" style="margin-bottom: 10px;">
                <input type="email" id="inqEmail" placeholder="Email Address" class="form-input" style="margin-bottom: 10px;">
                <textarea id="inqMsg" rows="3" placeholder="How can we assist you with our formulations?" class="form-input" style="margin-bottom: 14px;"></textarea>
                <button class="btn-minimal btn-minimal-primary" style="width: 100%;" onclick="submitInquiry()">Send Message</button>
              </div>
            </div>
          </div>
        </section>
      `;
    }

    function trackOrder() {
      const q = document.getElementById('trackInput')?.value.trim().toUpperCase();
      const box = document.getElementById('trackResultBox');
      if (!box || !q) return;

      const orders = getOrders();
      const match = orders.find(o => o.id === q);
      if (match) {
        box.innerHTML = `
          <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 14px; font-size: 0.85rem; margin-top: 10px;">
            <div style="font-weight: 700; color: var(--color-primary); margin-bottom: 4px;">Found: ${match.id}</div>
            <div><strong>Recipient:</strong> ${match.customerName}</div>
            <div><strong>Status:</strong> <span style="background: #FCEEF2; padding: 2px 6px; border-radius: 4px; font-weight: 700;">${match.status}</span></div>
            <div><strong>Order Total:</strong> ₹${match.total}</div>
          </div>
        `;
      } else {
        box.innerHTML = `<p style="color: #DC2626; font-size: 0.85rem; margin-top: 10px;">Order ID not found in database.</p>`;
      }
    }

    function submitInquiry() {
      const name = document.getElementById('inqName')?.value.trim();
      const email = document.getElementById('inqEmail')?.value.trim();
      const msg = document.getElementById('inqMsg')?.value.trim();
      if (!name || !email || !msg) {
        showToast("Please fill out all inquiry fields.");
        return;
      }
      showToast("Thank you " + name + ". Your inquiry has been dispatched to concierge.");
      document.getElementById('inqName').value = '';
      document.getElementById('inqEmail').value = '';
      document.getElementById('inqMsg').value = '';
    }

    // Initialize SPA on load
    document.addEventListener('DOMContentLoaded', () => {
      renderCurrentRoute();
    });
  </script>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(spa_html)

print('Master SPA index.html written successfully! Length:', len(spa_html), 'chars')
