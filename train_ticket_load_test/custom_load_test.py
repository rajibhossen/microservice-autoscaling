import asyncio
import json
import logging
import os
import random
import string
import time
import threading
import requests
from datetime import datetime
from test_data import USER_CREDETIALS, TRIP_DATA, TRAVEL_DATES

dir_path = os.path.dirname(os.path.realpath(__file__))
handler = logging.FileHandler(os.path.join(dir_path, "logs/temp.log"))
handler.setFormatter(logging.Formatter('%(message)s'))
logger = logging.getLogger("Requests logger")
logger.setLevel(logging.INFO)

logger.addHandler(handler)


def log_requests(to_log):
    if logger is not None:
        logger.info(to_log)


log_requests("arrival_time,service,status_code,response_time")


class Requests:

    def __init__(self):
        self.host = "http://192.168.2.11:32677"
        user = random.choice(USER_CREDETIALS)
        self.user_name = user
        self.password = user
        self.trip_detail = random.choice(TRIP_DATA)
        self.food_detail = {}
        self.departure_date = random.choice(TRAVEL_DATES)
        # self.user_name = "fdse_microservice"
        # self.password = "111111"

    def home(self):
        arrival_time = datetime.now()
        start_time = time.time()
        response = requests.get(self.host + '/index.html')
        response_time = time.time() - start_time
        # to_log = {'name': "home", 'status_code': response.status_code,
        #           'response_time': response_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "home," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)

    def search_ticket(self):
        arrival_time = datetime.now()
        stations = ["Shang Hai", "Tai Yuan", "Nan Jing", "Wu Xi", "Su Zhou", "Shang Hai Hong Qiao", "Bei Jing",
                    "Shi Jia Zhuang", "Xu Zhou", "Ji Nan", "Hang Zhou", "Jia Xing Nan", "Zhen Jiang"]
        from_station, to_station = random.sample(stations, 2)
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        body_start = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date
        }
        start_time = time.time()
        response = requests.post(
            url=self.host + "/api/v1/travelservice/trips/left",
            headers=head,
            json=body_start)
        if not response.json()["data"]:
            response = requests.post(
                url=self.host + "/api/v1/travel2service/trips/left",
                headers=head,
                json=body_start)
        # to_log = {'name': "search_ticket", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "search_ticket," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)

    def login(self):
        start_time = time.time()
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}

        response = requests.post(url=self.host + "/api/v1/users/login",
                                 headers=head,
                                 json={
                                     "username": self.user_name,
                                     "password": self.password
                                 })
        # to_log = {'name': "login", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "login," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

        response_as_json = response.json()["data"]
        if response_as_json is not None:
            token = response_as_json["token"]
            self.bearer = "Bearer " + token
            self.user_id = response_as_json["userId"]

    # purchase ticket

    def start_booking(self):
        arrival_time = datetime.now()
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/client_ticket_book.html?tripId=" + self.trip_detail["trip_id"] + "&from=" +
                self.trip_detail[
                    "from"] +
                "&to=" + self.trip_detail["to"] + "&seatType=" + self.trip_detail["seat_type"] + "&seat_price=" +
                self.trip_detail["seat_price"] +
                "&date=" + departure_date,
            headers=head)
        # to_log = {'name': "start_booking", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "start_booking," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def get_assurance_types(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/api/v1/assuranceservice/assurances/types",
            headers=head)
        # to_log = {'name': "get_assurance_types", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_assurance_types," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def get_foods(self):
        arrival_time = datetime.now()
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/api/v1/foodservice/foods/" + departure_date + "/" + self.trip_detail["from"] + "/" +
                self.trip_detail["to"] + "/" + self.trip_detail["trip_id"],
            headers=head)
        # to_log = {'name': "get_foods", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_foods," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def select_contact(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response_contacts = requests.get(
            url=self.host + "/api/v1/contactservice/contacts/account/" + self.user_id,
            headers=head)

        response_as_json_contacts = response_contacts.json()["data"]

        if len(response_as_json_contacts) == 0:
            response_contacts = requests.post(
                url=self.host + "/api/v1/contactservice/contacts",
                headers=head,
                json={
                    "name": self.user_id, "accountId": self.user_id, "documentType": "1",
                    "documentNumber": self.user_id, "phoneNumber": "123456"})

            response_as_json_contacts = response_contacts.json()["data"]
            self.contactid = response_as_json_contacts["id"]
        else:
            self.contactid = response_as_json_contacts[0]["id"]

        # to_log = {'name': "select_contact", 'status_code': response_contacts.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "select_contact," + str(response_contacts.status_code) + "," + str(
            response_time)
        log_requests(to_log)
        # print(to_log)

    def finish_booking(self):
        arrival_time = datetime.now()
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}

        body_for_reservation = {
            "accountId": self.user_id,
            "contactsId": self.contactid,
            "tripId": self.trip_detail["trip_id"],
            "seatType": self.trip_detail["seat_type"],
            "date": departure_date,
            "from": self.trip_detail["from"],
            "to": self.trip_detail["to"],
            "assurance": random.choice(["0", "1"]),
            "foodType": 1,
            "foodName": "Bone Soup",
            "foodPrice": 2.5,
            "stationName": "",
            "storeName": ""
        }
        if self.food_detail:
            body_for_reservation["foodType"] = self.food_detail["foodType"]
            body_for_reservation["foodName"] = self.food_detail["foodName"]
            body_for_reservation["foodPrice"] = self.food_detail["foodPrice"]
        start_time = time.time()
        response = requests.post(
            url=self.host + "/api/v1/preserveservice/preserve",
            headers=head,
            json=body_for_reservation)
        # to_log = {'name': "finish_booking", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "finish_booking," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def select_order(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response_order_refresh = requests.post(
            url=self.host + "/api/v1/orderservice/order/refresh",
            headers=head,
            json={
                "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false",
                "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null",
                "boughtDateStart": "null", "boughtDateEnd": "null"})

        # to_log = {'name': "select_order", 'status_code': response_order_refresh.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "select_order," + str(response_order_refresh.status_code) + "," + str(
            response_time)
        log_requests(to_log)
        # print(to_log)

        response_as_json = response_order_refresh.json()["data"]
        if response_as_json:
            self.order_id = response_as_json[0]["id"]  # first order with paid or not paid
            self.paid_order_id = response_as_json[0]["id"]  # default first order with paid or unpaid.
        else:
            self.order_id = "sdasdasd"  # no orders, set a random number
            self.paid_order_id = "asdasdasn"
        # selecting order with payment status - not paid.
        for orders in response_as_json:
            if orders["status"] == 0:
                self.order_id = orders["id"]
                self.order_trip_id = orders["trainNumber"]
                break
        for orders in response_as_json:
            if orders["status"] == 1:
                self.paid_order_id = orders["id"]
                break

    def pay(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        if not self.order_id:
            return
        response = requests.post(
            url=self.host + "/api/v1/inside_pay_service/inside_payment",
            headers=head,
            json={"orderId": self.order_id, "tripId": self.order_trip_id})
        # to_log = {'name': "pay", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "pay," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        print(response.text)

    # cancelNoRefund

    def cancel_with_no_refund(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id,
            headers=head)
        # to_log = {'name': "cancel_no_refund", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "cancel_with_no_refund," + str(response.status_code) + "," + str(
            response_time)
        log_requests(to_log)
        # print(to_log)

    # user refund with voucher

    def get_voucher(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.post(
            url=self.host + "/getVoucher",
            headers=head,
            json={"orderId": self.order_id, "type": 1})
        # to_log = {'name': "get_voucher", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_voucher," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    # consign ticket

    def get_consigns(self):
        arrival_time = datetime.now()
        start_time = time.time()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        response = requests.get(
            url=self.host + "/api/v1/consignservice/consigns/order/" + self.order_id,
            headers=head)
        # to_log = {'name': "get_consigns", 'status_code': response.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_consigns," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def confirm_consign(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.put(
            url=self.host + "/api/v1/consignservice/consigns",
            json={
                "accountId": self.user_id,
                "handleDate": self.departure_date,
                "from": self.trip_detail["from"],
                "to": self.trip_detail["to"],
                "orderId": self.order_id,
                "consignee": self.order_id,
                "phone": ''.join([random.choice(string.digits) for n in range(8)]),
                "weight": "1",
                "id": "",
                "isWithin": "false"},
            headers=head)
        # to_log = {'name': "confirm_consign", 'status_code': response_as_json_consign.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "search_ticket," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def collect_ticket(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response_as_json_collect_ticket = requests.get(
            url=self.host + "/api/v1/executeservice/execute/collected/" + self.paid_order_id,
            headers=head)
        # to_log = {'name': "collect_ticket",
        #           'status_code': response_as_json_collect_ticket.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "collect_ticket," + str(
            response_as_json_collect_ticket.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def enter_station(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()

        response = requests.get(
            url=self.host + "/api/v1/executeservice/execute/execute/" + self.paid_order_id,
            headers=head)
        # to_log = {'name': "enter_station",
        #           'status_code': response_as_json_enter_station.status_code,
        #           'response_time': time.time() - start_time}
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "enter_station," + str(response.status_code) + "," + str(response_time)
        log_requests(to_log)
        # print(to_log)

    def perform_task(self, name):
        # name_without_suffix = name.replace("_expected", "").replace("_unexpected", "")
        task = getattr(self, name)
        task()


def user_tasks():
    collect_tasks = ["home", "login", "select_order", "pay", "collect_ticket", ]
    search_tasks = ["home", "search_ticket"]
    booking_tasks = ["home", "login", "search_ticket", "start_booking", "get_assurance_types", "get_foods",
                     "select_contact", "finish_booking"]
    consign_tasks = ["home", "login", "select_contact", "finish_booking", "select_order", "get_consigns",
                     "confirm_consign"]
    pay_tasks = ["home", "login", "select_contact", "finish_booking", "select_order", "pay"]
    #tasks = random.choice([search_tasks, booking_tasks, consign_tasks, pay_tasks, collect_tasks])
    tasks = pay_tasks
    #print("Tasks - ", tasks)
    req_obj = Requests()
    for task in tasks:
        req_obj.perform_task(task)


def start_load_test():
    start_time = time.time()
    end_time = time.time() + 180
    while time.time() < end_time:
        thread = threading.Thread(target=user_tasks)
        thread.start()
        next_arrival = random.expovariate(1 / 20)
        time.sleep(next_arrival / 1000.0)

    main_thread = threading.current_thread()
    for x in threading.enumerate():
        if x is main_thread:
            continue
        x.join()
    print("Finish Testing")
    print("Elapsed Time: ", time.time() - start_time)


start_load_test()
