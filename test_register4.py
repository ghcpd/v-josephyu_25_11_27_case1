import requests, re
s = requests.Session()
base='http://127.0.0.1:5000'
r = s.get(base+'/register')
# print snippet
idx = r.text.find('csrf_token')
print('snippet:', r.text[idx-80:idx+150])
# print exact token input tag line
start = r.text.rfind('<input', 0, idx)
end = r.text.find('>', idx)
if start!=-1 and end!=-1:
    line = r.text[start:end+1]
    print('input tag line:')
    print(line)
else:
    print('no input tag found')
