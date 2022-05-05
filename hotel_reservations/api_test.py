import random
import requests

host = "http://192.168.2.11:30500"


def get_user():
    id = random.randint(0, 500)
    user_name = "Cornell_" + str(id)
    password = ""
    for x in range(10):
        password += str(id)

    return user_name, password


def reserve():
    in_date = random.randint(9, 23)
    out_date = in_date + random.randint(1, 5)

    in_date_str = str(in_date)
    if in_date <= 9:
        in_date_str = "2015-04-0" + in_date_str
    else:
        in_date_str = "2015-04-" + in_date_str

    out_date_str = str(out_date)
    if out_date <= 9:
        out_date_str = "2015-04-0" + out_date_str
    else:
        out_date_str = "2015-04-" + out_date_str

    hotel_id = str(random.randint(1, 80))
    user_id, password = get_user()
    cust_name = user_id

    num_rooms = "1"

    lattitude = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
    longitude = -122.095 + (random.randint(0, 325) - 325) / 1000.0

    path = "/reservation"
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = {}
    body = {"inDate": in_date_str, "outDate": out_date_str, "lat": str(lattitude), "lon": str(longitude),
            "hotelId": hotel_id, "customerName": cust_name, "username": user_id, "password": password,
            "number": num_rooms}

    response = requests.post(url=host + path, params=body, headers=headers)
    print(response.url)
    print(response.status_code)
    print(response.text)


def search_hotel():
    in_date = random.randint(9, 23)
    out_date = random.randint(in_date + 1, 24)
    in_date_str = str(in_date)
    if in_date <= 9:
        in_date_str = "2015-04-0" + in_date_str
    else:
        in_date_str = "2015-04-" + in_date_str

    out_date_str = str(out_date)
    if out_date <= 9:
        out_date_str = "2015-04-0" + out_date_str
    else:
        out_date_str = "2015-04-" + out_date_str

    lattitude = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
    longitude = -122.095 + (random.randint(0, 325) - 325) / 1000.0

    path = "/hotels"
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = {}
    body = {"inDate": in_date_str, "outDate": out_date_str, "lat": str(lattitude), "lon": str(longitude)}

    response = requests.get(url=host + path, params=body, headers=headers)
    print(response.url)
    print(response.status_code)
    print(response.text)


def recommend():
    coin = random.uniform(0, 1)
    req_param = ""
    if coin < 0.33:
        req_param = "dis"
    elif coin < 0.66:
        req_param = "rate"
    else:
        req_param = "price"

    lattitude = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
    longitude = -122.095 + (random.randint(0, 325) - 325) / 1000.0

    path = "/recommendations"
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = {}
    body = {"require": req_param, "lat": str(lattitude), "lon": str(longitude)}

    response = requests.get(url=host + path, params=body, headers=headers)
    print(response.url)
    print(response.status_code)
    print(response.text)


def login():
    username, password = get_user()

    path = "/user"
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = {}
    body = {"username": username, "password": password}

    response = requests.get(url=host + path, params=body, headers=headers)
    print(response.url)
    print(response.status_code)
    print(response.text)


# reserve()
search_hotel()
# recommend()
# login()
