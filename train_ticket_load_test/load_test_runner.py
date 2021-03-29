import subprocess as sp
import sys
import time


def run_program(rate):
    procs = []
    for i in range(3, 5):
        p = sp.Popen([sys.executable, "custom_load_test.py", rate, "150", "data_p" + rate + "_t2_" + str(i)])
        procs.append(p)

    for p in procs:
        p.wait()


if __name__ == '__main__':
    for rate in [65, 60, 55, 50, 45, 40, 35, 30, 25, 20]:
        run_program(str(rate))
        print("####################")
        time.sleep(45)

