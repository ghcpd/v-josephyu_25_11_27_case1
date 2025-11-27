import requests, re
s = requests.Session()
base='http://127.0.0.1:5000'
print('GET /register')
r = s.get(base+'/register')
print('status', r.status_code)
# Find csrf token
m = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
if m:
    token = m.group(1)
    print('CSRF token found')
else:
    token = None
    print('No CSRF token found')
# Try to register
if token:
    data = {'username':'testuser','email':'test@example.com','password':'password123','csrf_token':token}
    r2 = s.post(base+'/register', data=data, allow_redirects=False)
    print('POST /register status', r2.status_code)
    print('Location:', r2.headers.get('Location'))
    print('Body snippet:', r2.text[:300])
else:
    print('skipping POST')
