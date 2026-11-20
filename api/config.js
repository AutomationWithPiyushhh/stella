export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Return public Key ID only - never expose KEY_SECRET
  return res.status(200).json({
    key_id: process.env.RAZORPAY_KEY_ID || 'rzp_test_U2MEsqbiNgtArA'
  });
}
