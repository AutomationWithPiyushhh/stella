import re

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Marker for Section 8 start and Section 9 start
start_marker_s8 = '// ==========================================\n// 8. ACCOUNT VIEW (CUSTOMER PORTAL)'
end_marker_s8 = '// ==========================================\n// 9. ADMIN VIEW'

# Marker for Section 10 start and End of file
start_marker_s10 = '// ==========================================\n// 10. CONTACT & TRACKING VIEW'

s8_pos = content.find(start_marker_s8)
s9_pos = content.find(end_marker_s8)
s10_pos = content.find(start_marker_s10)

print(f"s8_pos: {s8_pos}, s9_pos: {s9_pos}, s10_pos: {s10_pos}")
if s8_pos == -1 or s9_pos == -1 or s10_pos == -1:
    print("Error: Could not locate section markers!")
    exit(1)

new_section_8 = '''// ==========================================
// 8. ACCOUNT VIEW (CUSTOMER PORTAL)
// ==========================================
let accountAuthTab = 'signin';
let isEditingSkinProfile = false;

function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = 'Hide';
  } else {
    input.type = 'password';
    btn.textContent = 'Show';
  }
}

function showDomainAuthModal() {
  const existing = document.getElementById('stellaAuthModal');
  if (existing) existing.remove();

  const modal = document.createElement('div');
  modal.id = 'stellaAuthModal';
  modal.style.cssText = 'position: fixed; inset: 0; background: rgba(18, 14, 16, 0.6); backdrop-filter: blur(4px); z-index: 10000; display: flex; align-items: center; justify-content: center; padding: 20px;';
  modal.innerHTML = `
    <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); max-width: 520px; width: 100%; padding: 32px; box-shadow: var(--shadow-lg); text-align: left;">
      <span class="text-eyebrow" style="color: var(--color-primary);">Firebase Security Notice</span>
      <h3 style="font-family: var(--font-serif); font-size: 1.35rem; margin: 6px 0 12px 0;">Authorize Domain in Firebase Console</h3>
      <p style="font-size: 0.88rem; color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 16px;">
        Google Sign-In requires your hosting domain to be added to your Firebase project allowlist:
      </p>
      <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 14px; font-size: 0.82rem; margin-bottom: 18px; line-height: 1.6;">
        <strong>Steps to authorize:</strong><br>
        1. Open Firebase Console &bull; Project: <strong>the-stella</strong><br>
        2. Go to <strong>Authentication</strong> &rarr; <strong>Settings</strong> tab &rarr; <strong>Authorized domains</strong><br>
        3. Click <strong>Add domain</strong> and enter: <code>thestella-skincare.vercel.app</code>
      </div>
      <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <button class="btn-minimal btn-minimal-primary" style="flex: 1; padding: 11px;" onclick="continueDemoGoogleAuth()">Continue with Demo Account</button>
        <button class="btn-minimal btn-minimal-outline" style="padding: 11px 18px;" onclick="document.getElementById('stellaAuthModal').remove()">Close</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
}

function continueDemoGoogleAuth() {
  const modal = document.getElementById('stellaAuthModal');
  if (modal) modal.remove();
  const demoProfile = {
    id: 'usr_g_' + Date.now(),
    name: 'Piyush Baldaniya',
    email: 'piyush.google@thestella.in',
    phone: '+91 98765 43210',
    gender: 'Male',
    ageGroup: '25-34 years',
    skinType: 'Combination',
    concern: 'Dark Spots & Pigmentation',
    joinedDate: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
  };
  const users = getUsers();
  users.push(demoProfile);
  localStorage.setItem('stella_users', JSON.stringify(users));
  setCurrentUser(demoProfile);
  showToast("Signed in as " + demoProfile.name + ". Redirecting to home...");
  setTimeout(() => {
    window.location.href = 'index.html';
  }, 400);
}

function showSmsRegionModal(phoneNum) {
  const existing = document.getElementById('stellaSmsModal');
  if (existing) existing.remove();

  const modal = document.createElement('div');
  modal.id = 'stellaSmsModal';
  modal.style.cssText = 'position: fixed; inset: 0; background: rgba(18, 14, 16, 0.6); backdrop-filter: blur(4px); z-index: 10000; display: flex; align-items: center; justify-content: center; padding: 20px;';
  modal.innerHTML = `
    <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); max-width: 520px; width: 100%; padding: 32px; box-shadow: var(--shadow-lg); text-align: left;">
      <span class="text-eyebrow" style="color: var(--color-primary);">Firebase Phone Auth Notice</span>
      <h3 style="font-family: var(--font-serif); font-size: 1.35rem; margin: 6px 0 12px 0;">Enable India SMS Region in Firebase</h3>
      <p style="font-size: 0.88rem; color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 14px;">
        Firebase requires Phone Authentication and the India (+91) SMS region policy to be enabled in your console:
      </p>
      <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 14px; font-size: 0.82rem; margin-bottom: 18px; line-height: 1.6;">
        1. <strong>Authentication</strong> &rarr; <strong>Sign-in method</strong> &rarr; Enable <strong>Phone</strong><br>
        2. <strong>Settings</strong> &rarr; <strong>SMS region policy</strong> &rarr; Allow <strong>India (+91)</strong><br>
        3. Or add test phone numbers in Phone settings (e.g. <code>${phoneNum}</code> with code <code>123456</code>)
      </div>
      <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <button class="btn-minimal btn-minimal-primary" style="flex: 1; padding: 11px;" onclick="activateDemoOtp('${phoneNum}')">Use Instant Test OTP (123456)</button>
        <button class="btn-minimal btn-minimal-outline" style="padding: 11px 18px;" onclick="document.getElementById('stellaSmsModal').remove()">Close</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
}

function activateDemoOtp(phoneNum) {
  const modal = document.getElementById('stellaSmsModal');
  if (modal) modal.remove();
  window._pendingTestOtp = '123456';
  window._pendingOtpPhone = phoneNum;
  const s1 = document.getElementById('phoneStep1');
  const s2 = document.getElementById('phoneStep2');
  if (s1 && s2) {
    s1.style.display = 'none';
    s2.style.display = 'block';
  }
  const otpInput = document.getElementById('authOtpCode');
  if (otpInput) {
    otpInput.value = '123456';
  }
  showToast("Test OTP code 123456 applied. Click Verify to sign in.");
}

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
      const userPhone = (currentUser.phone || '').replace(/\\D/g, '');
      const ordPhone = (ord.phone || '').replace(/\\D/g, '');
      const isEmailMatch = Boolean(userEmail && ordEmail && userEmail === ordEmail);
      const isPhoneMatch = Boolean(userPhone && ordPhone && userPhone.length >= 10 && userPhone.slice(-10) === ordPhone.slice(-10));
      const isUserIdMatch = Boolean(ord.userId && (ord.userId === currentUser.id || ord.userId === currentUser.uid));
      return isEmailMatch || isPhoneMatch || isUserIdMatch;
    });

    // Personalized product curation based on gender, age, skinType, and primary concern
    const catalog = getCatalog();
    let curatedProducts = [];
    const focusConcern = (currentUser.concern || '').toLowerCase();

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

    const hasSkinProfile = Boolean(currentUser.skinType && currentUser.concern);

    el.innerHTML = `
      <div class="container" style="padding: 40px 0 80px 0; max-width: 860px;">
        <div class="breadcrumbs">
          <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Account</span>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; flex-wrap: wrap; gap: 14px;">
          <div>
            <span class="text-eyebrow">Customer Portal</span>
            <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-top: 4px;">Welcome, ${currentUser.name}</h1>
          </div>
          <button class="btn-minimal btn-minimal-outline" onclick="setCurrentUser(null); renderCurrentRoute();">Sign Out</button>
        </div>

        <!-- Client Account Details Summary -->
        <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px 28px; margin-bottom: 28px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid var(--color-border); padding-bottom: 12px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem;">Account Overview</h3>
            <span style="font-size: 0.72rem; background: #FCEEF2; color: var(--color-primary); font-weight: 700; padding: 4px 10px; border-radius: var(--radius-pill); text-transform: uppercase;">Verified Member</span>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; font-size: 0.88rem;">
            <div><span style="color: var(--color-text-secondary); display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em;">Full Name</span><strong>${currentUser.name}</strong></div>
            <div><span style="color: var(--color-text-secondary); display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em;">Email Address</span><strong>${currentUser.email || 'Not provided'}</strong></div>
            <div><span style="color: var(--color-text-secondary); display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em;">Mobile Number</span><strong>${currentUser.phone || 'Not provided'}</strong></div>
            <div><span style="color: var(--color-text-secondary); display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em;">Member Since</span><strong>${currentUser.joinedDate || '2026'}</strong></div>
          </div>
        </div>

        <!-- DEDICATED SKINCARE & DEMOGRAPHIC PROFILING SECTION -->
        <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 26px 28px; margin-bottom: 32px;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
            <div>
              <span class="text-eyebrow" style="color: var(--color-primary);">Dermatological Customization</span>
              <h3 style="font-family: var(--font-serif); font-size: 1.3rem; margin-top: 4px;">Skin & Demographic Profile</h3>
              <p style="font-size: 0.85rem; color: var(--color-text-secondary); margin-top: 4px; line-height: 1.5; max-width: 580px;">
                Tailor your profile so our clinical recommendation engine presents formulations specifically matched to your skin barrier, tone goals, and age.
              </p>
            </div>
            ${hasSkinProfile && !isEditingSkinProfile ? `
              <button class="btn-minimal btn-minimal-outline" style="font-size: 0.8rem; padding: 6px 14px;" onclick="isEditingSkinProfile = true; renderCurrentRoute();">Edit Profile</button>
            ` : ''}
          </div>

          ${hasSkinProfile && !isEditingSkinProfile ? `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; margin-top: 8px;">
              <div>
                <span style="display: block; font-size: 0.72rem; text-transform: uppercase; color: var(--color-text-secondary);">Demographic</span>
                <strong style="font-size: 0.92rem;">${currentUser.gender || 'Not specified'} &bull; ${currentUser.ageGroup || 'Adult'}</strong>
              </div>
              <div>
                <span style="display: block; font-size: 0.72rem; text-transform: uppercase; color: var(--color-text-secondary);">Skin Barrier</span>
                <strong style="font-size: 0.92rem;">${currentUser.skinType || 'Balanced'}</strong>
              </div>
              <div style="grid-column: 1 / -1;">
                <span style="display: block; font-size: 0.72rem; text-transform: uppercase; color: var(--color-text-secondary);">Primary Dermatological Goal</span>
                <strong style="font-size: 0.92rem; color: var(--color-primary);">${currentUser.concern || 'Radiance & Hydration'}</strong>
              </div>
            </div>
          ` : `
            <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 22px; margin-top: 8px;">
              ${!hasSkinProfile ? `
                <div style="padding: 10px 14px; background: #FCEEF2; border-radius: var(--radius-sm); font-size: 0.82rem; color: var(--color-primary); font-weight: 600; margin-bottom: 18px;">
                  Profile incomplete &bull; Select your profile details below to unlock personalized recommendations.
                </div>
              ` : ''}
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 20px;">
                <div>
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Gender</label>
                  <select id="profileGender" class="form-input" style="width: 100%; padding: 10px 12px; font-size: 0.88rem; border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                    <option value="Female" ${currentUser.gender==='Female'?'selected':''}>Female</option>
                    <option value="Male" ${currentUser.gender==='Male'?'selected':''}>Male</option>
                    <option value="Non-binary / Other" ${currentUser.gender==='Non-binary / Other'?'selected':''}>Non-binary / Other</option>
                    <option value="Prefer not to say" ${currentUser.gender==='Prefer not to say'?'selected':''}>Prefer not to say</option>
                  </select>
                </div>
                <div>
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Age Bracket</label>
                  <select id="profileAge" class="form-input" style="width: 100%; padding: 10px 12px; font-size: 0.88rem; border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                    <option value="18-24 years" ${currentUser.ageGroup==='18-24 years'?'selected':''}>18 – 24 years</option>
                    <option value="25-34 years" ${(!currentUser.ageGroup || currentUser.ageGroup==='25-34 years')?'selected':''}>25 – 34 years</option>
                    <option value="35-44 years" ${currentUser.ageGroup==='35-44 years'?'selected':''}>35 – 44 years</option>
                    <option value="45-54 years" ${currentUser.ageGroup==='45-54 years'?'selected':''}>45 – 54 years</option>
                    <option value="55+ years" ${currentUser.ageGroup==='55+ years'?'selected':''}>55+ years</option>
                  </select>
                </div>
                <div>
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Skin Barrier Type</label>
                  <select id="profileSkinType" class="form-input" style="width: 100%; padding: 10px 12px; font-size: 0.88rem; border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                    <option value="Combination" ${(!currentUser.skinType || currentUser.skinType==='Combination')?'selected':''}>Combination</option>
                    <option value="Dry / Dehydrated" ${currentUser.skinType==='Dry / Dehydrated'?'selected':''}>Dry / Dehydrated</option>
                    <option value="Oily / Acne-Prone" ${currentUser.skinType==='Oily / Acne-Prone'?'selected':''}>Oily / Acne-Prone</option>
                    <option value="Sensitive" ${currentUser.skinType==='Sensitive'?'selected':''}>Sensitive</option>
                    <option value="Normal / Balanced" ${currentUser.skinType==='Normal / Balanced'?'selected':''}>Normal / Balanced</option>
                  </select>
                </div>
                <div>
                  <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Primary Skin Concern</label>
                  <select id="profileConcern" class="form-input" style="width: 100%; padding: 10px 12px; font-size: 0.88rem; border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                    <option value="Dark Spots & Pigmentation" ${(!currentUser.concern || currentUser.concern.includes('Pigment'))?'selected':''}>Dark Spots & Pigmentation</option>
                    <option value="Dullness & Dehydration" ${currentUser.concern && currentUser.concern.includes('Dullness')?'selected':''}>Dullness & Dehydration</option>
                    <option value="Scalp Flakes & Dandruff" ${currentUser.concern && currentUser.concern.includes('Scalp')?'selected':''}>Scalp Flakes & Dandruff</option>
                    <option value="Body Texture & Blemishes" ${currentUser.concern && currentUser.concern.includes('Body')?'selected':''}>Body Texture & Blemishes</option>
                    <option value="Underarm Friction & Tone" ${currentUser.concern && currentUser.concern.includes('Underarm')?'selected':''}>Underarm Friction & Tone</option>
                  </select>
                </div>
              </div>

              <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                <button class="btn-minimal btn-minimal-primary" style="padding: 10px 22px; font-size: 0.85rem;" onclick="saveCustomerSkinProfile()">Save Profile & Update Shelf</button>
                ${hasSkinProfile ? `
                  <button class="btn-minimal btn-minimal-outline" style="padding: 10px 18px; font-size: 0.85rem;" onclick="isEditingSkinProfile = false; renderCurrentRoute();">Cancel</button>
                ` : `
                  <a href="routine-finder.html" class="btn-minimal btn-minimal-outline" style="padding: 10px 18px; font-size: 0.85rem;" onclick="spaNavigate(event, 'routine-finder.html')">Take Routine Quiz Instead</a>
                `}
              </div>
            </div>
          `}
        </div>

        <!-- Curated Formulations Section -->
        <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 26px 28px; margin-bottom: 36px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 8px;">
            <div>
              <span class="text-eyebrow">Targeted Selection</span>
              <h3 style="font-family: var(--font-serif); font-size: 1.3rem; margin-top: 2px;">Curated For Your Skin Profile</h3>
            </div>
            <span style="font-size: 0.78rem; color: var(--color-text-secondary); background: #FFFFFF; padding: 4px 10px; border-radius: var(--radius-sm); border: 1px solid var(--color-border);">
              Active Focus: <strong>${currentUser.concern || 'Hydration & Radiance'}</strong>
            </span>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px;">
            ${curatedProducts.map(p => `
              <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px; text-align: center; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <img src="${p.image}" alt="${p.name}" style="height: 84px; object-fit: contain; margin: 0 auto 10px auto; display: block;">
                  <h4 style="font-size: 0.88rem; font-weight: 600; line-height: 1.3; margin-bottom: 4px;">${p.name}</h4>
                  <div style="font-size: 0.74rem; color: var(--color-text-secondary); margin-bottom: 10px;">${p.actives.split('•')[0]}</div>
                </div>
                <div>
                  <div style="font-size: 0.95rem; font-weight: 700; margin-bottom: 10px;">₹${p.price}</div>
                  <button class="btn-minimal btn-minimal-primary" style="font-size: 0.8rem; padding: 7px 14px; width: 100%;" onclick="addToBag('${p.id}', 1)">Add to Bag</button>
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
    // Unauthenticated: Sign In / Phone OTP / Create Account Tabs
    el.innerHTML = `
      <div class="container" style="padding: 40px 0 80px 0; max-width: 520px;">
        <div class="breadcrumbs">
          <a href="index.html" onclick="spaNavigate(event, 'index.html')">Home</a> &bull; <span>Account</span>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 36px 32px; box-shadow: var(--shadow-sm);">
          
          <!-- Mode Tabs -->
          <div style="display: flex; border-bottom: 1px solid var(--color-border); margin-bottom: 26px;">
            <button type="button" class="tab-btn ${accountAuthTab==='signin'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='signin'?'var(--color-primary)':'transparent'}; font-size: 0.85rem;" onclick="accountAuthTab='signin'; renderCurrentRoute();">Email</button>
            <button type="button" class="tab-btn ${accountAuthTab==='phone'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='phone'?'var(--color-primary)':'transparent'}; font-size: 0.85rem;" onclick="accountAuthTab='phone'; renderCurrentRoute();">Phone OTP</button>
            <button type="button" class="tab-btn ${accountAuthTab==='signup'?'active':''}" style="flex: 1; border-bottom: 2px solid ${accountAuthTab==='signup'?'var(--color-primary)':'transparent'}; font-size: 0.85rem;" onclick="accountAuthTab='signup'; renderCurrentRoute();">Create Account</button>
          </div>

          ${accountAuthTab === 'signin' ? `
            <!-- EMAIL SIGN IN -->
            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Email Address</label>
              <input type="email" id="authEmail" class="form-input" placeholder="name@example.com" value="user@thestella.in" style="width: 100%; padding: 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;">
            </div>
            <div style="margin-bottom: 22px;">
              <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Password</label>
              <div style="position: relative;">
                <input type="password" id="authPassword" class="form-input" value="password123" style="width: 100%; padding: 12px 50px 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;">
                <button type="button" onclick="togglePasswordVisibility('authPassword', this)" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 0.72rem; color: var(--color-text-secondary); cursor: pointer; text-transform: uppercase; font-weight: 600;">Show</button>
              </div>
            </div>
            <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-weight: 600;" onclick="executeUserSignIn()">Sign In with Email</button>
            <p style="font-size: 0.78rem; color: var(--color-text-secondary); text-align: center; margin-top: 14px;">Demo credentials prefilled for instant access.</p>
          ` : accountAuthTab === 'phone' ? `
            <!-- PHONE OTP SIGN IN -->
            <div id="phoneStep1">
              <div style="margin-bottom: 16px;">
                <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Mobile Number</label>
                <div style="display: flex; gap: 8px;">
                  <select id="authPhoneCountry" class="form-input" style="width: 140px; font-weight: 600; padding: 12px 8px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem; background: #FFFFFF;">
                    <option value="+91" selected>+91 (India)</option>
                    <option value="+1">+1 (US/CA)</option>
                    <option value="+44">+44 (UK)</option>
                    <option value="+971">+971 (UAE)</option>
                    <option value="+65">+65 (Singapore)</option>
                    <option value="+61">+61 (Australia)</option>
                  </select>
                  <input type="tel" id="authPhone" class="form-input" style="flex: 1; padding: 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;" placeholder="10-digit mobile number" maxlength="10" inputmode="numeric" oninput="this.value = this.value.replace(/\\D/g, '').slice(0, 10)">
                </div>
                <p style="font-size: 0.72rem; color: var(--color-text-secondary); margin-top: 5px;">Enter your 10-digit number to receive a one-time verification code.</p>
              </div>
              <div id="recaptcha-container"></div>
              <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-weight: 600;" onclick="executeSendOtp()">Send Verification Code</button>
            </div>

            <div id="phoneStep2" style="display: none;">
              <div style="margin-bottom: 16px;">
                <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Enter 6-Digit SMS Code</label>
                <input type="text" id="authOtpCode" class="form-input" placeholder="123456" maxlength="6" style="letter-spacing: 0.3em; text-align: center; font-size: 1.25rem; font-weight: 700; padding: 12px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); width: 100%;">
                <p style="font-size: 0.72rem; color: var(--color-text-secondary); text-align: center; margin-top: 6px;">For testing: you can enter 123456</p>
              </div>
              <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-weight: 600;" onclick="executeVerifyOtp()">Verify & Sign In</button>
              <button type="button" class="btn-minimal btn-minimal-outline" style="width: 100%; margin-top: 10px; font-size: 0.8rem; padding: 10px;" onclick="document.getElementById('phoneStep1').style.display='block'; document.getElementById('phoneStep2').style.display='none';">Re-enter Phone Number</button>
            </div>
          ` : `
            <!-- CREATE ACCOUNT FORM (PURE CONTACT ESSENTIALS ONLY) -->
            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Full Name</label>
              <input type="text" id="regName" class="form-input" placeholder="e.g. Avina Vasoya" style="width: 100%; padding: 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;">
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Email Address</label>
              <input type="email" id="regEmail" class="form-input" placeholder="name@example.com" style="width: 100%; padding: 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;">
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Mobile Number</label>
              <div style="display: flex; gap: 8px;">
                <select id="regCountryCode" class="form-input" style="width: 140px; font-weight: 600; padding: 12px 8px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem; background: #FFFFFF;">
                  <option value="+91" selected>+91 (India)</option>
                  <option value="+1">+1 (US/CA)</option>
                  <option value="+44">+44 (UK)</option>
                  <option value="+971">+971 (UAE)</option>
                  <option value="+65">+65 (Singapore)</option>
                  <option value="+61">+61 (Australia)</option>
                </select>
                <input type="tel" id="regPhone" class="form-input" style="flex: 1; padding: 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;" placeholder="10-digit mobile number" maxlength="10" inputmode="numeric" oninput="this.value = this.value.replace(/\\D/g, '').slice(0, 10)">
              </div>
              <p style="font-size: 0.72rem; color: var(--color-text-secondary); margin-top: 5px;">10-digit mobile number for order delivery & OTP updates.</p>
            </div>

            <div style="margin-bottom: 24px;">
              <label style="display: block; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Create Password</label>
              <div style="position: relative;">
                <input type="password" id="regPassword" class="form-input" placeholder="Create secure password (min 6 chars)" style="width: 100%; padding: 12px 50px 12px 14px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.9rem;">
                <button type="button" onclick="togglePasswordVisibility('regPassword', this)" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 0.72rem; color: var(--color-text-secondary); cursor: pointer; text-transform: uppercase; font-weight: 600;">Show</button>
              </div>
            </div>

            <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 14px; font-weight: 600;" onclick="executeUserSignUp()">Create Account</button>
            <p style="font-size: 0.75rem; color: var(--color-text-secondary); text-align: center; margin-top: 14px;">
              Skin and demographic preferences can be completed inside your portal.
            </p>
          `}

          <!-- Google Social Sign-In -->
          <div style="margin: 24px 0 16px 0; display: flex; align-items: center; text-align: center;">
            <div style="flex: 1; border-bottom: 1px solid var(--color-border);"></div>
            <span style="padding: 0 12px; font-size: 0.72rem; text-transform: uppercase; color: var(--color-text-secondary); letter-spacing: 0.05em;">Or Continue With</span>
            <div style="flex: 1; border-bottom: 1px solid var(--color-border);"></div>
          </div>

          <button type="button" class="btn-minimal btn-minimal-outline" style="width: 100%; padding: 12px; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 600; font-size: 0.88rem;" onclick="executeGoogleSignIn()">
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

async function saveCustomerSkinProfile() {
  const currentUser = getCurrentUser();
  if (!currentUser) return;

  const gender = document.getElementById('profileGender')?.value || 'Client';
  const ageGroup = document.getElementById('profileAge')?.value || '25-34 years';
  const skinType = document.getElementById('profileSkinType')?.value || 'Combination';
  const concern = document.getElementById('profileConcern')?.value || 'Dark Spots & Pigmentation';

  currentUser.gender = gender;
  currentUser.ageGroup = ageGroup;
  currentUser.skinType = skinType;
  currentUser.concern = concern;

  // Persist locally
  const users = getUsers();
  const idx = users.findIndex(u => u.id === currentUser.id || u.email === currentUser.email);
  if (idx > -1) {
    users[idx] = currentUser;
    localStorage.setItem('stella_users', JSON.stringify(users));
  }
  setCurrentUser(currentUser);

  // Sync to Cloud Firestore if connected
  if (window.firebase && window.firebase.firestore && currentUser.id) {
    window.firebase.firestore().collection('users').doc(currentUser.id).set({
      gender: gender,
      ageGroup: ageGroup,
      skinType: skinType,
      concern: concern,
      updatedAt: window.firebase.firestore.FieldValue.serverTimestamp()
    }, { merge: true }).catch(err => console.warn('Firestore profile sync notice:', err));
  }

  isEditingSkinProfile = false;
  showToast("Skin profile updated. Your recommended formulations are refreshed!");
  renderCurrentRoute();
}

async function executeGoogleSignIn() {
  if (window.StellaFirebase && window.StellaFirebase.auth) {
    try {
      showToast("Opening Google Sign-In...");
      const profile = await window.StellaFirebase.auth.signInWithGoogle();
      setCurrentUser(profile);
      showToast("Welcome, " + profile.name + ". Redirecting to home...");
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 400);
    } catch (err) {
      console.warn("Google Sign-In exception:", err);
      const isDomainError = err.code === 'auth/unauthorized-domain' || (err.message && err.message.includes('unauthorized-domain'));
      if (isDomainError) {
        showDomainAuthModal();
      } else {
        showToast(err.message || "Google Sign-In was cancelled.");
      }
    }
  } else {
    showToast("Connecting to Firebase...");
  }
}

async function executeSendOtp() {
  const country = document.getElementById('authPhoneCountry')?.value || '+91';
  const rawNum = document.getElementById('authPhone')?.value.replace(/\\D/g, '').trim();

  if (!rawNum || rawNum.length < 10) {
    showToast("Please enter a valid 10-digit mobile number.");
    return;
  }
  const fullPhone = country + rawNum;
  window._pendingOtpPhone = fullPhone;

  if (window.StellaFirebase && window.StellaFirebase.auth) {
    try {
      showToast("Sending verification code to " + fullPhone + "...");
      await window.StellaFirebase.auth.sendPhoneOtp(fullPhone, 'recaptcha-container');
      showToast("Verification code sent via SMS!");
      const s1 = document.getElementById('phoneStep1');
      const s2 = document.getElementById('phoneStep2');
      if (s1 && s2) {
        s1.style.display = 'none';
        s2.style.display = 'block';
      }
    } catch (err) {
      console.warn("Firebase Phone Auth notice:", err);
      const isRegionOrOp = err.code === 'auth/operation-not-allowed' || 
                           (err.message && (err.message.includes('operation-not-allowed') || err.message.includes('SMS unable to be sent')));
      if (isRegionOrOp) {
        showSmsRegionModal(fullPhone);
      } else {
        showToast(err.message || "Unable to send SMS. Check phone settings.");
      }
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

  // Support instant test verification
  if (window._pendingTestOtp && code === window._pendingTestOtp) {
    const userPhone = window._pendingOtpPhone || '+91 9876543210';
    const profile = {
      id: 'usr_p_' + Date.now(),
      name: 'Stella Client (' + userPhone.slice(-4) + ')',
      email: userPhone.replace(/\\D/g, '') + '@thestella.in',
      phone: userPhone,
      gender: '',
      ageGroup: '',
      skinType: '',
      concern: '',
      joinedDate: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    };
    const users = getUsers();
    users.push(profile);
    localStorage.setItem('stella_users', JSON.stringify(users));
    setCurrentUser(profile);
    showToast("Phone verified! Welcome, " + profile.name + ". Redirecting to home...");
    setTimeout(() => {
      window.location.href = 'index.html';
    }, 400);
    return;
  }

  if (window.StellaFirebase && window.StellaFirebase.auth) {
    try {
      showToast("Verifying code...");
      const profile = await window.StellaFirebase.auth.verifyPhoneOtp(code);
      setCurrentUser(profile);
      showToast("Phone verified! Welcome, " + profile.name + ". Redirecting to home...");
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 400);
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
      showToast("Signed in as " + profile.name + ". Redirecting to home...");
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 400);
      return;
    } catch (err) {
      console.warn("Firebase email sign-in fallback:", err.message);
    }
  }
  const users = getUsers();
  const u = users.find(x => x.email === email && x.password === pass);
  if (u) {
    setCurrentUser(u);
    showToast("Signed in as " + u.name + ". Redirecting to home...");
    setTimeout(() => {
      window.location.href = 'index.html';
    }, 400);
  } else {
    showToast("Invalid email or password.");
  }
}

async function executeUserSignUp() {
  const name = document.getElementById('regName')?.value.trim();
  const email = document.getElementById('regEmail')?.value.trim();
  const countryCode = document.getElementById('regCountryCode')?.value || '+91';
  const rawNum = document.getElementById('regPhone')?.value.replace(/\\D/g, '').trim();
  const pass = document.getElementById('regPassword')?.value.trim();

  if (!name || !email || !pass) {
    showToast("Please enter your full name, email address, and password.");
    return;
  }
  if (!rawNum || rawNum.length < 10) {
    showToast("Please enter a valid 10-digit mobile number.");
    return;
  }
  if (pass.length < 6) {
    showToast("Password must be at least 6 characters.");
    return;
  }

  const fullPhone = countryCode + ' ' + rawNum;

  const userProfile = {
    id: 'usr_' + Date.now(),
    name: name,
    email: email,
    phone: fullPhone,
    gender: '',
    ageGroup: '',
    skinType: '',
    concern: '',
    password: pass,
    joinedDate: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
  };

  if (window.StellaFirebase && window.StellaFirebase.auth) {
    try {
      showToast("Registering account in Firebase...");
      const fbProfile = await window.StellaFirebase.auth.signUpWithEmail(email, pass, name, fullPhone);
      userProfile.id = fbProfile.id;
    } catch (err) {
      console.warn("Firebase sign up fallback:", err.message);
      if (err.code === 'auth/email-already-in-use') {
        showToast("An account with this email already exists. Please sign in.");
        return;
      }
    }
  }

  const users = getUsers();
  const existingIdx = users.findIndex(u => u.email.toLowerCase() === email.toLowerCase());
  if (existingIdx > -1) {
    users[existingIdx] = userProfile;
  } else {
    users.push(userProfile);
  }
  localStorage.setItem('stella_users', JSON.stringify(users));
  setCurrentUser(userProfile);

  showToast("Welcome to The Stella, " + name + "! Redirecting to home...");
  
  // Explicit requirement: user should be redirected to home page after creating account
  setTimeout(() => {
    window.location.href = 'index.html';
  }, 400);
}
'''

