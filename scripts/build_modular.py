import re

with open('index.html') as f:
    full = f.read()

# Extract script inside <script> at bottom of index.html
s = re.search(r'<script>(.*?)</script>\s*</body>', full, re.DOTALL)
if s:
    app_js = s.group(1).strip()
    with open('assets/js/app.js', 'w') as f:
        f.write(app_js)
    print('assets/js/app.js created! Length:', len(app_js))
else:
    print('Could not find script block')

