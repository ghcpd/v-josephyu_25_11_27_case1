import requests
s=requests.Session()
url='http://127.0.0.1:5000/register'
r=s.get(url)
idx=r.text.find('csrf_token')
print('Found csrf_token?', idx!=-1)
print(r.text[idx-120:idx+120])
