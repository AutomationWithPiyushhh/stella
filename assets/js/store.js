/**
 * THE STELLA — CENTRAL DATA STORE & LOGIC
 * Manages Catalog, Bag, Wishlist, Orders, User Auth & Admin Sessions.
 * Strictly Zero Emojis. Clean Minimalist Architecture.
 */

// 1. Initial Master Product Catalog
const DEFAULT_CATALOG = [
  {
    id: 'stella-dual-phase',
    name: 'Dual-Phase De-Pigmentation Serum',
    category: 'face',
    volume: '30 ml / 1.0 FL. OZ',
    price: 699,
    originalPrice: 899,
    stock: 42,
    badge: 'Formula 01',
    actives: '3% Tranexamic Acid • 4% Niacinamide • Vitamin B12 • Licorice Oil',
    description: 'A targeted two-phase clinical formula that combines lipid-soluble Licorice Oil with water-soluble Tranexamic Acid and Niacinamide. Designed to address stubborn hyperpigmentation, melasma, and post-acne marks while maintaining the skin barrier.',
    howToUse: 'Shake vigorously for 4 seconds to emulsify the lipid and water phases. Press 3-4 drops into cleansed face and neck morning and evening. Follow with sunscreen during daylight hours.',
    ingredients: 'Aqua, Tranexamic Acid (3%), Niacinamide (4%), Vitamin B12 (Cyanocobalamin), 4-Butylresorcinol, Glycyrrhiza Glabra (Licorice) Root Extract, Squalane, Glycerin, Sodium Hyaluronate, Tocopherol, Phenoxyethanol.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dual-phase-packshot-YV5jY4gZl6MQnfXA45wiM4f0Y82L86.jpg'
  },
  {
    id: 'stella-bi-phase',
    name: 'Bi-Phase Hydration Glow Serum',
    category: 'face',
    volume: '30 ml / 1.0 FL. OZ',
    price: 649,
    originalPrice: 799,
    stock: 38,
    badge: 'Formula 02',
    actives: '2% Polyglutamic Acid • Cica Stem Cell • 25% Bakuchiol & Rosehip',
    description: 'A deep moisture-locking formulation featuring botanical Bakuchiol and Rosehip Seed Oil atop an oceanic base of Polyglutamic Acid and Centella Stem Cells. Provides up to 72 hours of cellular hydration and gentle barrier renewal.',
    howToUse: 'Shake well to combine the golden oil and hydrating base. Gently pat 3-4 drops onto damp skin prior to moisturizers.',
    ingredients: 'Rosa Canina (Rosehip) Seed Oil, Bakuchiol (1%), Polyglutamic Acid (2%), Niacinamide (3%), Centella Asiatica Stem Cell Extract, Coco-Caprylate, Sodium Hyaluronate, Panthenol.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/bi-phase-packshot-hXf7XwL5pv7ugDOA0Vg45vKU8Qa7yy.jpg'
  },
  {
    id: 'stella-dahi-shampoo',
    name: 'Curd Protein Conditioning Shampoo',
    category: 'hair',
    volume: '250 ml / 8.4 FL. OZ',
    price: 449,
    originalPrice: 599,
    stock: 65,
    badge: 'Haircare',
    actives: 'Pure Curd Protein • Natural Lactic Acid • Built-in Conditioner',
    description: 'Restores scalp balance through bio-fermented curd proteins and mild lactic acid exfoliation. Clarifies flake accumulation, relieves itchiness, and smooths hair cuticles without drying sulfates.',
    howToUse: 'Massage thoroughly into wet scalp and lengths. Allow active proteins to penetrate for 2 minutes before rinsing with cool water. Conditioner built-in.',
    ingredients: 'Purified Water, Hydrolyzed Curd Protein, Sodium Cocoyl Isethionate, Lactic Acid, Biotin, D-Panthenol, Hydrolyzed Keratin, Aloe Barbadensis Leaf Juice, Argania Spinosa Kernel Oil.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/dahi-shampoo-clean-vCNEZjXkphoa2otEbyZZUwdDnO9m74.jpg'
  },
  {
    id: 'stella-underarm-rollon',
    name: 'Underarm Confidence Roll-On',
    category: 'underarm',
    volume: '50 ml / 1.7 FL. OZ',
    price: 299,
    originalPrice: 399,
    stock: 80,
    badge: 'UnderGlow',
    actives: '2% Niacinamide • Alpha Arbutin • 0% Aluminum',
    description: 'Non-irritating, aluminum-free underarm therapy designed to gradually lighten post-friction and shaving discoloration while neutralizing odor-causing bacteria for 48 hours.',
    howToUse: 'Glide evenly over clean, dry underarms daily. Allow 30 seconds to absorb before dressing.',
    ingredients: 'Aqua, Niacinamide (2%), Alpha Arbutin (1%), Licorice Extract, Chamomile Flower Water, Witch Hazel, Zinc Ricinoleate, Allantoin.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/underarm-rollon-packshot-ZkCK5viBuhw6HvSFzl2vzARajZfmA2.jpg'
  },
  {
    id: 'stella-salicylic-body-wash',
    name: '1% Salicylic Acid Clarifying Body Wash',
    category: 'body',
    volume: '200 ml / 6.7 FL. OZ',
    price: 499,
    originalPrice: 649,
    stock: 50,
    badge: 'Body Care',
    actives: '1% Salicylic Acid • Tea Tree Oil • Cooling Menthol',
    description: 'Dissolves trapped dead skin cells and excess sebum in pores across the back, chest, and arms. Helps clear body blemishes, rough strawberry texture, and ingrown hairs.',
    howToUse: 'Lather over wet body skin using hands or a gentle cloth. Focus on blemish-prone areas for 60 seconds before rinsing.',
    ingredients: 'Purified Water, Salicylic Acid (1%), Melaleuca Alternifolia (Tea Tree) Leaf Oil, Aloe Barbadensis Leaf Extract, Cocamidopropyl Betaine, Glycerin, Menthol.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/salicylic-body-wash-packshot-dawMRC9uvYrAxhQGCdQys0NB2FPvf8.jpg'
  },
  {
    id: 'stella-papaya-cleanser',
    name: 'Papaya Clean Anti-Blemish Wash',
    category: 'face',
    volume: '100 ml / 3.4 FL. OZ',
    price: 349,
    originalPrice: 449,
    stock: 55,
    badge: 'Cleanser',
    actives: 'Natural Papain Enzyme • Vitamin E • Micro-Glycolic',
    description: 'Enzyme-based gentle foaming cleanser that dissolves dull surface keratin without stripping essential moisture. Promotes a smooth, clarified complexion.',
    howToUse: 'Work a small amount into lather with water. Gently massage across damp skin for 45 seconds, then rinse.',
    ingredients: 'Aqua, Carica Papaya Fruit Extract, Tocopheryl Acetate (Vitamin E), Sodium Lauroyl Sarcosinate, Cocamidopropyl Betaine, Glycolic Acid, Glycerin.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/papaya-facewash-packshot-7lbLV8fn8WBn2zNXWWVJbhCwyQ5KOl.jpg'
  },
  {
    id: 'stella-vitamin-c',
    name: '10% Vitamin C Radiance Serum',
    category: 'face',
    volume: '30 ml / 1.0 FL. OZ',
    price: 599,
    originalPrice: 749,
    stock: 35,
    badge: 'Antioxidant',
    actives: '10% Ethyl Ascorbic Acid • Ferulic Acid • Hyaluronic Acid',
    description: 'A stabilized morning antioxidant solution that shields against daily environmental stressors, supports collagen density, and promotes overall skin luminosity.',
    howToUse: 'Apply 3-4 drops each morning to clean face and neck before moisturizer and sunscreen.',
    ingredients: 'Aqua, 3-O-Ethyl Ascorbic Acid (10%), Ferulic Acid (0.5%), Sodium Hyaluronate, Citrus Aurantium Dulcis Peel Oil, Phenoxyethanol.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/vitamin-c-serum-packshot-i0XYZLbgFPYhbmg1LpOkGZbySfBPdz.jpg'
  },
  {
    id: 'stella-body-lotion',
    name: 'Deep Hydration Body Lotion',
    category: 'body',
    volume: '200 ml / 6.7 FL. OZ',
    price: 479,
    originalPrice: 599,
    stock: 45,
    badge: 'Nourishment',
    actives: 'Raw Shea Butter • Triple Hyaluronic Acid • Vitamin E',
    description: 'A velvet lipid-replenishing body treatment designed for dry, flake-prone skin. Leaves an unnoticeable, non-sticky satin veil that locks in moisture all day.',
    howToUse: 'Smooth generously over the body immediately after showering while skin is slightly damp.',
    ingredients: 'Aqua, Butyrospermum Parkii (Shea) Butter, Hyaluronic Acid Complex, Prunus Amygdalus Dulcis (Sweet Almond) Oil, Tocopherol, Cetearyl Alcohol.',
    image: 'https://yjvwhwhqqsiaau2p.public.blob.vercel-storage.com/bodycare-packshot-2e0ZN5RpHr3GdQvxrDtl6g8sV502d0.jpg'
  }
];

