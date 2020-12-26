import sys
import time
import grequests

BASE_PATH = "http://localhost:5000"
WORK_PATH = BASE_PATH + "/work"

EMEA = WORK_PATH + "/emea"
ASIA = WORK_PATH + "/asia"
US = WORK_PATH + "/us"

EMEA_0 = EMEA + "/0"
ASIA_0 = ASIA + "/0"
ASIA_1 = ASIA + "/1"
US_0 = US + "/0"
US_1 = US + "/1"

region_paths = [EMEA, ASIA, US]
specific_paths = [EMEA_0, ASIA_0, ASIA_1, US_0, US_1]


def response_handler_start(response, *args, **kwargs):
    print(response.json())


def start_servers():
    reqs = (grequests.get(url, stream=False, hooks={'response': response_handler_start}) for url in specific_paths)
    grequests.map(reqs)


def policy_1():
    batch_size = 100
    print("Policy 1: random worker with big batch size, batch size:", batch_size)
    reqs = (grequests.get(WORK_PATH, stream=False, verify=False) for _ in range(nb_requests))
    grequests.map(reqs, size=batch_size)


def policy_2():
    batch_size = 10
    print("Policy 2: random worker with small batch size, batch size:", batch_size)
    reqs = (grequests.get(WORK_PATH, stream=False, verify=False) for _ in range(nb_requests))
    grequests.map(reqs, size=batch_size)


def policy_3():
    batch_size = 100
    print("Policy 3: call only EMEA_0 worker, batch size:", batch_size)
    reqs = (grequests.get(EMEA_0, stream=False, verify=False) for _ in range(nb_requests))
    grequests.map(reqs, size=batch_size)


def policy_4():
    batch_size = 100
    print("Policy 4: round-robin, batch size:", batch_size)
    reqs = []
    for i in range(nb_requests):
        reqs.append(grequests.get(specific_paths[i % 5], stream=False, verify=False))

    grequests.map(reqs, size=batch_size)


def policy_5():
    batch_size = 100
    print("Policy 5: round-robin on regions, batch size:", batch_size)
    reqs = []
    for i in range(nb_requests):
        reqs.append(grequests.get(region_paths[i % 3], stream=False, verify=False))

    grequests.map(reqs, size=batch_size)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('You should run the program as ./main.py <number_of_requests> <policy_number> '
                 '<should_start_servers> (optional - true/false)')
    if len(sys.argv) == 4 and sys.argv[3] == "true":
        start_servers()

    nb_requests = int(sys.argv[1])
    nb_policy = int(sys.argv[2])
    switcher = {
        1: policy_1,
        2: policy_2,
        3: policy_3,
        4: policy_4,
        5: policy_5
    }
    policy = switcher.get(nb_policy)
    start_time = time.time()
    policy()
    print("---%s seconds---" % (time.time() - start_time))
