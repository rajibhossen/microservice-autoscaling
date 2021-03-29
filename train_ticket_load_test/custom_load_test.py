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
import sys

total_user = 0


def setup_logger(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    handler = logging.FileHandler(os.path.join(dir_path, "load_data/" + file_name + ".log"))
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger = logging.getLogger("Requests logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("arrival_time,service,status_code,response_time,user")
    return logger


# def log_requests(to_log):
#     if logger is not None:
#         logger.info(to_log)


class Requests:

    def __init__(self, logger, uuid):
        self.host = "http://192.168.2.11:32677"
        user = random.choice(USER_CREDETIALS)
        self.user_name = user
        self.password = user
        self.trip_detail = random.choice(TRIP_DATA)
        self.food_detail = {}
        self.departure_date = random.choice(TRAVEL_DATES)
        self.logger = logger
        self.request_uuid = uuid
        # self.user_name = "fdse_microservice"
        # self.password = "111111"

    def home(self):
        arrival_time = datetime.now()
        start_time = time.time()
        response = requests.get(self.host + '/index.html')
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "home," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)

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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "search_ticket," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)

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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "login," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "start_booking," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
        # print(to_log)

    def get_assurance_types(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/api/v1/assuranceservice/assurances/types",
            headers=head)
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_assurance_types," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_foods," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "select_contact," + str(response_contacts.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "finish_booking," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "select_order," + str(response_order_refresh.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
        # print(to_log)

        response_as_json = response_order_refresh.json()["data"]
        if response_as_json:
            self.order_id = response_as_json[0]["id"]  # first order with paid or not paid
            self.paid_order_id = response_as_json[0]["id"]  # default first order with paid or unpaid.
            self.order_trip_id = response_as_json[0]["trainNumber"]
        else:
            self.order_id = "sdasdasd"  # no orders, set a random number
            self.paid_order_id = "asdasdasn"
            self.order_trip_id = "d1234"
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "pay," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
        # print(response.text)

    # cancelNoRefund

    def cancel_with_no_refund(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id,
            headers=head)
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "cancel_with_no_refund," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_voucher," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_consigns," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "search_ticket," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
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
            response_as_json_collect_ticket.status_code) + "," + str(response_time) + "," + self.request_uuid
        self.logger.info(to_log)
        # print(to_log)

    def enter_station(self):
        arrival_time = datetime.now()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()

        response = requests.get(
            url=self.host + "/api/v1/executeservice/execute/execute/" + self.paid_order_id,
            headers=head)
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "enter_station," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid
        self.logger.info(to_log)
        # print(to_log)

    def perform_task(self, name):
        task = getattr(self, name)
        task()


def user_tasks(logger, uuid):
    global total_user
    total_user += 1
    collect_tasks = ["home", "login", "select_order", "pay", "collect_ticket", ]
    search_tasks = ["search_ticket"]
    booking_tasks = ["login", "search_ticket", "start_booking", "get_assurance_types", "get_foods",
                     "select_contact", "finish_booking"]
    consign_tasks = ["login", "select_contact", "finish_booking", "select_order", "get_consigns",
                     "confirm_consign"]
    pay_tasks = ["home", "login", "select_contact", "finish_booking", "select_order", "pay"]
    tasks = random.choice([search_tasks, booking_tasks, consign_tasks])
    # print("Tasks - ", tasks)
    # uuid = shortuuid.uuid()
    req_obj = Requests(logger, uuid)
    for task in tasks:
        req_obj.perform_task(task)


def start_load_test(logger, lambd, runtime):
    end_time = time.time() + runtime
    while time.time() < end_time:
        # gevent.spawn(user_tasks, logger, str(total_user))
        thread = threading.Thread(target=user_tasks, args=(logger, str(total_user)))
        thread.start()
        next_arrival = random.expovariate(1 / lambd)
        time.sleep(next_arrival / 1000.0)
        # print(next_arrival)

    main_thread = threading.current_thread()
    for x in threading.enumerate():
        if x is main_thread:
            continue
        x.join()


if __name__ == '__main__':
    arrival_rate = int(sys.argv[1])
    runtime = int(sys.argv[2])
    file_name = sys.argv[3]
    logger = setup_logger(file_name)
    start_time = time.time()
    print("Start Testing with arrival rate - %s ms, runtime--%s s at %s" % (arrival_rate, runtime, datetime.now()))

    start_load_test(logger, arrival_rate, runtime)

    print("Finish Testing at %s, Total User Spawned - %s" % (datetime.now(), total_user))
    print("Elapsed Time: ", time.time() - start_time)