// Initialize Catalog in LocalStorage if not present
function getCatalog() {
  const stored = localStorage.getItem('stella_catalog');
  if (!stored) {
    localStorage.setItem('stella_catalog', JSON.stringify(DEFAULT_CATALOG));
    return DEFAULT_CATALOG;
  }
  return JSON.parse(stored);
}

function saveCatalog(catalog) {
  localStorage.setItem('stella_catalog', JSON.stringify(catalog));
}

// 2. Shopping Bag Store
function getBag() {
  return JSON.parse(localStorage.getItem('stella_bag') || '[]');
}

function saveBag(bag) {
  localStorage.setItem('stella_bag', JSON.stringify(bag));
  updateHeaderBagBadge();
}

function addToBag(id, quantity = 1) {
  const bag = getBag();
  const existing = bag.find(item => item.id === id);
  if (existing) {
    existing.quantity += quantity;
  } else {
    bag.push({ id, quantity });
  }
  saveBag(bag);
  
  const catalog = getCatalog();
  const product = catalog.find(p => p.id === id);
  showToast(product ? `${product.name} added to bag` : 'Item added');
}

function updateBagQuantity(id, delta) {
  const bag = getBag();
  const idx = bag.findIndex(item => item.id === id);
  if (idx > -1) {
    bag[idx].quantity += delta;
    if (bag[idx].quantity <= 0) {
      bag.splice(idx, 1);
    }
    saveBag(bag);
  }
}

