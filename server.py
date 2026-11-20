#!/usr/bin/env python3
"""
The Stella — Local Development Server with Razorpay Standard Checkout Endpoints
"""

import os
import json
import hmac
import hashlib
import base64
import urllib.parse
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 1. Load Environment Variables from .env
def load_env(env_path='.env'):
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value

load_env()

RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_live_U2Nb9Nn5yOhCQj')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '1nBYlU5iSwYUneYYvU4Ws3Ov')

# Initialize Razorpay Client if SDK available
try:
    import razorpay
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except Exception as e:
    razorpay_client = None
    print(f"Notice: Razorpay Python SDK fallback mode: {e}")

class StellaCheckoutHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # Endpoint: GET /api/config
        if parsed.path == '/api/config':
            return self.send_json(200, {
                'key_id': RAZORPAY_KEY_ID
            })

        # Static file handling (SPA fallback for clean URLs)
        clean_path = parsed.path.lstrip('/')
        if clean_path and not os.path.exists(clean_path):
            if os.path.exists(clean_path + '.html'):
                self.path = '/' + clean_path + '.html'
            elif not clean_path.startswith('api/'):
                self.path = '/index.html'

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)

        try:
            body = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        except Exception:
            return self.send_json(400, {'error': 'Malformed JSON payload.'})

        # ==============================================================
        # STEP 1: BACKEND - Create Order (POST /api/create-order)
        # ==============================================================
        if parsed.path == '/api/create-order':
            if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
                return self.send_json(500, {'error': 'Razorpay credentials not configured in environment.'})

            amount = body.get('amount')
            currency = body.get('currency', 'INR')
            receipt = body.get('receipt', 'receipt_order')

            # Validate amount >= 100 paise
            try:
                amount_int = int(amount)
            except (ValueError, TypeError):
                return self.send_json(400, {'error': 'Invalid amount parameter. Must be an integer.'})

            if amount_int < 100:
                return self.send_json(400, {'error': 'Invalid amount. Minimum amount is 100 paise (₹1.00).'})

            try:
                # Use razorpay Python SDK or direct HTTP request
                if razorpay_client:
                    order = razorpay_client.order.create({
                        'amount': amount_int,
                        'currency': currency,
                        'receipt': receipt
                    })
                    order_id = order['id']
                    order_amount = order['amount']
                    order_currency = order['currency']
                else:
                    req_data = json.dumps({
                        'amount': amount_int,
                        'currency': currency,
                        'receipt': receipt
                    }).encode('utf-8')
                    auth_b64 = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode('utf-8')).decode('utf-8')
                    req = urllib.request.Request(
                        'https://api.razorpay.com/v1/orders',
                        data=req_data,
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Basic {auth_b64}'
                        },
                        method='POST'
                    )
                    with urllib.request.urlopen(req) as resp:
                        res = json.loads(resp.read().decode('utf-8'))
                        order_id = res['id']
                        order_amount = res['amount']
                        order_currency = res['currency']

                return self.send_json(200, {
                    'order_id': order_id,
                    'amount': order_amount,
                    'currency': order_currency,
                    'key_id': RAZORPAY_KEY_ID
                })

            except Exception as e:
                err_str = str(e)
                if '401' in err_str or 'Unauthorized' in err_str:
                    return self.send_json(401, {'error': 'Razorpay authentication failed. Invalid API credentials.'})
                return self.send_json(500, {'error': f'Razorpay API error: {err_str}'})

        # ==============================================================
        # STEP 3: BACKEND - Verify Signature (POST /api/verify-payment)
        # ==============================================================
        elif parsed.path == '/api/verify-payment':
            if not RAZORPAY_KEY_SECRET:
                return self.send_json(500, {'error': 'Razorpay secret not configured in environment.'})

            order_id = body.get('order_id') or body.get('razorpay_order_id')
            payment_id = body.get('payment_id') or body.get('razorpay_payment_id')
            signature = body.get('signature') or body.get('razorpay_signature')

            # Missing fields check
            if not order_id or not payment_id or not signature:
                return self.send_json(400, {
                    'error': 'Missing required fields for verification (order_id, payment_id, signature).'
                })

            # Algorithm: HMAC-SHA256(order_id + "|" + payment_id, KEY_SECRET)
            message = f"{order_id}|{payment_id}"
            generated_signature = hmac.new(
                RAZORPAY_KEY_SECRET.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            # Compare generated signature with razorpay_signature
            if hmac.compare_digest(generated_signature, signature):
                return self.send_json(200, {
                    'status': 'success',
                    'message': 'Payment verified successfully',
                    'order_id': order_id,
                    'payment_id': payment_id
                })
            else:
                return self.send_json(400, {
                    'status': 'failure',
                    'error': 'Signature verification mismatch. Payment verification failed.'
                })

        else:
            return self.send_json(404, {'error': 'Endpoint not found.'})

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, StellaCheckoutHandler)
    print(f"The Stella Server running on http://localhost:{port}")
    print(f"Loaded Razorpay Key ID: {RAZORPAY_KEY_ID}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    run(port)
