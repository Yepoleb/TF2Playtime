import re
import urllib.request
import json
import queue
import threading
import http.client

NAME_RE = re.compile(r"http://steamcommunity.com/id/(\w+)")
PROFILE_RE = re.compile(r"http://steamcommunity.com/profiles/(\d+)")
PATH_FORMAT = "group/tf2-highlander_{}.html"
API_KEY = open("key.txt", "r").read().strip()
CONNECTIONS = 4
API_SERVER = "api.steampowered.com"
API_PATH = "/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}"
ID_CACHE = "vanitycache.json"
IDS_OUT = "steamids.json"


steamids = set()
names = set()
for page_num in range(1,34):
    page = open(PATH_FORMAT.format(page_num), "r").read()
    names |= set(NAME_RE.findall(page))
    steamids |= set(PROFILE_RE.findall(page))

idmap = json.load(open(ID_CACHE, "r"))

download_status = 0
def download_job():
    client = http.client.HTTPConnection(API_SERVER)
    while not profiles_queue.empty():
        name = profiles_queue.get()
        url = API_PATH.format(API_KEY, name)
        client.request("GET", url)
        resp = client.getresponse()
        data = resp.read()
        if resp.status == 404:
            print("Failed 404", name)
        else:
            js = json.loads(data.decode("utf8"))
            if js["response"]["success"] != 1:
                print("Failed to get id for user", name)
                idmap[name] = None
            else:
                steamid = js["response"]["steamid"]
                idmap[name] = steamid
        profiles_queue.task_done()
        global download_status
        download_status += 1
        print(download_status, name)
    print("Thread closed")

profiles_queue = queue.Queue()
for name in names:
    if name not in idmap:
        profiles_queue.put(name)

for i in range(min(CONNECTIONS, profiles_queue.qsize())):
    t = threading.Thread(target=download_job)
    t.start()

profiles_queue.join()
json.dump(idmap, open(ID_CACHE, "w"), indent=2, sort_keys=True)
print("Download finished")

for name in names:
    if not idmap[name]:
        continue
    steamids.add(idmap[name])

print("Found", len(steamids), "Steam IDs")
json.dump(list(steamids), open(IDS_OUT, "w"), indent=2, sort_keys=True)
