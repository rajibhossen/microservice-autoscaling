import requests

base_url = "http://192.168.2.11:32677/"
login_url = base_url + "api/v1/users/login"
verify_url = base_url + "api/v1/verifycode/generate"
search_url = base_url + "api/v1/travel2service/trips/"
user_login = {"username": "fdse_microservice", "password": "111111"}
search_data = {"startingPlace": "Shang Hai", "endPlace": "Su Zhou", "departureTime": "2021-01-28"}
headers = {'Content-Type': 'application/json'}
login = requests.post(url=login_url, data=user_login, headers=headers)
print(login.status_code)
print(login.text)
