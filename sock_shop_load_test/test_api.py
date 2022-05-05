import base64
import time
from datetime import datetime
from faker import Faker
import requests

host = "http://192.168.2.11:30001"
fake = Faker()
session = requests.Session()


def register(username):
    body = {
        "username": username,
        "password": username,
        "email": fake.email()
    }

    response = session.post(url=host + "/register", json=body)
    if response.status_code == 200:
        res_json = response.json()
        user_id = res_json["id"]
        address_id = add_address(user_id)
        card_id = add_card(user_id)
        print("user created-", user_id)
        if address_id:
            print("address-%s created for user: %s" % (address_id, user_id))
        if card_id:
            print("card-%s created for user: %s" % (card_id, user_id))
        return user_id
    if response.status_code == 500:
        return 0


def add_address(user_id):
    if user_id:
        body = {
            "street": fake.street_name(),
            "number": fake.building_number(),
            "country": fake.country(),
            "city": fake.city(),
            "postcode": fake.postcode(),
            "userID": user_id
        }
        response = session.post(url=host + "/addresses", json=body)
        res_json = response.json()
        if res_json:
            address_id = res_json["id"]
            return address_id
        else:
            return None


def add_card(user_id):
    if user_id:
        body = {
            "longNum": fake.credit_card_number(card_type=None),
            "expires": fake.credit_card_expire(),
            "ccv": fake.credit_card_security_code(card_type=None),
            "userID": user_id
        }
        response = session.post(url=host + "/cards", json=body)
        # print(response.text)
        res_json = response.json()
        if res_json:
            card_id = res_json["id"]
            return card_id
        else:
            return None


user_name = "admin"
user_cred = user_name + ":" + user_name
user_cred = user_cred.encode("ascii")
base64_bytes = base64.b64encode(user_cred)
base64string = base64_bytes.decode("ascii")

token = "Basic " + base64string
head = {"Accept": "application/json", "Content-Type": "application/json",
        "Authorization": token}
response = session.get(url=host + "/login", headers=head)

# add = add_address("57a98d98e4b00679b4a830af")
# print(add)

usernames = []
for x in range(2000):
    username = fake.user_name()
    user_id = register(username)
    if user_id == 0:
        print("User Not created")
    else:
        usernames.append(username)

print(usernames)
