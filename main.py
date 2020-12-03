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

responses = []
region_paths = [EMEA, ASIA, US]
specific_paths = [EMEA_0, ASIA_0, ASIA_1, US_0, US_1]


def response_handler(response, *args, **kwargs):
    if response.status_code == 200:
        body = response.json()
        responses.append({
            'machine': body['machine'],
            'region': body['region'],
            'response_time': body['response_time']
        })
        print(body)


def warm_up_servers():
    # for url in specific_paths:
    #     reqs = (grequests.get(url, stream=False, hooks={'response': response_handler}, verify=False) for _ in
    #             range(1490))
    #     grequests.map(reqs, size=100)

    with open("pf.txt", "r") as f:
        content = f.read()
        list_resp = [int(s) for s in content.split(' ')]
        print(list_resp)


def policy_1():
    print("policy1")


def policy_2():
    print("policy2")


def policy_3():
    print("policy3")


def policy_4():
    print("policy4")


def policy_5():
    print("policy5")


if __name__ == "__main__":
    warm_up_servers()
