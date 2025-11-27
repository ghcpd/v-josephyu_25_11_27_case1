import requests
import re
base='http://127.0.0.1:5000'
resp = requests.get(base+'/register')
idx = resp.text.find('csrf_token')
print('CSRF token present:', idx!=-1)
start = resp.text.rfind('<input', 0, idx)
end = resp.text.find('>', idx)
print(resp.text[start:end+1])
