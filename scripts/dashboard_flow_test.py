import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))

import requests

API_URL = 'http://127.0.0.1:8001'

print('Testing backend at', API_URL)

# Test register doctor
reg_payload = {
    'username': 'doctor_test_user',
    'email': 'doctor_test_user@example.com',
    'password': 'DocPass123',
    'role': 'doctor'
}
reg_resp = requests.post(f'{API_URL}/api/v1/auth/register', json=reg_payload)
print('Register status:', reg_resp.status_code)
print('Register body:', reg_resp.text)

# Test login
login_payload = {
    'username': 'doctor_test_user',
    'password': 'DocPass123'
}
login_resp = requests.post(f'{API_URL}/api/v1/auth/login', json=login_payload)
print('Login status:', login_resp.status_code)
print('Login body:', login_resp.text)

if login_resp.status_code == 200:
    token = login_resp.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    device_payload = {
        'device_id': 'DOCTOR-TEST-01',
        'patient_id': 'PAT-DOCTOR-01',
        'device_type': 'Doctor Monitor',
        'battery_level': 75,
        'signal_strength': 88
    }
    create_resp = requests.post(f'{API_URL}/api/v1/devices', json=device_payload, headers=headers)
    print('Create device status:', create_resp.status_code)
    print('Create device body:', create_resp.text)

    devices_resp = requests.get(f'{API_URL}/api/v1/devices', headers=headers)
    print('Fetch devices status:', devices_resp.status_code)
    print('Fetch devices body:', devices_resp.text)
else:
    print('Skipping device creation because login failed.')
