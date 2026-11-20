/**
 * THE STELLA — FIREBASE CLIENT & CLOUD FIRESTORE CONNECTOR
 * Firebase Project: the-stella
 * Zero Emojis. Clean Minimalist Architecture.
 */

(function (window) {
  'use strict';

  // 1. Production Configuration for project: the-stella
  const STELLA_FIREBASE_CONFIG = {
    apiKey: "AIzaSyAvX23SJ-HIncMGQ5L3tcFTHPph-hCuYc4",
    authDomain: "the-stella.firebaseapp.com",
    projectId: "the-stella",
    storageBucket: "the-stella.firebasestorage.app",
    messagingSenderId: "878098792028",
    appId: "1:878098792028:web:fd3b93e29325171693f099"
  };

  let app = null;
  let auth = null;
  let db = null;
  let confirmationResult = null;
  let recaptchaVerifier = null;

  function isConfigured() {
    return Boolean(STELLA_FIREBASE_CONFIG.apiKey && STELLA_FIREBASE_CONFIG.apiKey.startsWith('AIzaSy'));
  }

  function initialize() {
    if (!window.firebase) {
      console.warn('Firebase SDK scripts not loaded yet');
      return false;
    }

    try {
      if (!firebase.apps.length) {
        app = firebase.initializeApp(STELLA_FIREBASE_CONFIG);
      } else {
        app = firebase.app();
      }
      auth = firebase.auth();
      db = firebase.firestore();

      auth.setPersistence(firebase.auth.Auth.Persistence.LOCAL).catch(err => {
        console.warn('Auth persistence notice:', err.message);
      });

      console.info('Firebase initialized for project: the-stella');
      return true;
    } catch (err) {
      console.error('Firebase initialization failed:', err);
      return false;
    }
  }

  // 2. Authentication Methods
  const StellaAuth = {
    isReady: () => Boolean(auth),

    // Email & Password Sign Up
    signUpWithEmail: async function (email, password, displayName, phone) {
      if (!auth) initialize();
      if (!auth) throw new Error('Firebase authentication is not ready.');
      
      const cred = await auth.createUserWithEmailAndPassword(email, password);
      const user = cred.user;
      if (displayName && user.updateProfile) {
        await user.updateProfile({ displayName: displayName });
      }

      // Sync customer record to Firestore
      if (db) {
        try {
          await db.collection('users').doc(user.uid).set({
            id: user.uid,
            uid: user.uid,
            name: displayName || email.split('@')[0],
            email: email,
            phone: phone || '',
            joinedDate: new Date().toISOString().split('T')[0],
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
          }, { merge: true });
        } catch (e) {
          console.warn('User document creation notice:', e);
        }
      }

      return {
        id: user.uid,
        name: displayName || user.displayName || email.split('@')[0],
        email: user.email,
        phone: phone || user.phoneNumber || ''
      };
    },

    // Email & Password Sign In
    signInWithEmail: async function (email, password) {
      if (!auth) initialize();
      if (!auth) throw new Error('Firebase authentication is not ready.');
      
      const cred = await auth.signInWithEmailAndPassword(email, password);
      const user = cred.user;

      let profileData = {
        id: user.uid,
        name: user.displayName || user.email.split('@')[0],
        email: user.email,
        phone: user.phoneNumber || ''
      };

      if (db) {
        try {
          const doc = await db.collection('users').doc(user.uid).get();
          if (doc.exists) {
            profileData = Object.assign(profileData, doc.data());
          }
        } catch (e) {
          console.warn('User profile fetch notice:', e);
        }
      }

      return profileData;
    },

    // Google Sign-In (Popup)
    signInWithGoogle: async function () {
      if (!auth) initialize();
      if (!auth) throw new Error('Firebase authentication is not ready.');
      
      const provider = new firebase.auth.GoogleAuthProvider();
      provider.addScope('email');
      provider.addScope('profile');

      const cred = await auth.signInWithPopup(provider);
      const user = cred.user;

      const profileData = {
        id: user.uid,
        name: user.displayName || user.email.split('@')[0],
        email: user.email,
        phone: user.phoneNumber || '',
        photoURL: user.photoURL || ''
      };

      if (db) {
        try {
          await db.collection('users').doc(user.uid).set({
            id: user.uid,
            uid: user.uid,
            name: profileData.name,
            email: profileData.email,
            phone: profileData.phone,
            joinedDate: new Date().toISOString().split('T')[0],
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
          }, { merge: true });
        } catch (e) {
          console.warn('Google profile sync notice:', e);
        }
      }

      return profileData;
    },

    // Phone Authentication: Send OTP
    sendPhoneOtp: async function (phoneNumber, containerId) {
      if (!auth) initialize();
      if (!auth) throw new Error('Firebase authentication is not ready.');
      if (!phoneNumber || phoneNumber.length < 8) {
        throw new Error('Please provide a valid phone number with country code (e.g., +91 9876543210).');
      }

      const targetId = containerId || 'recaptcha-container';
      if (!recaptchaVerifier) {
        recaptchaVerifier = new firebase.auth.RecaptchaVerifier(targetId, {
          size: 'invisible',
          callback: () => {
            // Invisible reCAPTCHA resolved
          }
        });
      }

      confirmationResult = await auth.signInWithPhoneNumber(phoneNumber, recaptchaVerifier);
      return confirmationResult;
    },

    // Phone Authentication: Verify OTP
    verifyPhoneOtp: async function (verificationCode) {
      if (!confirmationResult) {
        throw new Error('No pending OTP request. Please request an OTP first.');
      }
      const cred = await confirmationResult.confirm(verificationCode);
      const user = cred.user;

      const profileData = {
        id: user.uid,
        name: user.displayName || 'Stella Client (' + user.phoneNumber.slice(-4) + ')',
        email: user.email || (user.phoneNumber + '@thestella.in'),
        phone: user.phoneNumber
      };

      if (db) {
        try {
          await db.collection('users').doc(user.uid).set({
            id: user.uid,
            uid: user.uid,
            name: profileData.name,
            phone: user.phoneNumber,
            joinedDate: new Date().toISOString().split('T')[0],
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
          }, { merge: true });
        } catch (e) {
          console.warn('Phone user sync notice:', e);
        }
      }

      return profileData;
    },

    // Sign Out
    signOut: async function () {
      if (auth) {
        await auth.signOut();
      }
    },

    // Listen for Auth Changes
    onAuthStateChanged: function (callback) {
      if (!auth) initialize();
      if (!auth) return () => {};
      return auth.onAuthStateChanged(callback);
    }
  };

  // 3. Firestore Database Methods
  const StellaDb = {
    isReady: () => Boolean(db),

    // Realtime Orders Listener
    listenOrders: function (callback) {
      if (!db) initialize();
      if (!db) return () => {};
      return db.collection('orders').orderBy('createdAt', 'desc').onSnapshot(
        snapshot => {
          const list = [];
          snapshot.forEach(doc => {
            list.push(doc.data());
          });
          callback(list);
        },
        error => {
          console.warn('Firestore orders sync notice:', error.message);
        }
      );
    },

    // Create Order in Firestore (sanitized against strict firestore.rules)
    createOrder: async function (orderObj) {
      if (!db) initialize();
      if (!db) return null;
      const allowedKeys = [
        'id', 'date', 'customerName', 'phone', 'address',
        'items', 'total', 'status', 'paymentMethod',
        'customerEmail', 'userId', 'subtotal', 'discount',
        'shipping', 'trackingNumber', 'notes'
      ];
      const cleanOrder = {};
      for (let i = 0; i < allowedKeys.length; i++) {
        const k = allowedKeys[i];
        if (orderObj[k] !== undefined && orderObj[k] !== null && orderObj[k] !== '') {
          cleanOrder[k] = orderObj[k];
        }
      }
      cleanOrder.createdAt = firebase.firestore.FieldValue.serverTimestamp();
      cleanOrder.updatedAt = firebase.firestore.FieldValue.serverTimestamp();
      await db.collection('orders').doc(orderObj.id).set(cleanOrder);
      return cleanOrder;
    },

    // Update Order Status (Restricted to Admin by Security Rules)
    updateOrderStatus: async function (orderId, newStatus) {
      if (!db) initialize();
      if (!db) return;
      await db.collection('orders').doc(orderId).update({
        status: newStatus,
        updatedAt: firebase.firestore.FieldValue.serverTimestamp()
      });
    },

    // Public Order Lookup by exact Order ID
    lookupOrder: async function (orderId) {
      if (!db) initialize();
      if (!db) return null;
      const doc = await db.collection('orders').doc(orderId).get();
      return doc.exists ? doc.data() : null;
    },

    // Realtime Catalog Listener
    listenProducts: function (callback) {
      if (!db) initialize();
      if (!db) return () => {};
      return db.collection('products').onSnapshot(
        snapshot => {
          const list = [];
          snapshot.forEach(doc => {
            list.push(doc.data());
          });
          if (list.length > 0) {
            callback(list);
          }
        },
        error => {
          console.warn('Firestore products sync notice:', error.message);
        }
      );
    },

    // Seed Master Catalog to Firestore if Empty
    seedProductsIfEmpty: async function (defaultCatalog) {
      if (!db) initialize();
      if (!db) return;
      try {
        const snapshot = await db.collection('products').limit(1).get();
        if (snapshot.empty && Array.isArray(defaultCatalog)) {
          console.info('Seeding initial master products into Firestore...');
          const batch = db.batch();
          defaultCatalog.forEach(p => {
            const ref = db.collection('products').doc(p.id);
            batch.set(ref, Object.assign({}, p, {
              createdAt: firebase.firestore.FieldValue.serverTimestamp()
            }));
          });
          await batch.commit();
          console.info('Successfully seeded', defaultCatalog.length, 'products to Firestore.');
        }
      } catch (err) {
        console.warn('Product seeding notice:', err.message);
      }
    },

    // Update Product Price & Stock (Admin)
    updateProduct: async function (productId, updates) {
      if (!db) initialize();
      if (!db) return;
      await db.collection('products').doc(productId).update(
        Object.assign({}, updates, {
          updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        })
      );
    }
  };

  // Expose to window
  window.StellaFirebase = {
    init: initialize,
    isConfigured: isConfigured,
    getConfig: () => STELLA_FIREBASE_CONFIG,
    auth: StellaAuth,
    db: StellaDb
  };

  // Auto-init on script load if firebase is present
  if (typeof window !== 'undefined') {
    if (window.firebase) {
      initialize();
    } else {
      window.addEventListener('DOMContentLoaded', initialize);
    }
  }

})(window);
