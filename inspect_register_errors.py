import requests
s=requests.Session()
base='http://127.0.0.1:5000'
r=s.get(base+'/register')
# get csrf token
import re
m=re.search(r'name="csrf_token" value="([^"]+)"', r.text, flags=re.S)
if m:
    token=m.group(1)
else:
    token=''
# Try to register with short password
payload={'username':'bob1','email':'bob1@example.com','password':'123','csrf_token':token}
r2=s.post(base+'/register', data=payload)
print('status',r2.status_code)
print(r2.text)
