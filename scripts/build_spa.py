import os, re, json

with open('index.html') as f:
    home_src = f.read()

# We can create a self-routing master HTML with template sections
# When navigating to /shop.html, it shows shop view
# When /product.html, shows product view
# etc.

# Let's inspect each HTML file's <main> or content
pages = ['shop.html', 'product.html', 'haircare.html', 'about.html', 'routine-finder.html', 'checkout.html', 'account.html', 'admin.html', 'contact.html']

extracted = {}
for p in pages:
    with open(p) as f:
        content = f.read()
    # strip header, footer, announcement-bar, scripts
    # Find between </header> and <footer
    m = re.search(r'</header>\s*(.*?)\s*<footer', content, re.DOTALL)
    if m:
        body_part = m.group(1).strip()
    else:
        body_part = ""
    # Find inline script
    s = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    script_part = s.group(1).strip() if s else ""
    extracted[p] = {
        'html': body_part,
        'script': script_part
    }
    print(f'Extracted {p}: html={len(body_part)} chars, script={len(script_part)} chars')

