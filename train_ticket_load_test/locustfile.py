import json
import logging
import math
import os
import random
import string
import sys
import time
from datetime import date
from random import randint

import numpy as np
from locust import task, constant, HttpUser, between
from locust.event import EventHook
from locust import LoadTestShape, events
from requests.adapters import HTTPAdapter

DEP_DATE = "2021-04-23"
VERBOSE_LOGGING = 0  # ${LOCUST_VERBOSE_LOGGING}
# stat_file = open("output/full_stats.csv", "w")
# user_file = open("output/user_counts.csv", "w")


def random_string_generator():
    len = randint(8, 16)
    prob = randint(0, 100)
    if prob < 25:
        random_string = ''.join([random.choice(string.ascii_letters) for n in range(len)])
    elif prob < 50:
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(len)])
    elif prob < 75:
        random_string = ''.join(
            [random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(len)])
    else:
        random_string = ''
    return random_string


def random_date_generator():
    temp = randint(0, 4)
    random_y = 2000 + temp * 10 + randint(0, 9)
    random_m = randint(1, 12)
    random_d = randint(1, 31)  # assumendo che la data possa essere non sensata (e.g. 30 Febbraio)
    return str(random_y) + '-' + str(random_m) + '-' + str(random_d)


def postfix(expected=True):
    if expected:
        return '_expected'
    return '_unexpected'


