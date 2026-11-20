import re

def update_app():
    with open('assets/js/app.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Clear helper text in handlePincodeInput
    code = re.sub(
        r"text\.textContent\s*=\s*'Enter 6-digit PIN code to auto-detect City and State\.';",
        "text.textContent = '';",
        code
    )

    # Clear looking up text in fetchPincodeDetails
    code = re.sub(
        r'text\.textContent\s*=\s*`Looking up postal records for PIN \$\{pin\}\.\.\.`;',
        "text.textContent = '';",
        code
    )

    # Clear recognized text in applyPincodeData
    code = re.sub(
        r'text\.textContent\s*=\s*`Recognized: \$\{data\.city\}, \$\{data\.state\}\. Now enter Address Line 1 and 2 below\.`;',
        "text.textContent = '';",
        code
    )

    # 2. Add escapeHtml, Address State & Helper methods right after toggleManualCityStateEdit
    address_helpers = """
// ----------------------------------------------------
// MULTI-ADDRESS CHECKOUT SYSTEM (Amazon & Flipkart UX)
// ----------------------------------------------------
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

let selectedCheckoutAddressId = null;
let isAddingNewCheckoutAddress = false;
let editingCheckoutAddressId = null;
let selectedAddressType = 'Home';

function selectCheckoutSavedAddress(addrId) {
  selectedCheckoutAddressId = addrId;
  const cards = document.querySelectorAll('.saved-address-card');
  cards.forEach(card => {
    const radio = card.querySelector('input[type="radio"]');
    const isThis = card.getAttribute('data-addr-id') === addrId;
    if (radio) radio.checked = isThis;
    if (isThis) {
      card.classList.add('selected');
      card.style.borderColor = 'var(--color-primary)';
      card.style.background = '#FDF9FA';
      const ind = card.querySelector('.selected-indicator');
      if (ind) ind.style.display = 'inline-flex';
      const btn = card.querySelector('.deliver-btn-unselected');
      if (btn) btn.style.display = 'none';
    } else {
      card.classList.remove('selected');
      card.style.borderColor = 'var(--color-border)';
      card.style.background = '#FFFFFF';
      const ind = card.querySelector('.selected-indicator');
      if (ind) ind.style.display = 'none';
      const btn = card.querySelector('.deliver-btn-unselected');
      if (btn) btn.style.display = 'inline-block';
    }
  });
}

function openNewCheckoutAddressForm() {
  editingCheckoutAddressId = null;
  isAddingNewCheckoutAddress = true;
  selectedAddressType = 'Home';
  renderCurrentRoute();
}

function cancelCheckoutAddressForm() {
  editingCheckoutAddressId = null;
  isAddingNewCheckoutAddress = false;
  renderCurrentRoute();
}

function editCheckoutSavedAddress(addrId) {
  editingCheckoutAddressId = addrId;
  isAddingNewCheckoutAddress = true;
  const addrs = getSavedAddresses();
  const found = addrs.find(a => a.id === addrId);
  if (found) {
    selectedAddressType = found.type || 'Home';
  }
  renderCurrentRoute();
}

function deleteCheckoutSavedAddress(addrId) {
  if (confirm("Are you sure you want to remove this delivery address?")) {
    deleteUserAddress(addrId);
    selectedCheckoutAddressId = null;
    showToast("Address removed.");
    renderCurrentRoute();
  }
}

function selectAddressType(type) {
  selectedAddressType = type;
  const container = document.getElementById('addressTypeSelector');
  if (container) {
    container.querySelectorAll('.address-type-pill').forEach(btn => {
      const isMatch = btn.getAttribute('data-type') === type;
      if (isMatch) {
        btn.classList.add('active');
        btn.style.borderColor = 'var(--color-primary)';
        btn.style.background = '#FDF8F9';
        btn.style.color = 'var(--color-primary)';
        btn.style.fontWeight = '700';
      } else {
        btn.classList.remove('active');
        btn.style.borderColor = 'var(--color-border)';
        btn.style.background = '#FFFFFF';
        btn.style.color = 'var(--color-text-main)';
        btn.style.fontWeight = '500';
      }
    });
  }
}

function saveAndDeliverAddress() {
  const recipientName = document.getElementById('chkName')?.value.trim();
  const countryCode = document.getElementById('chkCountryCode')?.value.trim() || '+91';
  const rawPhone = document.getElementById('chkPhone')?.value.trim().replace(/\\D/g, '');
  const pin = document.getElementById('chkPin')?.value.trim().replace(/\\D/g, '');
  const line1 = document.getElementById('chkAddress1')?.value.trim();
  const line2 = document.getElementById('chkAddress2')?.value.trim();
  const city = document.getElementById('chkCity')?.value.trim();
  const state = document.getElementById('chkState')?.value.trim();

  if (!recipientName) {
    showToast("Please provide the full recipient name.");
    document.getElementById('chkName')?.focus();
    return;
  }
  if (!rawPhone || rawPhone.length !== 10) {
    showToast("Please provide a valid 10-digit mobile number.");
    document.getElementById('chkPhone')?.focus();
    return;
  }
  if (!pin || pin.length !== 6) {
    showToast("Please enter a valid 6-digit PIN code.");
    document.getElementById('chkPin')?.focus();
    return;
  }
  if (!city) {
    showToast("Please enter destination city (or click Edit manually).");
    document.getElementById('chkCity')?.focus();
    return;
  }
  if (!state) {
    showToast("Please enter destination state.");
    document.getElementById('chkState')?.focus();
    return;
  }
  if (!line1) {
    showToast("Please enter Address Line 1 (Flat, House no., Building).");
    document.getElementById('chkAddress1')?.focus();
    return;
  }

  const saved = saveUserAddress({
    id: editingCheckoutAddressId || undefined,
    name: recipientName,
    phone: rawPhone,
    countryCode: countryCode,
    pincode: pin,
    city: city,
    state: state,
    address1: line1,
    address2: line2,
    type: selectedAddressType || 'Home',
    isDefault: true
  });

  selectedCheckoutAddressId = saved.id;
  isAddingNewCheckoutAddress = false;
  editingCheckoutAddressId = null;
  showToast("Address saved successfully!");
  renderCurrentRoute();
}
"""

    anchor = "if (showToastMessage) showToast(\"City & State unlocked for manual editing.\");\n  }\n}"
    if anchor in code and "function selectCheckoutSavedAddress" not in code:
        code = code.replace(anchor, anchor + "\n" + address_helpers, 1)

    # 3. Replace renderCheckoutView
    # Let's locate from "function renderCheckoutView(el) {" to "function applyPromo() {"
    start_str = "function renderCheckoutView(el) {"
    end_str = "function applyPromo() {"
    
    start_idx = code.find(start_str)
    end_idx = code.find(end_str)

    if start_idx != -1 and end_idx != -1:
        new_render_checkout = """function renderCheckoutView(el) {
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
  const savedAddresses = getSavedAddresses();

  // If no address selected or active not in list, select default or first
  if (!selectedCheckoutAddressId || !savedAddresses.some(a => a.id === selectedCheckoutAddressId)) {
    const def = savedAddresses.find(a => a.isDefault) || savedAddresses[0];
    selectedCheckoutAddressId = def ? def.id : null;
  }

  // If no saved addresses exist, automatically show new address form
  if (savedAddresses.length === 0) {
    isAddingNewCheckoutAddress = true;
  }

  // Determine form values if adding or editing
  let formName = '';
  let formCountryCode = '+91';
  let formPhone = '';
  let formPin = '';
  let formCity = '';
  let formState = '';
  let formAddress1 = '';
  let formAddress2 = '';
  let formType = selectedAddressType || 'Home';

  if (editingCheckoutAddressId) {
    const editAddr = savedAddresses.find(a => a.id === editingCheckoutAddressId);
    if (editAddr) {
      formName = editAddr.name || '';
      formCountryCode = editAddr.countryCode || '+91';
      formPhone = editAddr.phone || '';
      formPin = editAddr.pincode || '';
      formCity = editAddr.city || '';
      formState = editAddr.state || '';
      formAddress1 = editAddr.address1 || '';
      formAddress2 = editAddr.address2 || '';
      formType = editAddr.type || 'Home';
      selectedAddressType = formType;
    }
  } else {
    // New address: auto-detect name and phone from logged in account (editable!)
    formName = currentUser ? (currentUser.name || '') : '';
    if (currentUser && currentUser.phone) {
      const p = currentUser.phone.trim();
      if (p.startsWith('+91')) {
        formCountryCode = '+91';
        formPhone = p.replace('+91', '').trim().replace(/\\D/g, '').slice(-10);
      } else if (p.startsWith('+1')) {
        formCountryCode = '+1';
        formPhone = p.replace('+1', '').trim();
      } else if (p.startsWith('+44')) {
        formCountryCode = '+44';
        formPhone = p.replace('+44', '').trim();
      } else if (p.startsWith('+971')) {
        formCountryCode = '+971';
        formPhone = p.replace('+971', '').trim();
      } else {
        formPhone = p.replace(/\\D/g, '').slice(-10);
      }
    }
  }

  let shipping = subtotal >= 499 || subtotal === 0 ? 0 : 70;
  let discountAmount = 0;
  let grandTotal = subtotal + shipping;

  if (appliedPromoCode === 'ONERUPEE') {
    shipping = 0;
    discountAmount = Math.max(0, subtotal - 1);
    grandTotal = 1;
  } else if (checkoutDiscount > 0) {
    discountAmount = Math.round(subtotal * checkoutDiscount);
    grandTotal = Math.max(0, subtotal - discountAmount + shipping);
  }

  el.innerHTML = `
    <div class="container" style="padding: 40px 0 80px 0;">
      <div class="breadcrumbs">
        <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Shopping Bag & Checkout</span>
      </div>
      <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 24px;">Your Shopping Bag</h1>
      <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 32px;" id="checkoutGridContainer">
        <div>
          <!-- Bag Items List -->
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
                  <div style="font-size: 0.9rem; font-weight: 700; color: var(--color-primary); margin-top: 4px;">₹${it.prod.price} &times; ${it.quantity} = ₹${it.total}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <button class="btn-icon" style="width: 28px; height: 28px; padding: 0;" onclick="updateBagQuantity('${it.id}', ${it.quantity - 1})">-</button>
                  <span style="font-size: 0.9rem; font-weight: 600; min-width: 20px; text-align: center;">${it.quantity}</span>
                  <button class="btn-icon" style="width: 28px; height: 28px; padding: 0;" onclick="updateBagQuantity('${it.id}', ${it.quantity + 1})">+</button>
                  <button class="btn-icon" style="width: 28px; height: 28px; padding: 0; margin-left: 8px; color: #DC2626;" onclick="removeFromBag('${it.id}')" title="Remove Item">&times;</button>
                </div>
              </div>
            `).join('')}
          </div>

          <!-- 1. Delivery Destination Card / Saved Addresses (Flipkart & Amazon UX) -->
          <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 28px; margin-top: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <span style="display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; background: var(--color-primary); color: #FFFFFF; border-radius: 50%; font-size: 0.82rem; font-weight: 700;">1</span>
                <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin: 0;">Delivery Destination</h3>
              </div>
              <span style="font-size: 0.72rem; color: #059669; font-weight: 700; background: #ECFDF5; padding: 4px 10px; border-radius: var(--radius-pill); text-transform: uppercase; letter-spacing: 0.04em;">Pan-India Dispatch</span>
            </div>

            ${savedAddresses.length > 0 && !isAddingNewCheckoutAddress ? `
              <!-- SAVED ADDRESSES LIST -->
              <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                  <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-text-secondary);">
                    Saved Addresses (${savedAddresses.length})
                  </span>
                  <span style="font-size: 0.78rem; color: var(--color-primary); font-weight: 600;">Click to select</span>
                </div>

                <div id="savedAddressesContainer">
                  ${savedAddresses.map((addr, idx) => {
                    const isSelected = addr.id === selectedCheckoutAddressId;
                    const typeClass = (addr.type || 'home').toLowerCase();
                    const typeLabel = addr.type === 'Work' ? '🏢 WORK' : (addr.type === 'Other' ? '📍 OTHER' : '🏠 HOME');
                    return `
                      <div class="saved-address-card ${isSelected ? 'selected' : ''}" data-addr-id="${addr.id}" onclick="selectCheckoutSavedAddress('${addr.id}')" style="border: ${isSelected ? '2px solid var(--color-primary)' : '1px solid var(--color-border)'}; background: ${isSelected ? '#FDF9FA' : '#FFFFFF'}; border-radius: var(--radius-md); padding: 16px 18px; margin-bottom: 12px; cursor: pointer; transition: all 0.2s ease;">
                        <div style="display: flex; align-items: flex-start; gap: 14px;">
                          <input type="radio" name="checkoutAddressRadio" value="${addr.id}" ${isSelected ? 'checked' : ''} style="margin-top: 4px; accent-color: var(--color-primary); width: 18px; height: 18px; cursor: pointer;">
                          <div style="flex: 1;">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px; flex-wrap: wrap;">
                              <strong style="font-size: 0.98rem; color: var(--color-text-main);">${escapeHtml(addr.name)}</strong>
                              <span class="address-type-tag ${typeClass}">
                                ${typeLabel}
                              </span>
                              <span style="font-size: 0.88rem; font-weight: 600; color: var(--color-text-main); margin-left: auto;">${escapeHtml(addr.countryCode || '+91')} ${escapeHtml(addr.phone)}</span>
                            </div>
                            <p style="font-size: 0.88rem; color: var(--color-text-secondary); line-height: 1.5; margin-bottom: 10px;">
                              ${escapeHtml(addr.address1)}${addr.address2 ? ', ' + escapeHtml(addr.address2) : ''}, ${escapeHtml(addr.city)}, ${escapeHtml(addr.state)} — <strong style="color: var(--color-text-main);">${escapeHtml(addr.pincode)}</strong>
                            </p>
                            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed var(--color-border); padding-top: 10px; margin-top: 6px;">
                              <div style="display: flex; gap: 16px; align-items: center;">
                                <button type="button" onclick="event.stopPropagation(); editCheckoutSavedAddress('${addr.id}');" style="background: none; border: none; font-size: 0.8rem; color: var(--color-primary); font-weight: 600; text-decoration: underline; cursor: pointer; padding: 0;">Edit Address</button>
                                ${savedAddresses.length > 1 ? `
                                  <button type="button" onclick="event.stopPropagation(); deleteCheckoutSavedAddress('${addr.id}');" style="background: none; border: none; font-size: 0.8rem; color: #DC2626; text-decoration: underline; cursor: pointer; padding: 0;">Delete</button>
                                ` : ''}
                              </div>
                              <div>
                                <span class="selected-indicator" style="display: ${isSelected ? 'inline-flex' : 'none'}; font-size: 0.82rem; font-weight: 700; color: var(--color-primary); align-items: center; gap: 4px;">
                                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                  Delivering Here
                                </span>
                                <button type="button" class="deliver-btn-unselected btn-minimal btn-minimal-primary" onclick="event.stopPropagation(); selectCheckoutSavedAddress('${addr.id}');" style="display: ${isSelected ? 'none' : 'inline-block'}; padding: 6px 16px; font-size: 0.8rem;">
                                  Deliver Here
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>

                <button type="button" onclick="openNewCheckoutAddressForm()" style="width: 100%; box-sizing: border-box; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 14px; border: 1.5px dashed var(--color-primary); border-radius: var(--radius-md); background: #FAF9F8; color: var(--color-primary); font-size: 0.9rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; margin-top: 14px;">
                  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  + Add a New Delivery Address (Home, Work, etc.)
                </button>
              </div>
            ` : `
              <!-- ADDRESS ENTRY / EDIT FORM -->
              <div id="checkoutAddressForm">
                ${savedAddresses.length > 0 ? `
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid var(--color-border);">
                    <strong style="font-size: 0.95rem; color: var(--color-text-main);">
                      ${editingCheckoutAddressId ? 'Edit Delivery Address' : 'Add a New Delivery Address'}
                    </strong>
                    <button type="button" onclick="cancelCheckoutAddressForm()" style="background: none; border: none; font-size: 0.82rem; color: var(--color-primary); font-weight: 600; text-decoration: underline; cursor: pointer;">
                      Cancel & Return to Saved Addresses
                    </button>
                  </div>
                ` : ''}

                <!-- Recipient Name (Auto-detected from account, editable) -->
                <div style="margin-bottom: 16px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <label style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-text-main);">Full Recipient Name *</label>
                    ${currentUser && currentUser.name ? `<span style="font-size: 0.72rem; color: var(--color-primary); font-weight: 600;">Auto-detected from account (editable)</span>` : ''}
                  </div>
                  <input type="text" id="chkName" placeholder="Enter recipient full name" class="form-input" value="${escapeHtml(formName)}" style="width: 100%; box-sizing: border-box; height: 46px;">
                </div>

                <!-- Mobile Contact (Auto-detected from account, editable) -->
                <div style="margin-bottom: 18px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <label style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-text-main);">Mobile Contact for Delivery Updates *</label>
                    ${currentUser && currentUser.phone ? `<span style="font-size: 0.72rem; color: var(--color-primary); font-weight: 600;">Auto-detected from account (editable)</span>` : ''}
                  </div>
                  <div style="display: grid; grid-template-columns: 130px 1fr; gap: 10px;">
                    <select id="chkCountryCode" class="form-input" style="height: 46px; padding: 10px 8px; font-size: 0.88rem; background: #FFFFFF; width: 100%; box-sizing: border-box;">
                      <option value="+91" ${formCountryCode === '+91' ? 'selected' : ''}>+91 (India)</option>
                      <option value="+1" ${formCountryCode === '+1' ? 'selected' : ''}>+1 (US/CA)</option>
                      <option value="+44" ${formCountryCode === '+44' ? 'selected' : ''}>+44 (UK)</option>
                      <option value="+971" ${formCountryCode === '+971' ? 'selected' : ''}>+971 (UAE)</option>
                      <option value="+65" ${formCountryCode === '+65' ? 'selected' : ''}>+65 (SG)</option>
                      <option value="+61" ${formCountryCode === '+61' ? 'selected' : ''}>+61 (AU)</option>
                    </select>
                    <input type="tel" id="chkPhone" placeholder="10-digit mobile number" class="form-input" maxlength="10" inputmode="numeric" value="${escapeHtml(formPhone)}" style="width: 100%; box-sizing: border-box; height: 46px;">
                  </div>
                </div>

                <!-- PIN Code with Instant Auto-Lookup (No clutter text) -->
                <div style="margin-bottom: 16px; background: #FAF9F8; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <label style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin: 0; color: var(--color-text-main);">PIN Code (Postal Code) *</label>
                    <span id="pincodeStatusBadge" style="font-size: 0.72rem; display: none;"></span>
                  </div>
                  <div style="position: relative;">
                    <input type="text" id="chkPin" placeholder="Enter 6-digit PIN code (e.g. 400050 or 380015)" class="form-input" maxlength="6" inputmode="numeric" value="${escapeHtml(formPin)}" oninput="handlePincodeInput(this.value)" style="width: 100%; box-sizing: border-box; height: 46px; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.06em; background: #FFFFFF;">
                    <div id="pincodeSpinner" style="position: absolute; right: 14px; top: 50%; transform: translateY(-50%); display: none;">
                      <svg class="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5">
                        <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                        <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"></path>
                      </svg>
                    </div>
                  </div>
                  <div id="pincodeStatusText" style="font-size: 0.76rem; margin-top: 4px; line-height: 1.4;"></div>

                  <!-- Available Localities container -->
                  <div id="pincodeLocalityContainer" style="display: none; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--color-border);">
                    <div style="font-size: 0.72rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; margin-bottom: 6px;">Select Locality / Post Office:</div>
                    <div id="pincodeLocalityPills" style="display: flex; flex-wrap: wrap; gap: 6px;"></div>
                  </div>
                </div>

                <!-- Auto-Populated City & State in 2-Column Grid -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                  <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                      <label style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin: 0; color: var(--color-text-main);">City / District *</label>
                      <button type="button" id="btnEditCityState" onclick="toggleManualCityStateEdit()" style="background: none; border: none; font-size: 0.72rem; color: var(--color-primary); cursor: pointer; text-decoration: underline; padding: 0;">Edit manually</button>
                    </div>
                    <input type="text" id="chkCity" placeholder="Auto-detected from PIN" class="form-input" value="${escapeHtml(formCity)}" style="width: 100%; box-sizing: border-box; height: 46px; background: #F9F9F8;" readonly>
                  </div>
                  <div>
                    <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; color: var(--color-text-main);">State *</label>
                    <input type="text" id="chkState" placeholder="Auto-detected from PIN" class="form-input" value="${escapeHtml(formState)}" style="width: 100%; box-sizing: border-box; height: 46px; background: #F9F9F8;" readonly>
                  </div>
                </div>

                <!-- Address Line 1 -->
                <div style="margin-bottom: 16px;">
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; color: var(--color-text-main);">Address Line 1 (Flat, House No., Building Name) *</label>
                  <input type="text" id="chkAddress1" placeholder="e.g. Flat 402, Building A, Crystal Heights" class="form-input" value="${escapeHtml(formAddress1)}" style="width: 100%; box-sizing: border-box; height: 46px;">
                </div>

                <!-- Address Line 2 -->
                <div style="margin-bottom: 18px;">
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; color: var(--color-text-main);">Address Line 2 (Street, Area, Landmark) <span style="font-weight: 400; text-transform: none; color: var(--color-text-secondary);">(Optional)</span></label>
                  <input type="text" id="chkAddress2" placeholder="e.g. Diamond Avenue, Near Grand Mall" class="form-input" value="${escapeHtml(formAddress2)}" style="width: 100%; box-sizing: border-box; height: 46px;">
                </div>

                <!-- Address Type Selector (Save As: Home, Work, Other) -->
                <div style="margin-bottom: 20px;">
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px; color: var(--color-text-main);">Address Type (Save As)</label>
                  <div style="display: flex; gap: 10px; flex-wrap: wrap;" id="addressTypeSelector">
                    <button type="button" class="address-type-pill ${formType === 'Home' ? 'active' : ''}" data-type="Home" onclick="selectAddressType('Home')">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                      Home
                    </button>
                    <button type="button" class="address-type-pill ${formType === 'Work' ? 'active' : ''}" data-type="Work" onclick="selectAddressType('Work')">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                      Work / Office
                    </button>
                    <button type="button" class="address-type-pill ${formType === 'Other' ? 'active' : ''}" data-type="Other" onclick="selectAddressType('Other')">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                      Other
                    </button>
                  </div>
                </div>

                <!-- Action Button -->
                <button type="button" onclick="saveAndDeliverAddress()" class="btn-minimal btn-minimal-primary" style="width: 100%; box-sizing: border-box; padding: 13px; font-size: 0.9rem; font-weight: 700;">
                  ${editingCheckoutAddressId ? 'Save Changes & Deliver Here' : 'Save & Deliver to this Address'}
                </button>
              </div>
            `}
          </div>

          <!-- 2. Payment Method Visual Cards -->
          <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 28px; margin-top: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <span style="display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; background: var(--color-primary); color: #FFFFFF; border-radius: 50%; font-size: 0.82rem; font-weight: 700;">2</span>
                <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin: 0;">Payment Method</h3>
              </div>
              <span style="font-size: 0.75rem; color: #059669; font-weight: 700; background: #ECFDF5; padding: 3px 8px; border-radius: var(--radius-pill);">RBI & PCI-DSS Compliant</span>
            </div>

            <!-- Razorpay Card -->
            <div id="payCard_razorpay" onclick="selectPaymentMethod('razorpay', ${grandTotal})" style="border: 2px solid var(--color-primary); background: #FDF8F9; border-radius: var(--radius-md); padding: 18px; margin-bottom: 14px; cursor: pointer; transition: all 0.2s ease;">
              <div style="display: flex; align-items: flex-start; gap: 14px;">
                <input type="radio" id="payRadio_razorpay" name="stellaPaymentSelector" value="razorpay" checked style="margin-top: 4px; accent-color: var(--color-primary); width: 17px; height: 17px;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <strong style="font-size: 0.98rem; color: var(--color-text-main);">Razorpay Secure Checkout</strong>
                    <span style="background: #FCEEF2; color: var(--color-primary); font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Recommended</span>
                  </div>
                  <p style="font-size: 0.82rem; color: var(--color-text-secondary); margin-bottom: 8px; line-height: 1.5;">
                    Instant checkout via UPI (Google Pay, PhonePe, Paytm, BHIM, Cred), Credit/Debit Cards (RuPay, Visa, Mastercard), NetBanking (50+ Banks) & Wallets.
                  </p>
                  <div style="display: flex; flex-wrap: wrap; gap: 6px; font-size: 0.72rem; color: var(--color-text-secondary);">
                    <span style="background: #FFFFFF; border: 1px solid var(--color-border); padding: 2px 7px; border-radius: 3px;">Instant UPI</span>
                    <span style="background: #FFFFFF; border: 1px solid var(--color-border); padding: 2px 7px; border-radius: 3px;">Google Pay</span>
                    <span style="background: #FFFFFF; border: 1px solid var(--color-border); padding: 2px 7px; border-radius: 3px;">PhonePe</span>
                    <span style="background: #FFFFFF; border: 1px solid var(--color-border); padding: 2px 7px; border-radius: 3px;">All Debit & Credit Cards</span>
                    <span style="background: #FFFFFF; border: 1px solid var(--color-border); padding: 2px 7px; border-radius: 3px;">50+ NetBanking</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cash on Delivery Card -->
            <div id="payCard_cod" onclick="selectPaymentMethod('cod', ${grandTotal})" style="border: 1px solid var(--color-border); background: #FFFFFF; border-radius: var(--radius-md); padding: 18px; margin-bottom: 14px; cursor: pointer; transition: all 0.2s ease;">
              <div style="display: flex; align-items: flex-start; gap: 14px;">
                <input type="radio" id="payRadio_cod" name="stellaPaymentSelector" value="cod" style="margin-top: 4px; accent-color: var(--color-primary); width: 17px; height: 17px;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <strong style="font-size: 0.98rem; color: var(--color-text-main);">Cash on Delivery (COD)</strong>
                    <span style="font-size: 0.75rem; color: var(--color-text-secondary);">Pan-India</span>
                  </div>
                  <p style="font-size: 0.82rem; color: var(--color-text-secondary); line-height: 1.5;">
                    Pay in cash or scan delivery partner's UPI QR at your doorstep upon arrival.
                  </p>
                </div>
              </div>
            </div>

            <!-- Direct UPI QR Card -->
            <div id="payCard_direct_upi" onclick="selectPaymentMethod('direct_upi', ${grandTotal})" style="border: 1px solid var(--color-border); background: #FFFFFF; border-radius: var(--radius-md); padding: 18px; cursor: pointer; transition: all 0.2s ease;">
              <div style="display: flex; align-items: flex-start; gap: 14px;">
                <input type="radio" id="payRadio_direct_upi" name="stellaPaymentSelector" value="direct_upi" style="margin-top: 4px; accent-color: var(--color-primary); width: 17px; height: 17px;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <strong style="font-size: 0.98rem; color: var(--color-text-main);">Direct UPI QR Dispatch</strong>
                    <span style="font-size: 0.75rem; color: var(--color-text-secondary);">Zero Fees</span>
                  </div>
                  <p style="font-size: 0.82rem; color: var(--color-text-secondary); line-height: 1.5;">
                    Instantly generate dynamic order QR code and transfer directly to merchant account.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Summary -->
        <div>
          <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; position: sticky; top: 100px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 16px; border-bottom: 1px solid var(--color-border); padding-bottom: 12px;">Order Summary</h3>
            
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.9rem;">
              <span style="color: var(--color-text-secondary);">Subtotal (${items.reduce((acc, it) => acc + it.quantity, 0)} items)</span>
              <strong>₹${subtotal}</strong>
            </div>

            ${discountAmount > 0 ? `
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.9rem; color: #059669;">
                <span>Discount (${appliedPromoCode})</span>
                <strong>-₹${discountAmount}</strong>
              </div>
            ` : ''}

            <div style="display: flex; justify-content: space-between; margin-bottom: 16px; font-size: 0.9rem;">
              <span style="color: var(--color-text-secondary);">Pan-India Shipping</span>
              <span>${shipping === 0 ? '<strong style="color: #059669;">FREE</strong>' : `₹${shipping}`}</span>
            </div>

            <!-- Promo Code Box -->
            <div style="margin-bottom: 20px; border-top: 1px dashed var(--color-border); padding-top: 14px;">
              <div style="display: flex; gap: 8px;">
                <input type="text" id="promoCodeInput" placeholder="Enter promo code" class="form-input" style="flex: 1; padding: 8px 12px; font-size: 0.85rem; text-transform: uppercase;" value="${appliedPromoCode}">
                <button class="btn-minimal btn-minimal-outline" style="padding: 8px 14px; font-size: 0.85rem;" onclick="applyPromo()">Apply</button>
              </div>
              <div style="font-size: 0.72rem; color: var(--color-text-secondary); margin-top: 6px;">
                Try <strong>STELLA20</strong> for 20% off.
              </div>
            </div>

            <div style="display: flex; justify-content: space-between; font-size: 1.15rem; font-weight: 700; border-top: 1px solid var(--color-border); padding-top: 16px; margin-bottom: 24px;">
              <span>Total Payable</span>
              <span style="color: var(--color-primary);" id="checkoutGrandTotalDisplay">₹${grandTotal}</span>
            </div>

            <button id="btnSubmitOrder" class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-size: 1rem; text-align: center;" onclick="executeCheckoutPayment(${grandTotal})">
              Proceed to Pay ₹${grandTotal} via Razorpay
            </button>

            <div style="font-size: 0.74rem; color: var(--color-text-secondary); text-align: center; margin-top: 14px; line-height: 1.4;">
              By completing order, you accept The Stella's Pan-India Dispatch & Quality Standard Terms.
            </div>
          </div>
        </div>
      </div>
      <div id="confirmedOrderArea" style="display: none; margin-top: 30px;"></div>
    </div>
  `;

  // Auto-trigger PIN lookup if formPin exists and is 6 digits
  if (isAddingNewCheckoutAddress && formPin && formPin.length === 6) {
    setTimeout(() => {
      fetchPincodeDetails(formPin);
    }, 50);
  }
}

"""
        code = code[:start_idx] + new_render_checkout + code[end_idx:]

    # 4. Update executeCheckoutPayment destination resolution
    old_validation_block = """  // Validate fields
  const recipientName = document.getElementById('chkName')?.value.trim();
  const countryCode = document.getElementById('chkCountryCode')?.value.trim() || '+91';
  const rawPhone = document.getElementById('chkPhone')?.value.trim().replace(/\\D/g, '');
  const pin = document.getElementById('chkPin')?.value.trim().replace(/\\D/g, '');
  const line1 = document.getElementById('chkAddress1')?.value.trim();
  const line2 = document.getElementById('chkAddress2')?.value.trim();
  const city = document.getElementById('chkCity')?.value.trim();
  const state = document.getElementById('chkState')?.value.trim();

  if (!recipientName) {
    showToast("Please provide the full recipient name.");
    document.getElementById('chkName')?.focus();
    return;
  }
  if (!rawPhone || rawPhone.length !== 10) {
    showToast("Please provide a valid 10-digit mobile number.");
    document.getElementById('chkPhone')?.focus();
    return;
  }
  if (!pin || pin.length !== 6) {
    showToast("Please enter a valid 6-digit PIN code.");
    document.getElementById('chkPin')?.focus();
    return;
  }
  if (!city) {
    showToast("Please provide destination city (click 'Edit manually' if needed).");
    document.getElementById('chkCity')?.focus();
    return;
  }
  if (!state) {
    showToast("Please provide destination state.");
    document.getElementById('chkState')?.focus();
    return;
  }
  if (!line1) {
    showToast("Please enter Address Line 1 (Flat, House no., Building).");
    document.getElementById('chkAddress1')?.focus();
    return;
  }

  const fullPhone = `${countryCode} ${rawPhone}`;
  const streetParts = [line1, line2].filter(Boolean).join(', ');
  const fullAddress = [streetParts, city, state, pin].filter(Boolean).join(', ');"""

    new_validation_block = """  // Resolve delivery destination (Saved Address or Form)
  let recipientName = '';
  let fullPhone = '';
  let fullAddress = '';
  let pin = '';

  const savedAddresses = getSavedAddresses();
  const activeSaved = (!isAddingNewCheckoutAddress && savedAddresses.length > 0)
    ? (savedAddresses.find(a => a.id === selectedCheckoutAddressId) || savedAddresses[0])
    : null;

  if (activeSaved) {
    recipientName = activeSaved.name;
    fullPhone = `${activeSaved.countryCode || '+91'} ${activeSaved.phone}`;
    const streetParts = [activeSaved.address1, activeSaved.address2].filter(Boolean).join(', ');
    fullAddress = [streetParts, activeSaved.city, activeSaved.state, activeSaved.pincode].filter(Boolean).join(', ');
    pin = activeSaved.pincode;
  } else {
    recipientName = document.getElementById('chkName')?.value.trim();
    const countryCode = document.getElementById('chkCountryCode')?.value.trim() || '+91';
    const rawPhone = document.getElementById('chkPhone')?.value.trim().replace(/\\D/g, '');
    pin = document.getElementById('chkPin')?.value.trim().replace(/\\D/g, '');
    const line1 = document.getElementById('chkAddress1')?.value.trim();
    const line2 = document.getElementById('chkAddress2')?.value.trim();
    const city = document.getElementById('chkCity')?.value.trim();
    const state = document.getElementById('chkState')?.value.trim();

    if (!recipientName) {
      showToast("Please provide the full recipient name.");
      document.getElementById('chkName')?.focus();
      return;
    }
    if (!rawPhone || rawPhone.length !== 10) {
      showToast("Please provide a valid 10-digit mobile number.");
      document.getElementById('chkPhone')?.focus();
      return;
    }
    if (!pin || pin.length !== 6) {
      showToast("Please enter a valid 6-digit PIN code.");
      document.getElementById('chkPin')?.focus();
      return;
    }
    if (!city) {
      showToast("Please enter destination city (or click Edit manually).");
      document.getElementById('chkCity')?.focus();
      return;
    }
    if (!state) {
      showToast("Please enter destination state.");
      document.getElementById('chkState')?.focus();
      return;
    }
    if (!line1) {
      showToast("Please enter Address Line 1 (Flat, House no., Building).");
      document.getElementById('chkAddress1')?.focus();
      return;
    }

    fullPhone = `${countryCode} ${rawPhone}`;
    const streetParts = [line1, line2].filter(Boolean).join(', ');
    fullAddress = [streetParts, city, state, pin].filter(Boolean).join(', ');

    // Automatically persist this address for the customer
    saveUserAddress({
      name: recipientName,
      phone: rawPhone,
      countryCode: countryCode,
      pincode: pin,
      city: city,
      state: state,
      address1: line1,
      address2: line2,
      type: selectedAddressType || 'Home',
      isDefault: savedAddresses.length === 0
    });
  }"""

    if old_validation_block in code:
        code = code.replace(old_validation_block, new_validation_block, 1)

    with open('assets/js/app.js', 'w', encoding='utf-8') as f:
        f.write(code)

    print("SUCCESS: app.js updated successfully with Flipkart/Amazon multi-address system!")

if __name__ == '__main__':
    update_app()
