import requests, re
s = requests.Session()
base='http://127.0.0.1:5000'
r = s.get(base+'/register')
# we use DOTALL to allow matching across newlines
m = re.search(r'name="csrf_token" value="([^"]+)"', r.text, flags=re.S)
print('found token', bool(m))
if m:
    t=m.group(1)
    print('token length', len(t))
    data={'username':'testuser2','email':'test2@example.com','password':'password123','csrf_token':t}
    r2 = s.post(base+'/register', data=data, allow_redirects=False)
    print('post status', r2.status_code)
    print('location', r2.headers.get('Location'))
else:
    print('no token')