class Requests:

    def __init__(self, client):
        self.client = client
        dir_path = os.path.dirname(os.path.realpath(__file__))
        handler = logging.FileHandler(os.path.join(dir_path, "locustfile_debug.log"))
        # handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

        # self.user_name = "fdse_microservice"
        # self.password = "111111"
        self.user_name = "rajib_hossen"
        self.password = "rajibhossen"

        if VERBOSE_LOGGING == 1:
            logger = logging.getLogger("Debugging logger")
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            self.debugging_logger = logger
        else:
            self.debugging_logger = None

    def log_verbose(self, to_log):
        if self.debugging_logger is not None:
            self.debugging_logger.debug(json.dumps(to_log))

    def home(self, expected):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get('/index.html', name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time}
            self.log_verbose(to_log)

    def try_to_read_response_as_json(self, response):
        try:
            return response.json()
        except:
            try:
                return response.content.decode('utf-8')
            except:
                return response.content

    def search_ticket(self, departure_date, from_station, to_station, expected=True):
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        body_start = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date
        }

        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.post(
                url="/api/v1/travelservice/trips/left",
                headers=head,
                json=body_start,
                catch_response=True,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def search_departure(self, expected):
        if expected:
            self.search_ticket(date.today().strftime(random_date_generator()), "Shang Hai", "Su Zhou", expected)
        else:
            self.search_ticket(date.today().strftime(random_date_generator()), random_string_generator(), "Su Zhou",
                               expected)

    def search_return(self, expected):
        if expected:
            self.search_ticket(date.today().strftime(random_date_generator()), "Su Zhou", "Shang Hai", expected)
        else:
            self.search_ticket(date.today().strftime(random_date_generator()), random_string_generator(), "Shang Hai",
                               expected)

    def _create_user(self, expected):

        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        document_num = random.randint(1, 5)  # added by me
        with self.client.post(url="/api/v1/adminuserservice/users",
                              headers={
                                  "Authorization": self.bearer, "Accept": "application/json",
                                  "Content-Type": "application/json"},
                              json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0,
                                    "password": self.user_name, "userName": self.user_name},
                              name=req_label) as response2:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response2.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response2)}
            self.log_verbose(to_log)

    def _navigate_to_client_login(self, expected=True):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get('/client_login.html', name=req_label) as response:
            to_log = {'name': req_label, 'expected': True, 'status_code': response.status_code,
                      'response_time': time.time() - start_time}
            self.log_verbose(to_log)

    def login(self, expected):
        # self._create_user(True)

        # self._navigate_to_client_login()
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        if (expected):
            response = self.client.post(url="/api/v1/users/login",
                                        headers=head,
                                        json={
                                            "username": self.user_name,
                                            "password": self.password
                                        }, name=req_label)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)
        else:
            response = self.client.post(url="/api/v1/users/login",
                                        headers=head,
                                        json={
                                            "username": self.user_name,
                                            # wrong password
                                            "password": random_string_generator()
                                        }, name=req_label)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

        response_as_json = response.json()["data"]
        if response_as_json is not None:
            token = response_as_json["token"]
            self.bearer = "Bearer " + token
            self.user_id = response_as_json["userId"]

    # purchase ticket

    def start_booking(self, expected):
        departure_date = DEP_DATE
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get(
                url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0"
                    "&date=" + departure_date,
                headers=head,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time}
            self.log_verbose(to_log)

    def get_assurance_types(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get(
                url="/api/v1/assuranceservice/assurances/types",
                headers=head,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def get_foods(self, expected):
        departure_date = DEP_DATE
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get(
                url="/api/v1/foodservice/foods/" + departure_date + "/Shang%20Hai/Su%20Zhou/D1345",
                headers=head,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def select_contact(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        response_contacts = self.client.get(
            url="/api/v1/contactservice/contacts/account/" + self.user_id,
            headers=head,
            name=req_label)
        to_log = {'name': req_label, 'expected': expected, 'status_code': response_contacts.status_code,
                  'response_time': time.time() - start_time,
                  'response': self.try_to_read_response_as_json(response_contacts)}
        self.log_verbose(to_log)

        response_as_json_contacts = response_contacts.json()["data"]

        if len(response_as_json_contacts) == 0:
            req_label = 'set_new_contact' + postfix(expected)
            response_contacts = self.client.post(
                url="/api/v1/contactservice/contacts",
                headers=head,
                json={
                    "name": self.user_id, "accountId": self.user_id, "documentType": "1",
                    "documentNumber": self.user_id, "phoneNumber": "123456"},
                name=req_label)

            response_as_json_contacts = response_contacts.json()["data"]
            self.contactid = response_as_json_contacts["id"]
        else:
            self.contactid = response_as_json_contacts[0]["id"]

    def finish_booking(self, expected):
        departure_date = DEP_DATE
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        if (expected):
            body_for_reservation = {
                "accountId": self.user_id,
                "contactsId": self.contactid,
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
        else:
            body_for_reservation = {
                "accountId": self.user_id,
                "contactsId": self.contactid,
                "tripId": random_string_generator(),
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
        with self.client.post(
                url="/api/v1/preserveservice/preserve",
                headers=head,
                json=body_for_reservation,
                catch_response=True,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def select_order(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        response_order_refresh = self.client.post(
            url="/api/v1/orderservice/order/refresh",
            name=req_label,
            headers=head,
            json={
                "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false",
                "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null",
                "boughtDateStart": "null", "boughtDateEnd": "null"})

        to_log = {'name': req_label, 'expected': expected, 'status_code': response_order_refresh.status_code,
                  'response_time': time.time() - start_time,
                  'response': self.try_to_read_response_as_json(response_order_refresh)}
        self.log_verbose(to_log)

        response_as_json = response_order_refresh.json()["data"]
        self.order_id = response_as_json[0]["id"]  # first order with paid or not paid
        # selecting order with payment status - not paid.
        for orders in response_as_json:
            if orders["status"] == 0:
                self.order_id = orders["id"]

    def pay(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            with self.client.post(
                    url="/api/v1/inside_pay_service/inside_payment",
                    headers=head,
                    json={"orderId": self.order_id, "tripId": "D1345"},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)
        else:
            with self.client.post(
                    url="/api/v1/inside_pay_service/inside_payment",
                    headers=head,
                    json={"orderId": random_string_generator(), "tripId": "D1345"},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

    # cancelNoRefund

    def cancel_with_no_refund(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            with self.client.get(
                    url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id,
                    headers=head,
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

        else:
            with self.client.get(
                    url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + random_string_generator(),
                    headers=head,
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

    # user refund with voucher

    def get_voucher(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            with self.client.post(
                    url="/getVoucher",
                    headers=head,
                    json={"orderId": self.order_id, "type": 1},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

        else:
            with self.client.post(
                    url="/getVoucher",
                    headers=head,
                    json={"orderId": random_string_generator(), "type": 1},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time}
                self.log_verbose(to_log)

    # consign ticket

    def get_consigns(self, expected):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        with self.client.get(
                url="/api/v1/consignservice/consigns/order/" + self.order_id,
                headers=head,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def confirm_consign(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            response_as_json_consign = self.client.put(
                url="/api/v1/consignservice/consigns",
                name=req_label,
                json={
                    "accountId": self.user_id,
                    "handleDate": DEP_DATE,
                    "from": "Shang Hai",
                    "to": "Su Zhou",
                    "orderId": self.order_id,
                    "consignee": self.order_id,
                    "phone": "123",
                    "weight": "1",
                    "id": "",
                    "isWithin": "false"},
                headers=head)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response_as_json_consign.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_consign)}
            self.log_verbose(to_log)
        else:
            response_as_json_consign = self.client.put(
                url="/api/v1/consignservice/consigns",
                name=req_label,
                json={
                    "accountId": self.user_id,
                    "handleDate": DEP_DATE,
                    "from": "Shang Hai",
                    "to": "Su Zhou",
                    "orderId": self.order_id,
                    "consignee": random_string_generator(),
                    "phone": random_string_generator(),
                    "weight": "1",
                    "id": "",
                    "isWithin": "false"}, headers=head)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response_as_json_consign.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_consign)}
            self.log_verbose(to_log)

    def collect_ticket(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if expected:
            response_as_json_collect_ticket = self.client.get(
                url="/api/v1/executeservice/execute/collected/" + self.order_id,
                name=req_label,
                headers=head)
            to_log = {'name': req_label, 'expected': expected,
                      'status_code': response_as_json_collect_ticket.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_collect_ticket)}
            self.log_verbose(to_log)

    def enter_station(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if expected:
            response_as_json_enter_station = self.client.get(
                url="/api/v1/executeservice/execute/execute/" + self.order_id,
                name=req_label,
                headers=head)
            to_log = {'name': req_label, 'expected': expected,
                      'status_code': response_as_json_enter_station.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_enter_station)}
            self.log_verbose(to_log)

    def perform_task(self, name):
        name_without_suffix = name.replace("_expected", "").replace("_unexpected", "")
        task = getattr(self, name_without_suffix)
        task(name.endswith('_expected'))


class UserOnlyLogin(HttpUser):
    weight = 1
    # wait_function = random.expovariate(1) * 1000
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

    @task()
    def perform_task(self):
        logging.debug("User home -> login")
        request = Requests(self.client)
        tasks_sequence = ["login_expected"]
        for tasks in tasks_sequence:
            request.perform_task(tasks)


class UserNoLogin(HttpUser):
    weight = 1
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def perfom_task(self):
        logging.debug("Running user 'only search'...")

        task_sequence = ["home_expected", "search_departure_expected"]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)


class UserBooking(HttpUser):
    weight = 1
    # wait_function = random.expovariate(1)
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):
        logging.debug("Running user 'booking'...")

        task_sequence = ["home_expected", "login_expected", "search_departure_expected", "start_booking_expected",
                         "get_assurance_types_expected", "get_foods_expected", "select_contact_expected",
                         "finish_booking_expected"]
        # task_sequence = ["login_expected", "select_contact_expected", "finish_booking_expected"]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)


class UserPay(HttpUser):
    weight = 1
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):
        logging.debug("Running user 'booking'...")

        task_sequence = ["home_expected", "login_expected",
                         "select_contact_expected",
                         "finish_booking_expected",
                         "select_order_expected",
                         "pay_expected"]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)


class UserConsignTicket(HttpUser):
    weight = 1
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):
        logging.debug("Running user 'consign ticket'...")
        task_sequence = [
            "home_expected",
            "login_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "select_order_expected",
            "get_consigns_expected",
            "confirm_consign_expected",
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)


class UserCancelNoRefund(HttpUser):
    weight = 1
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):
        logging.debug("Running user 'cancel no refund'...")

        task_sequence = [
            "home_expected",
            "login_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "select_order_expected",
            "cancel_with_no_refund_expected",
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)


class UserRefundVoucher(HttpUser):
    weight = 1
    wait_time = constant(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):
        logging.debug("Running user 'refound voucher'...")

        task_sequence = [
            "home_expected",
            "login_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "select_order_expected",
            "get_voucher_expected",
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)


# @events.request_success.add_listener
# def hook_request_success(request_type, name, response_time, response_length, **kwargs):
#     stat_file.write(request_type + "," + name + "," + str(response_time) + "," + str(response_length) + "\n")
#
#
# @events.quitting.add_listener
# def hook_quitting(environment, **kw):
#     stat_file.close()

# class DoubleWaveShape(LoadTestShape):
#     min_users = 150
#     peak_one_users = 300
#     peak_two_users = 220
#     time_limit = 600
#
#     def tick(self):
#         run_time = round(self.get_run_time())
#
#         if run_time < self.time_limit:
#             user_count = (
#                     (self.peak_one_users - self.min_users) * math.e ** -(
#                     ((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
#                     + (self.peak_two_users - self.min_users) * math.e ** -(
#                     ((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
#                     + self.min_users
#             )
#             return round(user_count), round(user_count)
#         else:
#             return None

# class StepLoadShape(LoadTestShape):
#     """
#     A step load shape
#     Keyword arguments:
#         step_time -- Time between steps
#         step_load -- User increase amount at each step
#         spawn_rate -- Users to stop/start per second at every step
#         time_limit -- Time limit in seconds
#     """
#
#     step_time = 90
#     step_load = 50
#     spawn_rate = 10
#     time_limit = 600
#
#     def tick(self):
#         run_time = self.get_run_time()
#
#         if run_time > self.time_limit:
#             return None
#
#         current_step = math.floor(run_time / self.step_time) + 1
#         return current_step * self.step_load, self.spawn_rate