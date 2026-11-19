/**
 * THE STELLA — MINIMALIST LUXURY SCRIPT
 * High-performance state management, bag drawer, wishlist, and catalog filtering.
 * Zero emojis. Clean editorial typography.
 */

const STELLA_CATALOG = [
  {
    id: 'stella-dual-phase',
    name: 'Dual-Phase De-Pigmentation Serum',
    category: 'face',
    volume: '30 ml / 1.0 FL. OZ',
    price: 699,
    originalPrice: 899,
    badge: 'Formula 01',
    actives: '3% Tranexamic Acid • 4% Niacinamide • Vitamin B12',
    image: 'assets/images/products/dual-phase-packshot.jpg'
  },
  {
    id: 'stella-bi-phase',
    name: 'Bi-Phase Hydration Glow Serum',
    category: 'face',
    volume: '30 ml / 1.0 FL. OZ',
    price: 649,
    originalPrice: 799,
    badge: 'Formula 02',
    actives: '2% Polyglutamic Acid • Cica Stem Cell • Bakuchiol',
    image: 'assets/images/products/bi-phase-packshot.jpg'
  },
  {
    id: 'stella-dahi-shampoo',
    name: 'Curd Protein Conditioning Shampoo',
    category: 'hair',
    volume: '250 ml / 8.4 FL. OZ',
    price: 449,
    originalPrice: 599,
    badge: 'Haircare',
    actives: 'Pure Curd Protein • Lactic Acid • Built-in Conditioner',
    image: 'assets/images/products/dahi-shampoo-clean.jpg'
  },
  {
    id: 'stella-underarm-rollon',
    name: 'Underarm Confidence Roll-On',
    category: 'underarm',
    volume: '50 ml / 1.7 FL. OZ',
    price: 299,
    originalPrice: 399,
    badge: 'UnderGlow',
    actives: '2% Niacinamide • Alpha Arbutin • 0% Aluminum',
    image: 'assets/images/products/underarm-rollon-packshot.jpg'
  },
  {
    id: 'stella-salicylic-body-wash',
    name: '1% Salicylic Acid Body Wash',
    category: 'body',
    volume: '200 ml / 6.7 FL. OZ',
    price: 499,
    originalPrice: 649,
    badge: 'Body Care',
    actives: '1% Salicylic Acid • Tea Tree • Cooling Menthol',
    image: 'assets/images/products/salicylic-body-wash-packshot.jpg'
  },
  {
    id: 'stella-papaya-cleanser',
    name: 'Papaya Clean Anti-Blemish Wash',
    category: 'face',
    volume: '100 ml / 3.4 FL. OZ',
    price: 349,
    originalPrice: 449,
    badge: 'Cleanser',
    actives: 'Natural Papain Enzyme • Vitamin E • Micro-Glycolic',
    image: 'assets/images/products/papaya-facewash-packshot.jpg'
  },
  {
    id: 'stella-vitamin-c',
    name: '10% Vitamin C Radiance Serum',
    category: 'face',
    volume: '30 ml / 1.0 FL. OZ',
    price: 599,
    originalPrice: 749,
    badge: 'Antioxidant',
    actives: '10% Ethyl Ascorbic Acid • Ferulic Acid • Hyaluronic',
    image: 'assets/images/products/vitamin-c-serum-packshot.jpg'
  },
  {
    id: 'stella-body-lotion',
    name: 'Deep Hydration Body Lotion',
    category: 'body',
    volume: '200 ml / 6.7 FL. OZ',
    price: 479,
    originalPrice: 599,
    badge: 'Nourishment',
    actives: 'Raw Shea Butter • Triple Hyaluronic Acid • Vitamin E',
    image: 'assets/images/products/bodycare-packshot.jpg'
  }
];

const State = {
  cart: JSON.parse(localStorage.getItem('stella_bag') || '[]'),
  category: 'all',
  discountPercent: 0.20,
  freeShippingAt: 499
};

// Seed bag if empty
if (State.cart.length === 0) {
  State.cart = [
    { id: 'stella-dual-phase', quantity: 1 },
    { id: 'stella-dahi-shampoo', quantity: 1 }
  ];
  saveBag();
}

function saveBag() {
  localStorage.setItem('stella_bag', JSON.stringify(State.cart));
  updateBagUI();
}

function addToBag(id, qty = 1) {
  const item = State.cart.find(i => i.id === id);
  if (item) {
    item.quantity += qty;
  } else {
    State.cart.push({ id, quantity: qty });
  }
  saveBag();
  
  const product = STELLA_CATALOG.find(p => p.id === id);
  showToast(product ? `${product.name} added to bag` : 'Item added');
  openBagDrawer();
}

function updateBagQty(id, delta) {
  const idx = State.cart.findIndex(i => i.id === id);
  if (idx > -1) {
    State.cart[idx].quantity += delta;
    if (State.cart[idx].quantity <= 0) {
      State.cart.splice(idx, 1);
    }
    saveBag();
  }
}

