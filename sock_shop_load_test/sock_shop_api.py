import base64
import json
import logging
import os
import random
import string
import sys
import threading
import time
from datetime import datetime
from random import randint, choice
import requests

from faker import Faker

from sock_shop_load_test.users import USER_CREDENTIALS

total_user = 0
items = ['03fef6ac-1896-4ce8-bd69-b798f85c6e0b', '3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38',
         '819e1fbf-8b7e-4f6d-811f-693534916a8b', '837ab141-399e-4c1f-9abc-bace40296bac', 'a0a4f044-b040-410d-8ead-4de0446aec7e', 'd3588630-ad8e-49df-bbd7-3167f7efb246',
         'zzz4f044-b040-410d-8ead-4de0446aec7e']
faker = Faker()
random.seed(500)


def setup_logger(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    handler = logging.FileHandler(os.path.join(dir_path, "load_data/improved_algo/" + file_name + ".log"))
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger = logging.getLogger("Requests logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("arrival_time,service,status_code,response_time,user")
    return logger


class Request:
    def __init__(self, logger, uuid):
        self.host = "http://192.168.2.62:30001"
        user = choice(USER_CREDENTIALS)
        # user = ''.join(random.choices(string.ascii_letters, k=9))
        self.user_name = user
        self.password = user
        self.user_id = None
        self.choosen_item = choice(items)
        self.session = requests.Session()
        self.tags = ["brown", "geek", "formal", "blue", "skin", "red", "action", "sport", "black", "magic", "green"]
        self.card_id = None
        self.address_id = None

        self.logger = logger
        self.request_uuid = uuid

    def home(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/index.html")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "home," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def login(self):
        arrival_time = datetime.now()
        start_time = time.time()

        user_cred = self.user_name + ":" + self.password
        user_cred = user_cred.encode("ascii")
        base64_bytes = base64.b64encode(user_cred)
        base64string = base64_bytes.decode("ascii")

        token = "Basic " + base64string
        head = {"Accept": "application/json", "Content-Type": "application/json",
                "Authorization": token}

        response = self.session.get(url=self.host + "/login", headers=head)
        if response.status_code == 401:
            self.register()
            response = self.session.get(url=self.host + "/login", headers=head)
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "login," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def register(self):
        body = {
            "username": self.user_name,
            "password": self.password,
            "email": self.user_name + "@gmail.com"
        }
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.post(url=self.host + "/register", json=body)
        if response.status_code != 500:
            res_json = response.json()
            self.user_id = res_json["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "register," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def delete_user(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.delete(url=self.host + "/customers/" + self.user_id)

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "delete_user," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_all_item(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/catalogue")
        catalogue = response.json()
        if isinstance(catalogue, list):
            category_item = choice(catalogue)
            self.choosen_item = category_item["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_all_item," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def show_fixed_items(self):
        arrival_time = datetime.now()
        start_time = time.time()
        size = randint(1, 9)
        response = self.session.get(url=self.host + "/catalogue?size=" + str(size))
        catalogue = response.json()
        if isinstance(catalogue, list):
            category_item = choice(catalogue)
            self.choosen_item = category_item["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "show_fixed_items," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def scroll_items_1(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/catalogue?page=2&size=3")
        catalogue = response.json()
        if isinstance(catalogue, list):
            category_item = choice(catalogue)
            self.choosen_item = category_item["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "scroll_items_1," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def scroll_items_2(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/catalogue?page=3&size=3")
        catalogue = response.json()
        if isinstance(catalogue, list):
            category_item = choice(catalogue)
            self.choosen_item = category_item["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "scroll_items_2," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_item(self):
        arrival_time = datetime.now()
        start_time = time.time()

        if self.choosen_item:
            response = self.session.get(url=self.host + "/catalogue/" + self.choosen_item)
            response_time = time.time() - start_time
            to_log = str(arrival_time) + "," + "get_item," + str(response.status_code) + "," + str(
                response_time) + "," + self.request_uuid

            self.logger.info(to_log)

    def get_details_html(self):
        arrival_time = datetime.now()
        start_time = time.time()

        head = {"Content-Type": "html"}
        if self.choosen_item:
            response = self.session.get(url=self.host + "/detail.html?id=" + self.choosen_item, headers=head)

            response_time = time.time() - start_time
            to_log = str(arrival_time) + "," + "get_details_html," + str(response.status_code) + "," + str(
                response_time) + "," + self.request_uuid

            self.logger.info(to_log)

    def get_item_count(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/catalogue/size")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_item_count," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_category_html(self):
        arrival_time = datetime.now()
        start_time = time.time()

        head = {"Content-Type": "html"}
        response = self.session.get(url=self.host + "/category.html", headers=head)

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_category_html," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_tags(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/tags")
        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_tags," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def filter_items(self):
        arrival_time = datetime.now()
        start_time = time.time()

        tag = choice(self.tags)
        head = {"Content-Type": "html"}
        response = self.session.get(url=self.host + "/category.html?tag=" + tag, headers=head)

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "filter_items," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_related_items(self):
        arrival_time = datetime.now()
        start_time = time.time()

        tag = choice(self.tags)
        response = self.session.get(url=self.host + "/catalogue?sort=id&size=3&tags=" + tag)

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_related_items," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def add_to_cart(self):
        arrival_time = datetime.now()
        start_time = time.time()

        head = {"Content-Type": "application/json"}
        body = {
            "id": self.choosen_item,
            "quantity": 1
        }
        response = self.session.post(url=self.host + "/cart", headers=head, json=body)

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "add_to_cart," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_cart(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/cart")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_cart," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def delete_from_cart(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.delete(url=self.host + "/cart")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "delete_from_cart," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_basket(self):
        arrival_time = datetime.now()
        start_time = time.time()

        head = {"Content-Type": "application/json"}
        response = self.session.get(url=self.host + "/basket.html", headers=head)

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_basket," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_orders(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/orders")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_orders," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def checkout(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.post(url=self.host + "/orders")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "checkout," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_cards(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/cards")
        res_json = response.json()
        cards = res_json["_embedded"]["card"]
        # print(len(cards))
        if cards:
            card = choice(cards)
            self.card_id = card["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_cards," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def get_addresses(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/addresses")

        res_json = response.json()
        addresses = res_json["_embedded"]["address"]

        if addresses:
            address = choice(addresses)
            self.address_id = address["id"]

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "get_addresses," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def customer_orders(self):
        arrival_time = datetime.now()
        start_time = time.time()

        response = self.session.get(url=self.host + "/customer-orders.html")

        response_time = time.time() - start_time
        to_log = str(arrival_time) + "," + "customer_orders," + str(response.status_code) + "," + str(
            response_time) + "," + self.request_uuid

        self.logger.info(to_log)

    def perform_task(self, name):
        task = getattr(self, name)
        task()


def user_tasks(logger, uuid):
    global total_user
    total_user += 1

    browse_tasks = ["home", "get_all_item", "get_item", "get_category_html", "get_tags", "filter_items",
                    "get_related_items"]

    cart_tasks_1 = ["home", "get_item_count", "show_fixed_items", "scroll_items_1", "get_details_html", "login",
                    "add_to_cart", "get_cart"]

    cart_tasks_2 = ["home", "scroll_items_2", "get_tags", "filter_items", "login", "add_to_cart", "get_basket",
                    "delete_from_cart"]

    # account_tasks = ["home", "get_addresses", "get_cards", "login", "customer_orders", "get_orders", "delete_from_cart"]

    checkout_tasks = ["home", "login", "scroll_items_1", "get_cart", "checkout", "customer_orders", "get_orders"]

    tasks = random.choice([browse_tasks, cart_tasks_1, cart_tasks_2, checkout_tasks])
    req_obj = Request(logger, uuid)
    for task in tasks:
        req_obj.perform_task(task)


def start_load_test(logger, lambd, runtime):
    end_time = time.time() + runtime
    start_time = time.time()
    while time.time() < end_time:
        thread = threading.Thread(target=user_tasks, args=(logger, str(total_user)))
        thread.start()
        next_arrival = random.expovariate(1 / lambd)
        time.sleep(next_arrival / 1000.0)
        # print(next_arrival)
        # if int(time.time() - start_time) % 10 == 0:
        #     print("Time Remaining: ", end_time - time.time())

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
    print("Start Testing with arrival rate - %s ms, runtime--%s s, log file %s" % (arrival_rate, runtime, file_name))

    start_load_test(logger, arrival_rate, runtime)

    print("Finish Testing at %s, Total User Spawned - %s" % (datetime.now(), total_user))
    print("Elapsed Time: ", time.time() - start_time)
