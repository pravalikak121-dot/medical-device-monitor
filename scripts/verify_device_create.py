from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))
import requests
API_URL = 'http://127.0.0.1:8001'

print('Login as existing doctor...')
login = requests.post(f'{API_URL}/api/v1/auth/login', json={'username':'doctoruser1','password':'DocPass123'})
print('LOGIN', login.status_code, login.text)
if login.status_code != 200:
    sys.exit(1)
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print('Create device...')
create = requests.post(f'{API_URL}/api/v1/devices', json={'device_id':'AUTO-TEST-01','patient_id':'PAT-001','device_type':'Auto Test','battery_level':60,'signal_strength':85}, headers=headers)
print('CREATE', create.status_code, create.text)
print('Fetch devices...')
fetch = requests.get(f'{API_URL}/api/v1/devices', headers=headers)
print('DEVICES', fetch.status_code, fetch.text)
