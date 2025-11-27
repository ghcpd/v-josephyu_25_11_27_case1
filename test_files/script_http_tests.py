import requests
base='http://127.0.0.1:5000'
print('GET /signup ->', requests.get(base + '/signup').status_code)
print('GET /register ->', requests.get(base + '/register').status_code)
print('POST /api/register ->', requests.post(base + '/api/register', json={'user':'a','pass':'1'}).status_code)
print('POST /api/login ->', requests.post(base + '/api/login', json={'user':'a','pass':'1'}).status_code)
print('GET /profile ->', requests.get(base + '/profile').status_code)
