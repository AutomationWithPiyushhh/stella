import re

with open('assets/js/app.js', 'r') as f:
    content = f.read()

# Replacement block covering Sections 6, 7, and 8
replacement = '''// ==========================================
// 6. CLINICAL ROUTINE DIAGNOSTIC ENGINE
// ==========================================
let quizSkinType = 'dry';
let quizConcern = 'dryness';
let quizEnvironment = 'indoor';

function renderRoutineFinderView(el) {
document.title = "Skin Routine Diagnostic — The Stella";
el.innerHTML = `
<section class="page-header">
<div class="container">
<div class="breadcrumbs">
<a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Routine Diagnostic</span>
</div>
<span class="text-eyebrow">Dermatological Consultation</span>
<h1 class="page-header-title">Find Your Stellar Regimen</h1>
<p class="page-header-subtitle">
Complete a tailored diagnostic evaluation to receive your dermatologist-grade 3-step protocol with an instant 20% discount code.
</p>
</div>
</section>
<section style="padding: 40px 0 80px 0;">
<div class="container" style="max-width: 740px;">
<div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 36px 32px; box-shadow: var(--shadow-sm);">

<div style="margin-bottom: 26px;">
<label style="display: block; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
1. Your Primary Skin Barrier Type
</label>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
<button type="button" class="tab-btn ${quizSkinType==='dry'?'active':''}" onclick="selectSkinType('dry', this)">Dry / Dehydrated</button>
<button type="button" class="tab-btn ${quizSkinType==='combination'?'active':''}" onclick="selectSkinType('combination', this)">Combination</button>
<button type="button" class="tab-btn ${quizSkinType==='oily'?'active':''}" onclick="selectSkinType('oily', this)">Oily / Acne-Prone</button>
</div>
</div>

<div style="margin-bottom: 26px;">
<label style="display: block; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
2. Primary Dermatological Focus
</label>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
<button type="button" class="tab-btn ${quizConcern==='dryness'?'active':''}" onclick="selectConcern('dryness', this)">Dullness / Dehydration</button>
<button type="button" class="tab-btn ${quizConcern==='pigmentation'?'active':''}" onclick="selectConcern('pigmentation', this)">Dark Spots / Tone</button>
<button type="button" class="tab-btn ${quizConcern==='dandruff'?'active':''}" onclick="selectConcern('dandruff', this)">Scalp Flakes & Hair</button>
</div>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px;">
<button type="button" class="tab-btn ${quizConcern==='body'?'active':''}" onclick="selectConcern('body', this)">Body Blemishes & Texture</button>
<button type="button" class="tab-btn ${quizConcern==='underarm'?'active':''}" onclick="selectConcern('underarm', this)">Underarm Discoloration</button>
</div>
</div>

<div style="margin-bottom: 30px;">
<label style="display: block; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
3. Daily Environment & Climate
</label>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
<button type="button" class="tab-btn ${quizEnvironment==='urban'?'active':''}" onclick="selectEnvironment('urban', this)">Urban Pollution & Sun</button>
<button type="button" class="tab-btn ${quizEnvironment==='indoor'?'active':''}" onclick="selectEnvironment('indoor', this)">Air-Conditioned Indoors</button>
<button type="button" class="tab-btn ${quizEnvironment==='outdoor'?'active':''}" onclick="selectEnvironment('outdoor', this)">Outdoor Humid / Active</button>
</div>
</div>

<button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-size: 0.95rem; font-weight: 600;" onclick="calculateQuizResult()">
Generate Prescribed Protocol
</button>
</div>

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
const parent = btn.closest('div').parentElement;
parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
btn.classList.add('active');
}
function selectEnvironment(env, btn) {
quizEnvironment = env;
btn.parentElement.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
btn.classList.add('active');
}

function calculateQuizResult() {
const area = document.getElementById('quizResultArea');
if (!area) return;

const catalog = getCatalog();
let p1 = 'stella-papaya-facewash';
let p2 = 'stella-bi-phase';
let p3 = 'stella-body-lotion';
let diagnosisTitle = 'Lipid Replenishing & Deep Moisture Protocol';
let diagnosisSummary = 'Dermatological findings indicate transepidermal water loss (TEWL) and compromised intercellular lipid reserves. The prescribed regimen utilizes botanical Bakuchiol, Polyglutamic Acid, and Raw Shea Lipids to seal deep hydration for up to 72 hours.';

if (quizConcern === 'pigmentation') {
  p1 = 'stella-papaya-facewash';
  p2 = 'stella-dual-phase';
  p3 = 'stella-vitamin-c';
  diagnosisTitle = 'Hyperpigmentation & Tone Uniformity Protocol';
  diagnosisSummary = 'Cellular melanogenesis analysis indicates post-inflammatory pigment accumulation. The recommended protocol combines enzymatic surface renewal with Tranexamic Acid and multi-molecular hydration to interrupt pigment pathways while rebuilding the stratum corneum.';
} else if (quizConcern === 'dandruff') {
  p1 = 'stella-dahi-shampoo';
  p2 = 'stella-bi-phase';
  p3 = 'stella-salicylic-body-wash';
  diagnosisTitle = 'Microbiome Clarifying & Flake Defense Protocol';
  diagnosisSummary = 'Scalp trichology analysis shows desquamation of the follicular stratum corneum and micro-scaling. Bio-fermented Curd Protein and Natural Lactic Acid dissolve adherent flakes without stripping, rebalancing the cutaneous ecosystem.';
} else if (quizConcern === 'body') {
  p1 = 'stella-salicylic-body-wash';
  p2 = 'stella-body-lotion';
  p3 = 'stella-underarm-rollon';
  diagnosisTitle = 'Keratosis Smoothing & Blemish Defense Protocol';
  diagnosisSummary = 'Clinical inspection reveals trapped follicular keratin and rough strawberry skin texture across chest and limbs. 1% Salicylic Acid exfoliates lipid-soluble debris inside pores while shea ceramides restore smooth elasticity.';
} else if (quizConcern === 'underarm') {
  p1 = 'stella-salicylic-body-wash';
  p2 = 'stella-underarm-rollon';
  p3 = 'stella-body-lotion';
  diagnosisTitle = 'Axillary Clarity & Odor Neutralization Protocol';
  diagnosisSummary = 'Axillary friction and shaving stress have induced melanin darkening. 2% Niacinamide and Alpha Arbutin gradually restore natural tone while non-aluminum minerals provide 48-hour antimicrobial freshness.';
}

const c1 = catalog.find(p => p.id === p1) || catalog[0];
const c2 = catalog.find(p => p.id === p2) || catalog[1];
const c3 = catalog.find(p => p.id === p3) || catalog[2];
const subtotal = c1.price + c2.price + c3.price;
const discounted = Math.round(subtotal * 0.8);
const savings = subtotal - discounted;

area.innerHTML = `
<div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 36px 32px; animation: fadeIn 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
<div>
<span class="text-eyebrow">Clinical Prescription</span>
<h3 style="font-family: var(--font-serif); font-size: 1.45rem; margin-top: 4px;">${diagnosisTitle}</h3>
</div>
<div style="background: #FCEEF2; color: var(--color-primary); font-size: 0.78rem; font-weight: 700; padding: 6px 14px; border-radius: var(--radius-pill); letter-spacing: 0.05em;">
20% BUNDLE DISCOUNT APPLIED
</div>
</div>

<p style="font-size: 0.88rem; color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 26px; border-left: 2px solid var(--color-primary); padding-left: 14px;">
${diagnosisSummary}
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px;">
<div style="background: #FFF; padding: 18px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); text-align: center; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="font-size: 0.72rem; color: var(--color-primary); font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Step 1 &bull; Clarify</div>
<img src="${c1.image}" alt="${c1.name}" style="height: 88px; object-fit: contain; margin: 0 auto 10px auto; display: block;">
<div style="font-size: 0.86rem; font-weight: 600; line-height: 1.3;">${c1.name}</div>
</div>
<div style="font-size: 0.82rem; font-weight: 700; color: var(--color-text-main); margin-top: 10px;">₹${c1.price}</div>
</div>

<div style="background: #FFF; padding: 18px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); text-align: center; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="font-size: 0.72rem; color: var(--color-primary); font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Step 2 &bull; Correct</div>
<img src="${c2.image}" alt="${c2.name}" style="height: 88px; object-fit: contain; margin: 0 auto 10px auto; display: block;">
<div style="font-size: 0.86rem; font-weight: 600; line-height: 1.3;">${c2.name}</div>
</div>
<div style="font-size: 0.82rem; font-weight: 700; color: var(--color-text-main); margin-top: 10px;">₹${c2.price}</div>
</div>

<div style="background: #FFF; padding: 18px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); text-align: center; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="font-size: 0.72rem; color: var(--color-primary); font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Step 3 &bull; Protect</div>
<img src="${c3.image}" alt="${c3.name}" style="height: 88px; object-fit: contain; margin: 0 auto 10px auto; display: block;">
<div style="font-size: 0.86rem; font-weight: 600; line-height: 1.3;">${c3.name}</div>
</div>
<div style="font-size: 0.82rem; font-weight: 700; color: var(--color-text-main); margin-top: 10px;">₹${c3.price}</div>
</div>
</div>

<div style="display: flex; justify-content: space-between; align-items: center; padding-top: 20px; border-top: 1px solid var(--color-border); flex-wrap: wrap; gap: 14px;">
<div>
<div style="font-size: 0.82rem; color: var(--color-text-secondary);">Prescription Total (Save ₹${savings}):</div>
<span style="text-decoration: line-through; color: var(--color-text-muted); font-size: 0.95rem;">₹${subtotal}</span>
<span style="font-size: 1.35rem; font-weight: 700; color: var(--color-primary); margin-left: 8px;">₹${discounted}</span>
</div>
<button class="btn-minimal btn-minimal-primary" style="padding: 12px 24px; font-weight: 600;" onclick="addBundleToBag(['${c1.id}', '${c2.id}', '${c3.id}'])">
Add Prescribed Protocol to Bag
</button>
</div>
</div>
`;
area.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function addBundleToBag(ids) {
ids.forEach(id => addToBag(id, 1));
checkoutDiscount = 0.20;
showToast("Prescribed Protocol added to bag with 20% discount applied!");
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
const prodId = item.id || item.productId;
const prod = catalog.find(p => p.id === prodId);
if (!prod) return null;
const total = prod.price * item.quantity;
subtotal += total;
return { ...item, id: prodId, prod, total };
}).filter(Boolean);

const currentUser = getCurrentUser();
const defaultName = currentUser ? currentUser.name : 'Valued Client';
const defaultPhone = currentUser ? (currentUser.phone || '+91 98765 43210') : '+91 98765 43210';
const defaultAddress = currentUser ? (currentUser.address || '14 Crystal Avenue, Bandra West') : '14 Crystal Avenue, Bandra West';

const shipping = subtotal >= 499 || subtotal === 0 ? 0 : 70;
const discountAmount = Math.round(subtotal * checkoutDiscount);
const grandTotal = Math.max(0, subtotal - discountAmount + shipping);

el.innerHTML = `
<div class="container" style="padding: 40px 0 80px 0;">
<div class="breadcrumbs">
<a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Shopping Bag</span>
</div>
<h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 24px;">Your Shopping Bag</h1>
<div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 32px;" id="checkoutGridContainer">
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
<button onclick="updateBagQuantity('${it.id}', -1); renderCurrentRoute();" style="width: 28px; height: 28px; border: 1px solid var(--color-border); background: #FFF; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1rem;">−</button>
<span style="font-size: 0.9rem; font-weight: 600; min-width: 20px; text-align: center;">${it.quantity}</span>
<button onclick="updateBagQuantity('${it.id}', 1); renderCurrentRoute();" style="width: 28px; height: 28px; border: 1px solid var(--color-border); background: #FFF; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1rem;">+</button>
</div>
<button onclick="removeFromBag('${it.id}'); renderCurrentRoute();" style="background: none; border: none; color: #DC2626; font-size: 0.82rem; cursor: pointer; padding: 4px 8px; text-decoration: underline;">Remove</button>
</div>
`).join('')}
</div>

<div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; margin-top: 24px;">
<h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 16px;">Delivery Destination</h3>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
<input type="text" id="chkName" placeholder="Full Recipient Name" class="form-input" value="${defaultName}">
<input type="tel" id="chkPhone" placeholder="Mobile Contact" class="form-input" value="${defaultPhone}">
</div>
<input type="text" id="chkAddress" placeholder="Flat, Floor, Street Address" class="form-input" style="margin-bottom: 12px;" value="${defaultAddress}">
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
<input type="text" id="chkCity" placeholder="City" class="form-input" value="Mumbai">
<input type="text" id="chkState" placeholder="State" class="form-input" value="Maharashtra">
<input type="text" id="chkPin" placeholder="PIN Code" class="form-input" value="400050">
</div>
</div>
</div>

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
<div style="display: flex; gap: 8px; margin-bottom: 20px;">
<input type="text" id="promoCodeInput" placeholder="Discount Code" class="form-input" style="font-size: 0.82rem; text-transform: uppercase;">
<button class="btn-minimal btn-minimal-outline" style="padding: 8px 14px;" onclick="applyPromo()">Apply</button>
</div>
<div style="margin-bottom: 20px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Payment Method</label>
<select id="paymentMethodSelect" class="form-input">
<option value="Instant UPI / QR Code">Instant UPI / QR Code</option>
<option value="Credit / Debit Card">Credit / Debit Card</option>
<option value="NetBanking">NetBanking (All Indian Banks)</option>
<option value="Cash on Delivery">Cash on Delivery</option>
</select>
</div>
<button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-weight: 600;" onclick="placeOrder(${grandTotal})">
Place Order Now
</button>
</div>
</div>
</div>
<div id="confirmedOrderArea" style="display: none; margin-top: 40px;"></div>
</div>
`;
}

function applyPromo() {
const val = document.getElementById('promoCodeInput')?.value.trim().toUpperCase();
if (val === 'STELLA20') {
checkoutDiscount = 0.20;
showToast("Promo Code STELLA20 Applied: 20% Off!");
renderCurrentRoute();
} else {
showToast("Invalid promo code. Use STELLA20 for 20% off.");
}
}

function placeOrder(totalAmount) {
const bag = getBag();
if (bag.length === 0) {
showToast("Shopping bag is empty.");
return;
}
const catalog = getCatalog();
const validItems = bag.map(item => {
const prodId = item.id || item.productId;
const prod = catalog.find(p => p.id === prodId);
if (!prod) return null;
return {
id: prodId,
productId: prodId,
name: prod.name,
price: prod.price,
quantity: item.quantity
};
}).filter(Boolean);

const name = document.getElementById('chkName')?.value.trim() || 'Valued Client';
const phone = document.getElementById('chkPhone')?.value.trim() || '';
const address = document.getElementById('chkAddress')?.value.trim() || '';
const city = document.getElementById('chkCity')?.value.trim() || '';
const state = document.getElementById('chkState')?.value.trim() || '';
const pin = document.getElementById('chkPin')?.value.trim() || '';
const fullAddress = [address, city, state, pin].filter(Boolean).join(', ');
const method = document.getElementById('paymentMethodSelect')?.value || 'UPI';
const orderId = 'STL-' + Math.floor(10000 + Math.random() * 90000);
const currentUser = getCurrentUser();

const orderObj = {
id: orderId,
orderId: orderId,
date: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }),
customerName: name,
customerEmail: currentUser ? currentUser.email : '',
userId: currentUser ? (currentUser.id || currentUser.uid) : '',
phone: phone,
address: fullAddress || 'Standard Delivery',
items: validItems,
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
<p style="color: var(--color-text-secondary); margin-bottom: 24px;">Thank you for trusting The Stella. Your tracking ID has been generated and saved to your account.</p>
<div style="background: #FDFBFC; border: 1px dashed var(--color-border); border-radius: var(--radius-md); padding: 16px; margin-bottom: 24px; font-family: monospace; font-size: 1.1rem; color: var(--color-primary); font-weight: 700;">
Tracking ID: ${orderId}
</div>
<div style="text-align: left; background: #FAF9F8; padding: 16px; border-radius: var(--radius-md); margin-bottom: 24px; font-size: 0.88rem;">
<div style="margin-bottom: 6px;"><strong>Recipient:</strong> ${name}</div>
<div style="margin-bottom: 6px;"><strong>Delivery Address:</strong> ${fullAddress}</div>
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
// 8. ACCOUNT VIEW (CUSTOMER PORTAL)
// ==========================================
let accountAuthTab = 'signin';

function renderAccountView(el) {
document.title = "Customer Portal — The Stella";
const currentUser = getCurrentUser();
if (currentUser) {
// Filter orders specifically for this authenticated customer
const allOrders = getOrders();
const userOrders = allOrders.filter(ord => {
  if (!currentUser) return false;
  const userEmail = (currentUser.email || '').toLowerCase().trim();
  const ordEmail = (ord.customerEmail || '').toLowerCase().trim();
  const userPhone = (currentUser.phone || '').replace(/\D/g, '');
  const ordPhone = (ord.phone || '').replace(/\D/g, '');
  const isEmailMatch = Boolean(userEmail && ordEmail && userEmail === ordEmail);
  const isPhoneMatch = Boolean(userPhone && ordPhone && userPhone.length >= 10 && userPhone.slice(-10) === ordPhone.slice(-10));
  const isUserIdMatch = Boolean(ord.userId && (ord.userId === currentUser.id || ord.userId === currentUser.uid));
  return isEmailMatch || isPhoneMatch || isUserIdMatch;
});

// Personalized product curation based on gender, age, skinType, and primary concern
const catalog = getCatalog();
let curatedProducts = [];
const focusConcern = (currentUser.concern || '').toLowerCase();
const focusSkin = (currentUser.skinType || '').toLowerCase();

if (focusConcern.includes('pigment') || focusConcern.includes('dark spot')) {
  curatedProducts = catalog.filter(p => p.id === 'stella-dual-phase' || p.id === 'stella-vitamin-c' || p.id === 'stella-papaya-facewash');
} else if (focusConcern.includes('flake') || focusConcern.includes('dandruff') || focusConcern.includes('hair')) {
  curatedProducts = catalog.filter(p => p.id === 'stella-dahi-shampoo' || p.id === 'stella-bi-phase' || p.id === 'stella-salicylic-body-wash');
} else if (focusConcern.includes('body') || focusConcern.includes('texture')) {
  curatedProducts = catalog.filter(p => p.id === 'stella-salicylic-body-wash' || p.id === 'stella-body-lotion');
} else if (focusConcern.includes('underarm')) {
  curatedProducts = catalog.filter(p => p.id === 'stella-underarm-rollon' || p.id === 'stella-salicylic-body-wash');
} else {
  curatedProducts = catalog.filter(p => p.id === 'stella-bi-phase' || p.id === 'stella-papaya-facewash' || p.id === 'stella-body-lotion');
}
if (curatedProducts.length === 0) curatedProducts = catalog.slice(0, 3);

el.innerHTML = `
<div class="container" style="padding: 40px 0 80px 0; max-width: 840px;">
<div class="breadcrumbs">
<a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Account</span>
</div>

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; flex-wrap: wrap; gap: 12px;">
<div>
<span class="text-eyebrow">Customer Portal</span>
<h1 style="font-family: var(--font-serif); font-size: 2rem;">Welcome, ${currentUser.name}</h1>
</div>
<button class="btn-minimal btn-minimal-outline" onclick="setCurrentUser(null); renderCurrentRoute();">Sign Out</button>
</div>

<!-- Profile Card with Demographics & Skin Focus -->
<div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 26px; margin-bottom: 32px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid var(--color-border); padding-bottom: 12px;">
<h3 style="font-family: var(--font-serif); font-size: 1.25rem;">Client Profile</h3>
<span style="font-size: 0.75rem; background: #FCEEF2; color: var(--color-primary); font-weight: 700; padding: 4px 10px; border-radius: var(--radius-pill);">Active Member</span>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; font-size: 0.88rem;">
<div><span style="color: var(--color-text-secondary); display: block; font-size: 0.75rem; text-transform: uppercase;">Email Address</span><strong>${currentUser.email || 'Not provided'}</strong></div>
<div><span style="color: var(--color-text-secondary); display: block; font-size: 0.75rem; text-transform: uppercase;">Mobile Contact</span><strong>${currentUser.phone || 'Not provided'}</strong></div>
<div><span style="color: var(--color-text-secondary); display: block; font-size: 0.75rem; text-transform: uppercase;">Demographic</span><strong>${currentUser.gender || 'Client'} &bull; ${currentUser.ageGroup || 'Adult'}</strong></div>
<div><span style="color: var(--color-text-secondary); display: block; font-size: 0.75rem; text-transform: uppercase;">Skin Profile</span><strong>${currentUser.skinType || 'Balanced'}</strong></div>
<div style="grid-column: 1 / -1;"><span style="color: var(--color-text-secondary); display: block; font-size: 0.75rem; text-transform: uppercase;">Primary Concern</span><strong>${currentUser.concern || 'Radiance & Hydration'}</strong></div>
</div>
</div>

<!-- Curated Formulations Section -->
<div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; margin-bottom: 36px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
<div>
<span class="text-eyebrow">Personalized For You</span>
<h3 style="font-family: var(--font-serif); font-size: 1.25rem;">Curated For Your Skin Profile</h3>
</div>
<span style="font-size: 0.78rem; color: var(--color-text-secondary);">Filtered by: ${currentUser.concern || 'Hydration'}</span>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px;">
${curatedProducts.map(p => `
<div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 14px; text-align: center; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<img src="${p.image}" alt="${p.name}" style="height: 76px; object-fit: contain; margin: 0 auto 8px auto; display: block;">
<h4 style="font-size: 0.85rem; font-weight: 600; line-height: 1.3; margin-bottom: 4px;">${p.name}</h4>
<div style="font-size: 0.72rem; color: var(--color-text-secondary); margin-bottom: 8px;">${p.actives.split('•')[0]}</div>
</div>
<div>
<div style="font-size: 0.9rem; font-weight: 700; margin-bottom: 8px;">₹${p.price}</div>
<button class="btn-minimal btn-minimal-primary" style="font-size: 0.78rem; padding: 6px 14px; width: 100%;" onclick="addToBag('${p.id}', 1)">Add to Bag</button>
</div>
</div>
`).join('')}
</div>
</div>

<!-- Live Order History -->
<h3 style="font-family: var(--font-serif); font-size: 1.35rem; margin-bottom: 16px;">Your Order History</h3>
<div>
${userOrders.length === 0 ? `
<div style="background: #FFFFFF; border: 1px dashed var(--color-border); border-radius: var(--radius-lg); padding: 48px 24px; text-align: center;">
<p style="color: var(--color-text-secondary); margin-bottom: 16px; font-size: 0.92rem;">You have not placed any orders yet. Once you make your first purchase, live order status and dispatch updates will appear here.</p>
<a href="shop.html" class="btn-minimal btn-minimal-primary" onclick="spaNavigate(event, 'shop.html')">Explore Formulations</a>
</div>
` : userOrders.map(ord => `
<div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; margin-bottom: 14px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
<div>
<span style="font-family: monospace; font-weight: 700; color: var(--color-primary); font-size: 0.95rem;">${ord.id || ord.orderId}</span>
<span style="font-size: 0.8rem; color: var(--color-text-secondary); margin-left: 10px;">${ord.date}</span>
</div>
<span style="background: #FCEEF2; color: var(--color-primary); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: var(--radius-pill);">${ord.status}</span>
</div>
<div style="font-size: 0.88rem; color: var(--color-text-secondary); margin-bottom: 8px;">
${(ord.items || []).map(it => `${it.name} (x${it.quantity})`).join(', ')}
</div>
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.92rem;">
<div><strong>Total Paid:</strong> ₹${ord.total} via ${ord.paymentMethod || 'Online'}</div>
<a href="contact.html" style="font-size: 0.8rem; color: var(--color-primary); text-decoration: underline;" onclick="spaNavigate(event, 'contact.html')">Track Shipment</a>
</div>
</div>
`).join('')}
</div>
</div>
`;
} else {
// Sign In / Register / Phone OTP Form
el.innerHTML = `
<div class="container" style="padding: 40px 0 80px 0; max-width: 520px;">
<div class="breadcrumbs">
<a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Account</span>
</div>
<div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 36px 32px; box-shadow: var(--shadow-sm);">
<div style="display: flex; border-bottom: 1px solid var(--color-border); margin-bottom: 24px;">
<button type="button" class="tab-btn ${accountAuthTab==='signin'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='signin'?'var(--color-primary)':'transparent'}; font-size: 0.85rem;" onclick="accountAuthTab='signin'; renderCurrentRoute();">Email</button>
<button type="button" class="tab-btn ${accountAuthTab==='phone'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='phone'?'var(--color-primary)':'transparent'}; font-size: 0.85rem;" onclick="accountAuthTab='phone'; renderCurrentRoute();">Phone OTP</button>
<button type="button" class="tab-btn ${accountAuthTab==='signup'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='signup'?'var(--color-primary)':'transparent'}; font-size: 0.85rem;" onclick="accountAuthTab='signup'; renderCurrentRoute();">Create Account</button>
</div>

${accountAuthTab === 'signin' ? `
<div style="margin-bottom: 14px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Email Address</label>
<input type="email" id="authEmail" class="form-input" placeholder="name@example.com" value="user@thestella.in">
</div>
<div style="margin-bottom: 20px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Password</label>
<input type="password" id="authPassword" class="form-input" value="password123">
</div>
<button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeUserSignIn()">Sign In with Email</button>
<p style="font-size: 0.78rem; color: var(--color-text-secondary); text-align: center; margin-top: 14px;">Test credentials prefilled for instant access.</p>
` : accountAuthTab === 'phone' ? `
<div id="phoneStep1">
<div style="margin-bottom: 14px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Mobile Number</label>
<div style="display: flex; gap: 8px;">
<span style="display: flex; align-items: center; padding: 0 12px; background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem; font-weight: 600;">+91</span>
<input type="tel" id="authPhone" class="form-input" style="flex: 1;" placeholder="98765 43210" value="9876543210">
</div>
</div>
<div id="recaptcha-container"></div>
<button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeSendOtp()">Send Verification Code</button>
</div>
<div id="phoneStep2" style="display: none;">
<div style="margin-bottom: 14px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Enter 6-Digit SMS OTP</label>
<input type="text" id="authOtpCode" class="form-input" placeholder="123456" maxlength="6" style="letter-spacing: 0.25em; text-align: center; font-size: 1.2rem; font-weight: 700;">
</div>
<button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeVerifyOtp()">Verify & Sign In</button>
<button type="button" class="btn-minimal btn-minimal-outline" style="width: 100%; margin-top: 10px; font-size: 0.8rem;" onclick="document.getElementById('phoneStep1').style.display='block'; document.getElementById('phoneStep2').style.display='none';">Re-enter Phone</button>
</div>
` : `
<div style="margin-bottom: 12px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Full Name</label>
<input type="text" id="regName" class="form-input" placeholder="Avina Vasoya">
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
<div>
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Email Address</label>
<input type="email" id="regEmail" class="form-input" placeholder="avina@example.com">
</div>
<div>
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Mobile Phone</label>
<input type="tel" id="regPhone" class="form-input" placeholder="+91 98765 43210">
</div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
<div>
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Gender</label>
<select id="regGender" class="form-input">
<option value="Female">Female</option>
<option value="Male">Male</option>
<option value="Non-binary / Other">Non-binary / Other</option>
<option value="Prefer not to say">Prefer not to say</option>
</select>
</div>
<div>
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Age Bracket</label>
<select id="regAge" class="form-input">
<option value="18-24 years">18 – 24 years</option>
<option value="25-34 years" selected>25 – 34 years</option>
<option value="35-44 years">35 – 44 years</option>
<option value="45-54 years">45 – 54 years</option>
<option value="55+ years">55+ years</option>
</select>
</div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
<div>
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Skin Type</label>
<select id="regSkinType" class="form-input">
<option value="Combination">Combination</option>
<option value="Dry / Dehydrated">Dry / Dehydrated</option>
<option value="Oily / Acne-Prone">Oily / Acne-Prone</option>
<option value="Sensitive">Sensitive</option>
<option value="Normal / Balanced">Normal / Balanced</option>
</select>
</div>
<div>
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Primary Concern</label>
<select id="regConcern" class="form-input">
<option value="Dark Spots & Pigmentation">Dark Spots & Pigmentation</option>
<option value="Dullness & Dehydration">Dullness & Dehydration</option>
<option value="Scalp Flakes & Dandruff">Scalp Flakes & Dandruff</option>
<option value="Body Texture & Blemishes">Body Texture & Blemishes</option>
<option value="Underarm Friction & Tone">Underarm Friction & Tone</option>
</select>
</div>
</div>

<div style="margin-bottom: 20px;">
<label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Password</label>
<input type="password" id="regPassword" class="form-input" placeholder="Create secure password">
</div>
<button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 13px;" onclick="executeUserSignUp()">Create Personalized Account</button>
`}

<div style="margin: 22px 0 16px 0; display: flex; align-items: center; text-align: center;">
<div style="flex: 1; border-bottom: 1px solid var(--color-border);"></div>
<span style="padding: 0 12px; font-size: 0.72rem; text-transform: uppercase; color: var(--color-text-secondary); letter-spacing: 0.05em;">Or Continue With</span>
<div style="flex: 1; border-bottom: 1px solid var(--color-border);"></div>
</div>

<button type="button" class="btn-minimal btn-minimal-outline" style="width: 100%; padding: 11px; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 600; font-size: 0.88rem;" onclick="executeGoogleSignIn()">
<svg width="18" height="18" viewBox="0 0 24 24">
<path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
<path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.34 24 12 24z"/>
<path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
<path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.34 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
</svg>
Sign In with Google
</button>

<div style="margin-top: 18px; padding: 10px 14px; background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.72rem; color: var(--color-text-secondary); text-align: center;">
Connected to Google Cloud Firestore (the-stella)
</div>
</div>
</div>
`;
}
}

async function executeGoogleSignIn() {
if (window.StellaFirebase && window.StellaFirebase.auth) {
try {
showToast("Opening Google Sign-In...");
const profile = await window.StellaFirebase.auth.signInWithGoogle();
setCurrentUser(profile);
showToast("Welcome back, " + profile.name);
renderCurrentRoute();
} catch (err) {
console.warn(err);
showToast(err.message || "Google Sign-In was cancelled or domain unauthorized.");
}
} else {
showToast("Connecting to Firebase...");
}
}

async function executeSendOtp() {
const phone = document.getElementById('authPhone')?.value.trim();
if (!phone || phone.length < 8) {
showToast("Please enter a valid mobile number.");
return;
}
const fullPhone = phone.startsWith('+') ? phone : '+91' + phone.replace(/^0+/, '');
if (window.StellaFirebase && window.StellaFirebase.auth) {
try {
showToast("Sending OTP to " + fullPhone + "...");
await window.StellaFirebase.auth.sendPhoneOtp(fullPhone, 'recaptcha-container');
showToast("Verification code sent via SMS!");
const s1 = document.getElementById('phoneStep1');
const s2 = document.getElementById('phoneStep2');
if (s1 && s2) {
s1.style.display = 'none';
s2.style.display = 'block';
}
} catch (err) {
console.error(err);
showToast(err.message || "Unable to send SMS. Ensure Phone Auth is enabled in Firebase Console.");
}
} else {
showToast("Connecting to Firebase Phone Auth...");
}
}

async function executeVerifyOtp() {
const code = document.getElementById('authOtpCode')?.value.trim();
if (!code || code.length < 6) {
showToast("Please enter the 6-digit verification code.");
return;
}
if (window.StellaFirebase && window.StellaFirebase.auth) {
try {
showToast("Verifying code...");
const profile = await window.StellaFirebase.auth.verifyPhoneOtp(code);
setCurrentUser(profile);
showToast("Phone verified! Welcome, " + profile.name);
renderCurrentRoute();
} catch (err) {
console.error(err);
showToast(err.message || "Invalid or expired OTP code.");
}
}
}

async function executeUserSignIn() {
const email = document.getElementById('authEmail')?.value.trim();
const pass = document.getElementById('authPassword')?.value.trim();
if (!email || !pass) {
showToast("Please enter email and password.");
return;
}
if (window.StellaFirebase && window.StellaFirebase.auth) {
try {
showToast("Authenticating...");
const profile = await window.StellaFirebase.auth.signInWithEmail(email, pass);
setCurrentUser(profile);
showToast("Signed in as " + profile.name);
renderCurrentRoute();
return;
} catch (err) {
console.warn("Firebase email sign-in fallback:", err.message);
}
}
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

async function executeUserSignUp() {
const name = document.getElementById('regName')?.value.trim();
const email = document.getElementById('regEmail')?.value.trim();
const phone = document.getElementById('regPhone')?.value.trim();
const gender = document.getElementById('regGender')?.value;
const ageGroup = document.getElementById('regAge')?.value;
const skinType = document.getElementById('regSkinType')?.value;
const concern = document.getElementById('regConcern')?.value;
const pass = document.getElementById('regPassword')?.value.trim();

if (!name || !email || !pass) {
showToast("Please enter your name, email, and password.");
return;
}

const userProfile = {
id: 'usr_' + Date.now(),
name: name,
email: email,
phone: phone || '+91 98765 43210',
gender: gender || 'Female',
ageGroup: ageGroup || '25-34 years',
skinType: skinType || 'Combination',
concern: concern || 'Dark Spots & Pigmentation',
password: pass,
joinedDate: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
};

if (window.StellaFirebase && window.StellaFirebase.auth) {
try {
showToast("Creating personalized account in Firebase...");
const fbProfile = await window.StellaFirebase.auth.signUpWithEmail(email, pass, name, phone);
userProfile.id = fbProfile.id;
if (window.firebase && window.firebase.firestore) {
window.firebase.firestore().collection('users').doc(fbProfile.id).set({
gender: gender,
ageGroup: ageGroup,
skinType: skinType,
concern: concern
}, { merge: true }).catch(() => {});
}
} catch (err) {
console.warn("Firebase sign up fallback:", err.message);
}
}

const users = getUsers();
users.push(userProfile);
localStorage.setItem('stella_users', JSON.stringify(users));
setCurrentUser(userProfile);
showToast("Welcome to The Stella, " + name + "!");
renderCurrentRoute();
}
'''

# Find start of section 6 and end of section 8 (before // 9. ADMIN VIEW)
start_marker = '// ==========================================\n// 6. ROUTINE FINDER QUIZ VIEW'
end_marker = '// ==========================================\n// 9. ADMIN VIEW'

pos_start = content.find(start_marker)
pos_end = content.find(end_marker)

if pos_start != -1 and pos_end != -1:
    new_content = content[:pos_start] + replacement + '\n' + content[pos_end:]
    with open('assets/js/app.js', 'w') as f:
        f.write(new_content)
    print("SUCCESS: app.js updated cleanly! Replaced chars:", pos_end - pos_start)
else:
    print("ERROR: Markers not found! pos_start:", pos_start, "pos_end:", pos_end)