function removeFromBag(id) {
  const bag = getBag().filter(item => item.id !== id);
  saveBag(bag);
  showToast('Item removed from bag');
}

// 3. User Authentication Store
const DEFAULT_USERS = [
  {
    name: 'Piyush Baldaniya',
    email: 'user@thestella.in',
    password: 'password123',
    phone: '+91 98765 43210',
    joinedDate: '2026-01-15',
    addresses: [
      {
        id: 'addr-1',
        title: 'Home',
        line1: '402, Stella Horizon, Diamond Avenue',
        city: 'Ahmedabad',
        state: 'Gujarat',
        pincode: '380015',
        isDefault: true
      }
    ]
  }
];

function getUsers() {
  const stored = localStorage.getItem('stella_users');
  if (!stored) {
    localStorage.setItem('stella_users', JSON.stringify(DEFAULT_USERS));
    return DEFAULT_USERS;
  }
  return JSON.parse(stored);
}

function getCurrentUser() {
  const stored = localStorage.getItem('stella_current_user');
  return stored ? JSON.parse(stored) : null;
}

function setCurrentUser(user) {
  if (user) {
    localStorage.setItem('stella_current_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('stella_current_user');
  }
  updateHeaderAuthUI();
}

// 4. Admin Authentication Store
const ADMIN_CREDENTIALS = {
  email: 'admin@thestella.in',
  password: 'admin123',
  name: 'Lead Administrator',
  role: 'Store Manager'
};

function getAdminSession() {
  const stored = localStorage.getItem('stella_admin_session');
  return stored ? JSON.parse(stored) : null;
}

function setAdminSession(admin) {
  if (admin) {
    localStorage.setItem('stella_admin_session', JSON.stringify(admin));
  } else {
    localStorage.removeItem('stella_admin_session');
  }
}

// 5. Orders Database Store
const DEFAULT_ORDERS = [
  {
    orderId: 'STL-90412',
    date: '2026-11-18',
    customerName: 'Piyush Baldaniya',
    customerEmail: 'user@thestella.in',
    customerPhone: '+91 98765 43210',
    address: '402, Stella Horizon, Diamond Avenue, Ahmedabad, Gujarat 380015',
    items: [
      { id: 'stella-dual-phase', name: 'Dual-Phase De-Pigmentation Serum', price: 699, quantity: 1 },
      { id: 'stella-dahi-shampoo', name: 'Curd Protein Conditioning Shampoo', price: 449, quantity: 1 }
    ],
    subtotal: 1148,
    discount: 230,
    shipping: 0,
    total: 918,
    paymentMethod: 'UPI',
    status: 'Shipped',
    trackingNumber: 'DEL-99281928'
  },
  {
    orderId: 'STL-88194',
    date: '2026-11-14',
    customerName: 'Avina Vasoya',
    customerEmail: 'avina@example.com',
    customerPhone: '+91 91234 56789',
    address: 'B-12, Green Park, Surat, Gujarat 395007',
    items: [
      { id: 'stella-bi-phase', name: 'Bi-Phase Hydration Glow Serum', price: 649, quantity: 2 }
    ],
    subtotal: 1298,
    discount: 260,
    shipping: 0,
    total: 1038,
    paymentMethod: 'Credit Card',
    status: 'Delivered',
    trackingNumber: 'DEL-88219412'
  }
];

function getOrders() {
  const stored = localStorage.getItem('stella_orders');
  if (!stored) {
    localStorage.setItem('stella_orders', JSON.stringify(DEFAULT_ORDERS));
    return DEFAULT_ORDERS;
  }
  return JSON.parse(stored);
}

function saveOrder(order) {
  const orders = getOrders();
  orders.unshift(order);
  localStorage.setItem('stella_orders', JSON.stringify(orders));

  // Sync to Cloud Firestore in real time
  if (window.StellaFirebase && window.StellaFirebase.db) {
    window.StellaFirebase.db.createOrder(order).catch(err => {
      console.warn('Firestore order sync notice:', err.message);
    });
  }
}

function updateOrderStatus(orderId, newStatus) {
  const orders = getOrders();
  const order = orders.find(o => (o.orderId === orderId || o.id === orderId));
  if (order) {
    order.status = newStatus;
    localStorage.setItem('stella_orders', JSON.stringify(orders));
  }

  // Sync status update to Cloud Firestore
  if (window.StellaFirebase && window.StellaFirebase.db) {
    window.StellaFirebase.db.updateOrderStatus(orderId, newStatus).catch(err => {
      console.warn('Firestore status update notice:', err.message);
    });
  }
}

// 6. UI Helpers
function showToast(message) {
  let toast = document.querySelector('.toast-bar');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast-bar';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.style.display = 'block';

  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => {
    toast.style.display = 'none';
  }, 2800);
}

