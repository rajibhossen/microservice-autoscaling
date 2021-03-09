import json
import sys
import time

import numpy as np
import random
import requests

username = "fdse_microservice"
password = "111111"
bearer = ""
user_id = ""
host = "http://192.168.2.11:32677"
contactid = ""
orderid = ""


def matrix_checker(matrix):
    # print(matrix)
    sum = np.sum(matrix, axis=1).tolist()
    return sum[1:] == sum[:-1]


def sequence_generator(matrix, all_functions):
    if not (matrix_checker(matrix)):
        raise Exception("Matrix is not correct")

    max_sequence_len = 20
    current_node = 0
    i = 0

    array = [all_functions[0]]
    # print(array)
    while i < max_sequence_len:
        if 1 in matrix[current_node] and matrix[current_node].tolist().index(1) == current_node:
            break
        print(matrix[current_node])
        selection = random.choices(population=all_functions, weights=matrix[current_node])[0]
        # print(selection)
        array.append(selection)

        current_node = all_functions.index(selection)

        i += 1
    return array


def matrix():
    all_functions = [
        "home_expected",
        "login_expected",
        "login_unexpected",
        "search_departure_expected",
        "search_departure_unexpected",
        "start_booking_expected",
        "get_assurance_types_expected",
        "get_foods_expected",
        "select_contact_expected",
        "finish_booking_expected",
        "finish_booking_unexpected",
        "select_order_expected",
        "pay_expected",
        "pay_unexpected",
    ]
    matrix = np.zeros((len(all_functions), len(all_functions)))

    matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.9
    matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.1

    matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.02
    matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.98

    matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.8  # 0.8
    matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.2  # 0.2

    matrix[
        all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_expected")] = 0.95
    matrix[all_functions.index("search_departure_unexpected"), all_functions.index(
        "search_departure_unexpected")] = 0.05

    matrix[all_functions.index("search_departure_expected"), all_functions.index("start_booking_expected")] = 1

    matrix[all_functions.index("start_booking_expected"), all_functions.index("get_assurance_types_expected")] = 1

    matrix[all_functions.index("get_assurance_types_expected"), all_functions.index("get_foods_expected")] = 1

    matrix[all_functions.index("get_foods_expected"), all_functions.index("select_contact_expected")] = 1

    matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_expected")] = 0.8

    matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_unexpected")] = 0.2

    matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_expected")] = 0.95
    matrix[
        all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_unexpected")] = 0.05

    matrix[all_functions.index("finish_booking_expected"), all_functions.index("select_order_expected")] = 1

    matrix[all_functions.index("select_order_expected"), all_functions.index("pay_expected")] = 0.8
    matrix[all_functions.index("select_order_expected"), all_functions.index("pay_unexpected")] = 0.2

    matrix[all_functions.index("pay_expected"), all_functions.index("pay_expected")] = 1

    matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.95

    matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.05

    task_sequence = sequence_generator(matrix, all_functions)

    print(task_sequence)


def login():
    global bearer
    global user_id
    start_time = time.time()
    head = {"Accept": "application/json",
            "Content-Type": "application/json"}
    response = requests.post(url=host + "/api/v1/users/login",
                             headers=head,
                             json={
                                 "username": username,
                                 "password": password})
    print(response.text)
    response_as_json = response.json()["data"]
    if response_as_json is not None:
        token = response_as_json["token"]
        bearer = "Bearer " + token
        user_id = response_as_json["userId"]


def search_ticket(departure_date, from_station, to_station, expected=True):
    head = {"Accept": "application/json",
            "Content-Type": "application/json"}
    body_start = {
        "startingPlace": from_station,
        "endPlace": to_station,
        "departureTime": departure_date
    }

    start_time = time.time()
    response = requests.post(
        url=host + "/api/v1/travelservice/trips/left",
        headers=head,
        json=body_start)
    response_time = time.time() - start_time
    print(json.dumps(response.json()))


def start_booking(from_station, expected=True):
    departure_date = "2021-04-21"
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    start_time = time.time()
    response = requests.get(
        url=host + "/client_ticket_book.html?tripId=D1345&from=" + from_station + "&to=Su%20Zhou&seatType=2&seat_price=50.0"
                                                                                  "&date=" + departure_date,
        headers=head)
    print(response)


def select_contact(expected=True):
    global contactid
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    response_contacts = requests.get(
        url=host + "/api/v1/contactservice/contacts/account/" + user_id,
        headers=head)

    response_as_json_contacts = response_contacts.json()["data"]
    print(json.dumps(response_as_json_contacts))
    if len(response_as_json_contacts) == 0:
        response_contacts = requests.post(
            url=host + "/api/v1/contactservice/contacts",
            headers=head,
            json={
                "name": user_id, "accountId": user_id, "documentType": "1",
                "documentNumber": user_id, "phoneNumber": "123456"})

        response_as_json_contacts = response_contacts.json()["data"]
        # print(response_as_json_contacts)
        contactid = response_as_json_contacts["id"]
    else:
        contactid = response_as_json_contacts[0]["id"]

    print(contactid)


def finish_booking():
    departure_date = dep
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    body_for_reservation = {
        "accountId": user_id,
        "contactsId": contactid,
        "tripId": "D1345",
        "seatType": "2",
        "date": departure_date,
        "from": "Shang Hai",
        "to": "Su Zhou",
        "assurance": "0",
        "foodType": 1,
        "foodName": "Bone Soup",
        "foodPrice": 2.5,
        "stationName": "",
        "storeName": ""
    }
    start_time = time.time()
    response = requests.post(
        url=host + "/api/v1/preserveservice/preserve",
        headers=head,
        json=body_for_reservation)
    print(response.text)
    print(response.status_code)


def select_order(expected):
    global orderid
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    start_time = time.time()
    response_order_refresh = requests.post(
        url=host + "/api/v1/orderservice/order/refresh",
        headers=head,
        json={
            "loginId": user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false",
            "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null",
            "boughtDateStart": "null", "boughtDateEnd": "null"})

    response_as_json = response_order_refresh.json()["data"]
    #print(json.dumps(response_order_refresh.json()))
    for orders in response_as_json:
        if orders["status"] == 1:
            orderid = orders["id"]


def pay():
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    start_time = time.time()
    response = requests.post(
        url=host + "/api/v1/inside_pay_service/inside_payment",
        headers=head,
        json={"orderId": orderid, "tripId": "D1345"})
    print(response.text)


def collect_ticket():
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    start_time = time.time()
    collect_ticket = requests.get(
        url=host+"/api/v1/executeservice/execute/collected/" + orderid,
        headers=head)
    print(collect_ticket.text)


def enter_station():
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    start_time = time.time()
    enter_station =requests.get(
        url=host+"/api/v1/executeservice/execute/execute/" + orderid,
        headers=head)
    print(enter_station.text)

def api_test():
    head = {"Accept": "application/json",
            "Content-Type": "application/json", "Authorization": bearer}
    response = requests.get(
        url=host + "/api/v1/foodservice/orders",
        headers=head)
    print(response.text)
    print(response.status_code)


if __name__ == '__main__':
    dep = "2021-04-21"
    from_station = "Nan Jing"
    # to_station = "Shang Hai"
    start_time = time.time()
    login()
    select_order("True")
    collect_ticket()
    #pay("True")
    # search_ticket(dep, from_station, to_station)
    # start_booking(from_station)
    # select_contact()
    # finish_booking()
    # api_test()
    # matrix()
    # name_without_suffix = "login_expected".replace("_expected", "").replace("_unexpected", "")
    # print(name_without_suffix)

    total_time = time.time() - start_time
    print("Total Response time: ", total_time)
    # matrix()
