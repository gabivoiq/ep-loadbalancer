# import time
# import grequests
# import matplotlib.pyplot as plt
# import pandas as pd
#
# BASE_PATH = "http://localhost:5000"
# WORK_PATH = BASE_PATH + "/work"
#
# EMEA = WORK_PATH + "/emea"
# ASIA = WORK_PATH + "/asia"
# US = WORK_PATH + "/us"
#
# EMEA_0 = EMEA + "/0"
# ASIA_0 = ASIA + "/0"
# ASIA_1 = ASIA + "/1"
# US_0 = US + "/0"
# US_1 = US + "/1"
#
# FILE_PREFIX = "times_gabrielvoicu200-"
# files = [FILE_PREFIX + "worker-asia-0.txt",
#          FILE_PREFIX + "worker-asia-1.txt",
#          FILE_PREFIX + "worker-us-0.txt",
#          FILE_PREFIX + "worker-us-1.txt",
#          FILE_PREFIX + "worker-emea-0.txt"]
#
# responses = []
# region_paths = [EMEA, ASIA, US]
# specific_paths = [EMEA_0, ASIA_0, ASIA_1, US_0, US_1]
#
#
# def response_handler_start(response, *args, **kwargs):
#     print(response.json())
#
#
# def response_handler(response, *args, **kwargs):
#     if response.status_code == 200:
#         body = response.json()
#         responses.append({
#             'machine': body['machine'],
#             'region': body['region'],
#             'response_time': body['response_time']
#         })
#         print(body)
#
#
# def get_service_times():
#     service_times = {files[i]: [] for i in range(5)}
#     for filename in files:
#         with open(filename, "r") as f:
#             content = f.read()
#             service_times[filename] = [int(s) for s in content.split(' ')]
#
#     return service_times
#
#
# def start_servers():
#     reqs = (grequests.get(url, stream=False, hooks={'response': response_handler_start}) for url in specific_paths)
#     grequests.map(reqs)
#
#
# def warm_up_servers():
#     for url in specific_paths:
#         reqs = (grequests.get(url, stream=False, hooks={'response': response_handler}, verify=False) for _ in
#                 range(700))
#         grequests.map(reqs, size=100)
#         time.sleep(5)
#
#
# def policy_1(nb):
#     batch_size = 100
#     print("Policy 1: random worker with big batch size, batch size:", batch_size)
#     reqs = (grequests.get(WORK_PATH, stream=False, hooks={'response': response_handler}, verify=False) for _ in
#             range(nb))
#     grequests.map(reqs, size=batch_size)
#
#
# def policy_2(nb):
#     batch_size = 10
#     print("Policy 2: random worker with small batch size, batch size:", batch_size)
#     reqs = (grequests.get(WORK_PATH, stream=False, hooks={'response': response_handler}, verify=False) for _ in
#             range(nb))
#     grequests.map(reqs, size=batch_size)
#
#
# def policy_3(nb):
#     batch_size = 100
#     print("Policy 3: call only EMEA_0 worker, batch size:", batch_size)
#     reqs = (grequests.get(EMEA_0, stream=False, hooks={'response': response_handler}, verify=False) for _ in
#             range(nb))
#     grequests.map(reqs, size=batch_size)
#
#
# def policy_4(nb):
#     batch_size = 100
#     print("Policy 4: round-robin, batch size:", batch_size)
#     reqs = []
#     for i in range(nb):
#         reqs.append(
#             grequests.get(specific_paths[i % 5], hooks={'response': response_handler}, stream=False, verify=False))
#
#     grequests.map(reqs, size=batch_size)
#
#
# def policy_5(nb):
#     batch_size = 100
#     print("Policy 5: round-robin on regions, batch size:", batch_size)
#     reqs = []
#     for i in range(nb):
#         reqs.append(
#             grequests.get(region_paths[i % 3], stream=False, hooks={'response': response_handler}, verify=False))
#
#     grequests.map(reqs, size=batch_size)
#
#
# def get_nb_requests_each_region():
#     nb_responses_regions = []
#     nb_responses_regions.append(len([resp for resp in responses if
#                                      resp['machine'] == 'Machine 0' and resp['region'] == 'asia']))
#     nb_responses_regions.append(len([resp for resp in responses if
#                                      resp['machine'] == 'Machine 1' and resp['region'] == 'asia']))
#     nb_responses_regions.append(len([resp for resp in responses if
#                                      resp['machine'] == 'Machine 0' and resp['region'] == 'us']))
#     nb_responses_regions.append(len([resp for resp in responses if
#                                      resp['machine'] == 'Machine 1' and resp['region'] == 'us']))
#     nb_responses_regions.append(len([resp for resp in responses if
#                                      resp['machine'] == 'Machine 0' and resp['region'] == 'emea']))
#
#     return nb_responses_regions
#
#
# def graphs_service_times(service_time_regions):
#     df = pd.DataFrame(service_time_regions)
#     df.columns = ['asia_0', "asia_1", "us_0", "us_1", "emea_0"]
#     plot_df = df.plot()
#     plot_df.set_title("Service times in workers with 100 concurrent requests")
#     plot_df.set_xlabel("Number of requests")
#     plot_df.set_ylabel("Service time (ms)")
#     plt.show()
#
#
# def graphs_total_times(arr):
#     df = pd.DataFrame(arr)
#     x_labels = [1000, 1250, 1500]
#
#     plot_df = df.plot.bar()
#     plot_df.set_title("Time it takes to compute requests based on policy")
#     plot_df.set_xlabel("Number of requests")
#     plot_df.set_ylabel("Total time (s)")
#     plot_df.set_xticklabels(x_labels, rotation=0)
#
#     plt.show()
#
#
# if __name__ == "__main__":
#     # warm_up_servers()
#
#     graphs_total_times(arr)
#
#     # nb_resp_regions = get_nb_requests_each_region()
#     # print(nb_resp_regions)
#     # service_times_regions = get_service_times()
#     # graphs_service_times(service_times_regions)