function updateHeaderBagBadge() {
  const badges = document.querySelectorAll('.bag-count-badge');
  const bag = getBag();
  const count = bag.reduce((sum, item) => sum + item.quantity, 0);
  badges.forEach(b => {
    b.textContent = count;
  });
}

function updateHeaderAuthUI() {
  const authLinks = document.querySelectorAll('.header-auth-status');
  const currentUser = getCurrentUser();
  const currentAdmin = getAdminSession();

  authLinks.forEach(el => {
    if (currentAdmin) {
      el.innerHTML = `<a href="admin.html" style="font-weight: 600; color: #D8315B;">Admin Portal</a>`;
    } else if (currentUser) {
      el.innerHTML = `<a href="account.html" style="font-weight: 600;">Account (${currentUser.name.split(' ')[0]})</a>`;
    } else {
      el.innerHTML = `<a href="account.html">Sign In</a>`;
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  updateHeaderBagBadge();
  updateHeaderAuthUI();

  // Initialize and synchronize with Firebase Cloud Firestore
  if (window.StellaFirebase) {
    if (typeof window.StellaFirebase.init === 'function') {
      window.StellaFirebase.init();
    }

    if (window.StellaFirebase.db) {
      // Seed products on first run if Firestore collection is empty
      window.StellaFirebase.db.seedProductsIfEmpty(DEFAULT_CATALOG);

      // Real-time bidirectional order sync
      window.StellaFirebase.db.listenOrders(remoteOrders => {
        if (Array.isArray(remoteOrders) && remoteOrders.length > 0) {
          localStorage.setItem('stella_orders', JSON.stringify(remoteOrders));
          // If viewing admin or account page, refresh view
          if (window.location.pathname.includes('admin') || window.location.pathname.includes('account')) {
            if (typeof renderCurrentRoute === 'function') {
              renderCurrentRoute();
            }
          }
        }
      });

      // Real-time catalog sync
      window.StellaFirebase.db.listenProducts(remoteProducts => {
        if (Array.isArray(remoteProducts) && remoteProducts.length > 0) {
          localStorage.setItem('stella_catalog', JSON.stringify(remoteProducts));
          if (typeof renderCurrentRoute === 'function') {
            renderCurrentRoute();
          }
        }
      });
    }

    // Observe Firebase Authentication state changes
    if (window.StellaFirebase.auth) {
      window.StellaFirebase.auth.onAuthStateChanged(fbUser => {
        if (fbUser) {
          const profile = {
            id: fbUser.uid,
            uid: fbUser.uid,
            name: fbUser.displayName || (fbUser.phoneNumber ? 'Client (' + fbUser.phoneNumber.slice(-4) + ')' : fbUser.email.split('@')[0]),
            email: fbUser.email || (fbUser.phoneNumber ? fbUser.phoneNumber + '@thestella.in' : ''),
            phone: fbUser.phoneNumber || ''
          };
          setCurrentUser(profile);
        }
      });
    }
  }
});
