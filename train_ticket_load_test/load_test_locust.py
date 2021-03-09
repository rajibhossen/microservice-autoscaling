import logging
import os

from train_ticket_load_test.lib.tools import run_external_applicaton


def get_configuration_files(global_plugin_state, current_configuration, output, test_id):
    return ["locustfile.py"]


def run(test_id=1):
    driver = "locustfile.py"
    # print(driver)
    host = "http://192.168.2.12:32677"  # current_configuration["locust_host_url"]
    load = 500  # current_configuration["load"]
    spawn_rate = 100  # current_configuration["spawn_rate_per_second"] user spawn / second
    run_time = 120  # current_configuration["run_time_in_seconds"]
    log_file = "output/locust_test.log"  # os.path.splitext(driver)[0] + ".log"
    out_file = "output/locust_test.out"  # os.path.splitext(driver)[0] + ".out"
    csv_prefix = "output/result"  # os.path.join(os.path.dirname(driver), "result")
    logging.info(f"Running the load test for {test_id}, with {load} users, running for {run_time} seconds.")
    run_external_applicaton(
        f'locust --locustfile {driver} --host {host} --users {load} --spawn-rate {spawn_rate} --run-time {run_time}s '
        f'--headless --only-summary --csv {csv_prefix} --csv-full-history --logfile "{log_file}" --loglevel DEBUG >> '
        f'{out_file} 2> {out_file}',
        False)


if __name__ == '__main__':
    #  locust --locustfile locustfile.py --host http://192.168.2.12:32677 --headless --only-summary --csv output/result --csv-full-history
    output = "/home/ridl/rajibs_work/mba"
    #output = os.path.join("C:", os.sep, "Users", "mxh6295xx", "PycharmProjects", "microservice_budget", "train_ticket_load_test")
    run()
