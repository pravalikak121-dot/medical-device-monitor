import requests
import sys

url = 'http://127.0.0.1:8001/api/v1/auth/register'
payload = {
    'username': 'testuser123',
    'email': 'testuser123@example.com',
    'password': 'Pass1234',
    'role': 'nurse'
}

try:
    r = requests.post(url, json=payload, timeout=10)
    print('STATUS', r.status_code)
    print('CONTENT-TYPE', r.headers.get('content-type'))
    print('TEXT_REPR', repr(r.text))
    try:
        print('JSON:', r.json())
    except Exception as e:
        print('JSON ERROR:', e)
except Exception as e:
    print('REQUEST ERROR:', e)
    sys.exit(1)