new_section_10 = '''// ==========================================
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
      <div class="container" style="max-width: 840px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 32px;">
          
          <!-- Live Tracking Box -->
          <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 26px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 8px;">Live Order Search</h3>
            <p style="font-size: 0.85rem; color: var(--color-text-secondary); margin-bottom: 16px;">
              Enter your Stella Order ID (e.g. STL-90412) to retrieve dispatch tracking from Cloud Firestore.
            </p>
            <div style="display: flex; gap: 8px; margin-bottom: 16px;">
              <input type="text" id="trackInput" placeholder="STL-XXXXX" class="form-input" style="font-size: 0.85rem; text-transform: uppercase; padding: 10px 12px; flex: 1; border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
              <button class="btn-minimal btn-minimal-primary" style="padding: 10px 18px;" onclick="trackOrder()">Track</button>
            </div>
            <div id="trackResultBox"></div>
          </div>

          <!-- Contact Form with 2-Field Mobile Number -->
          <div style="background: #FFFFFF; border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 26px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 8px;">Client Concierge Inquiry</h3>
            <p style="font-size: 0.85rem; color: var(--color-text-secondary); margin-bottom: 16px;">
              Our dermatological team answers all inquiries within 24 hours.
            </p>

            <div style="margin-bottom: 12px;">
              <label style="display: block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px;">Your Name</label>
              <input type="text" id="inqName" placeholder="e.g. Avina Vasoya" class="form-input" style="width: 100%; padding: 10px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem;">
            </div>

            <div style="margin-bottom: 12px;">
              <label style="display: block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px;">Email Address</label>
              <input type="email" id="inqEmail" placeholder="name@example.com" class="form-input" style="width: 100%; padding: 10px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem;">
            </div>

            <div style="margin-bottom: 12px;">
              <label style="display: block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px;">Mobile Number</label>
              <div style="display: flex; gap: 8px;">
                <select id="inqCountry" class="form-input" style="width: 130px; font-weight: 600; padding: 10px 8px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.85rem; background: #FFFFFF;">
                  <option value="+91" selected>+91 (India)</option>
                  <option value="+1">+1 (US/CA)</option>
                  <option value="+44">+44 (UK)</option>
                  <option value="+971">+971 (UAE)</option>
                </select>
                <input type="tel" id="inqPhone" placeholder="10-digit mobile" maxlength="10" inputmode="numeric" oninput="this.value = this.value.replace(/\\D/g, '').slice(0, 10)" class="form-input" style="flex: 1; padding: 10px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem;">
              </div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px;">Message</label>
              <textarea id="inqMsg" rows="3" placeholder="How can our clinical team assist with your routine?" class="form-input" style="width: 100%; padding: 10px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.88rem;"></textarea>
            </div>

            <button class="btn-minimal btn-minimal-primary" style="width: 100%; padding: 12px; font-weight: 600;" onclick="submitInquiry()">Submit Inquiry</button>
          </div>

        </div>
      </div>
    </section>
  `;
}

async function trackOrder() {
  const q = document.getElementById('trackInput')?.value.trim().toUpperCase();
  const box = document.getElementById('trackResultBox');
  if (!box || !q) return;

  box.innerHTML = `<p style="color: var(--color-text-secondary); font-size: 0.85rem; margin-top: 10px;">Searching Cloud Firestore...</p>`;

  let match = null;
  if (window.StellaFirebase && window.StellaFirebase.db) {
    try {
      match = await window.StellaFirebase.db.lookupOrder(q);
    } catch (err) {
      console.warn('Firestore tracking lookup fallback:', err);
    }
  }

  if (!match) {
    const orders = getOrders();
    match = orders.find(o => (o.id === q || o.orderId === q));
  }

  if (match) {
    box.innerHTML = `
      <div style="background: #FDFBFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 14px; font-size: 0.85rem; margin-top: 10px;">
        <div style="font-weight: 700; color: var(--color-primary); margin-bottom: 4px;">Found: ${match.id || match.orderId}</div>
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
  const phone = document.getElementById('inqPhone');
  if (phone) phone.value = '';
}

// Initialize SPA on load
document.addEventListener('DOMContentLoaded', () => {
  renderCurrentRoute();
});
'''

# Construct the updated content
updated_content = content[:s8_pos] + new_section_8 + '\n' + content[s9_pos:s10_pos] + new_section_10

with open('assets/js/app.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("SUCCESS: assets/js/app.js updated successfully!")