function removeFromBag(id) {
  State.cart = State.cart.filter(i => i.id !== id);
  saveBag();
  showToast('Item removed from bag');
}

function openBagDrawer() {
  document.getElementById('drawerScrim')?.classList.add('open');
  document.getElementById('cartPanel')?.classList.add('open');
}

function closeBagDrawer() {
  document.getElementById('drawerScrim')?.classList.remove('open');
  document.getElementById('cartPanel')?.classList.remove('open');
}

function updateBagUI() {
  const badge = document.getElementById('bagCountBadge');
  const itemsContainer = document.getElementById('bagItemsContainer');
  const subtotalEl = document.getElementById('bagSubtotal');
  const discountEl = document.getElementById('bagDiscount');
  const totalEl = document.getElementById('bagTotal');

  const totalUnits = State.cart.reduce((sum, item) => sum + item.quantity, 0);
  if (badge) badge.textContent = totalUnits;

  if (!itemsContainer) return;

  if (State.cart.length === 0) {
    itemsContainer.innerHTML = `
      <div style="text-align: center; padding: 60px 20px;">
        <h4 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 8px;">Your Shopping Bag is Empty</h4>
        <p style="color: var(--color-text-secondary); font-size: 0.88rem;">Explore the collection for everyday skin radiance.</p>
        <button class="btn-minimal btn-minimal-primary" style="margin-top: 20px;" onclick="closeBagDrawer(); scrollToCatalog();">
          Explore Products
        </button>
      </div>
    `;
    if (subtotalEl) subtotalEl.textContent = '₹0';
    if (discountEl) discountEl.textContent = '—';
    if (totalEl) totalEl.textContent = '₹0';
    return;
  }

  let subtotal = 0;
  itemsContainer.innerHTML = State.cart.map(item => {
    const product = STELLA_CATALOG.find(p => p.id === item.id);
    if (!product) return '';
    const totalItemPrice = product.price * item.quantity;
    subtotal += totalItemPrice;

    return `
      <div class="cart-tile">
        <div class="cart-tile-thumb">
          <img src="${product.image}" alt="${product.name}">
        </div>
        <div class="cart-tile-info">
          <div class="cart-tile-title">${product.name}</div>
          <div class="cart-tile-price">₹${product.price} <span style="font-size: 0.72rem; color: var(--color-text-tertiary);">(${product.volume})</span></div>
          <div class="cart-qty-row">
            <div class="qty-control">
              <button onclick="updateBagQty('${product.id}', -1)">−</button>
              <span>${item.quantity}</span>
              <button onclick="updateBagQty('${product.id}', 1)">+</button>
            </div>
            <span class="cart-remove-link" onclick="removeFromBag('${product.id}')">Remove</span>
          </div>
        </div>
      </div>
    `;
  }).join('');

  const discount = Math.round(subtotal * State.discountPercent);
  const finalTotal = subtotal - discount;

  if (subtotalEl) subtotalEl.textContent = `₹${subtotal}`;
  if (discountEl) discountEl.textContent = `-₹${discount} (STELLA20)`;
  if (totalEl) totalEl.textContent = `₹${finalTotal}`;
}

function renderCatalog() {
  const container = document.getElementById('catalogGrid');
  if (!container) return;

  let items = STELLA_CATALOG;
  if (State.category !== 'all') {
    items = items.filter(p => p.category === State.category);
  }

  container.innerHTML = items.map(product => `
    <div class="product-tile">
      <div class="product-media-box">
        <span class="product-badge-subtle">${product.badge}</span>
        <img src="${product.image}" alt="${product.name}" loading="lazy">
      </div>
      <div class="product-content">
        <span class="product-category-label">${product.category}</span>
        <h3 class="product-name">${product.name}</h3>
        <p class="product-formula">${product.actives}</p>
        <div class="product-footer">
          <div class="product-price-block">
            <span class="price-now">₹${product.price}</span>
            <span class="price-was">₹${product.originalPrice}</span>
          </div>
          <button class="btn-add-tile" onclick="addToBag('${product.id}')">
            Add
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

function showToast(msg) {
  let toast = document.querySelector('.toast-bar');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast-bar';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.display = 'block';

  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => {
    toast.style.display = 'none';
  }, 2800);
}

function scrollToCatalog() {
  document.getElementById('catalog')?.scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
  renderCatalog();
  updateBagUI();

  // Scroll Header
  window.addEventListener('scroll', () => {
    const header = document.querySelector('.site-header');
    if (header) {
      header.classList.toggle('scrolled', window.scrollY > 30);
    }
  });

  // Filter Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      State.category = e.target.dataset.filter;
      renderCatalog();
    });
  });

  // Newsletter
  const form = document.getElementById('footerNewsletter');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      showToast('Thank you for subscribing.');
      form.reset();
    });
  }
});
