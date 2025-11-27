import requests, re
base='http://127.0.0.1:5000'
resp = requests.get(base + '/register')
m = re.search(r'name="csrf_token" value="([^"]+)"', resp.text, flags=re.S)
t = m.group(1) if m else ''
payload = {'username': 'bob1', 'email': 'bob1@example.com', 'password': '123', 'csrf_token': t}
resp2 = requests.post(base + '/register', data=payload)
print('status', resp2.status_code)
print(resp2.text)
