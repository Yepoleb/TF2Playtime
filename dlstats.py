import json
import os
import queue
import threading
import http.client

API_SERVER = "api.steampowered.com"
API_PATH = "/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={}&steamid={}"
API_KEY = open("key.txt", "r").read().strip()
OUTPUT = "stats/{}.json"
CONNECTIONS = 4

steamids = json.load(open("steamids.json", "r"))

download_status = 0
def download_job():
    client = http.client.HTTPConnection(API_SERVER)
    while not id_queue.empty():
        steamid = id_queue.get()
        url = API_PATH.format(API_KEY, steamid)
        client.request("GET", url)
        resp = client.getresponse()
        data = resp.read()
        if resp.status >= 400:
            print("Failed", resp.status, steamid)
            data = b"{}"
        open("stats/{}.json".format(steamid), "wb").write(data)
        id_queue.task_done()
        global download_status
        download_status += 1
        print(download_status, steamid)
    print("Thread closed")

id_queue = queue.Queue()
for steamid in steamids:
    if not os.path.exists(OUTPUT.format(steamid)):
        id_queue.put(steamid)

for i in range(min(CONNECTIONS, id_queue.qsize())):
    t = threading.Thread(target=download_job)
    t.start()

id_queue.join()
print("Download finished")
