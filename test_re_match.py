import requests, re
r = requests.get('http://127.0.0.1:5000/register')
print('has csrf token', 'csrf_token' in r.text)
print('match name attribute', bool(re.search(r'name="csrf_token"', r.text)))
# match the value attribute after csrf_token
m = re.search(r'name="csrf_token"\s+value="(.*?)"', r.text, flags=re.S)
print('token via name-value pattern?', bool(m))
if m:
    print('token start', m.group(1)[:40], 'len', len(m.group(1)))
else:
    # fallback: match any value attribute found in snippet
    m2 = re.search(r'value="(.*?)"', r.text, flags=re.S)
    print('first value attr', bool(m2))
    if m2:
        print(m2.group(1)[:80])
