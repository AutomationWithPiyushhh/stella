import crypto from 'crypto';

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST.' });
  }

  const keySecret = process.env.RAZORPAY_KEY_SECRET;

  if (!keySecret) {
    return res.status(500).json({ error: 'Razorpay secret not configured in environment.' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const orderId = body.order_id || body.razorpay_order_id;
    const paymentId = body.payment_id || body.razorpay_payment_id;
    const clientSignature = body.signature || body.razorpay_signature;

    if (!orderId || !paymentId || !clientSignature) {
      return res.status(400).json({
        error: 'Missing required fields for signature verification (order_id, payment_id, signature).'
      });
    }

    const payload = `${orderId}|${paymentId}`;
    const generatedSignature = crypto
      .createHmac('sha256', keySecret)
      .update(payload)
      .digest('hex');

    const isMatch = crypto.timingSafeEqual(
      Buffer.from(generatedSignature, 'utf-8'),
      Buffer.from(clientSignature, 'utf-8')
    );

    if (isMatch) {
      return res.status(200).json({
        status: 'success',
        message: 'Payment verified successfully.',
        order_id: orderId,
        payment_id: paymentId
      });
    } else {
      return res.status(400).json({
        status: 'failure',
        error: 'Signature verification failed. Potential payment tampering detected.'
      });
    }
  } catch (err) {
    return res.status(500).json({
      error: 'Error during signature verification: ' + err.message
    });
  }
}
