# skid-nuker.py  ← run this once and leave it open
import requests, time, threading

WEBHOOK = "https://discord.com/api/webhooks/1467137149873819710/oDpNM0_05l4BLYpA6yri4jQ_mB14fvJF5wkOOsMozD4KNM17kBXFmb189GWvxr2-r_kb"
TOKEN = "MTQ4NDYyODkxMjYzMjg5MzY2MQ.Gmogss.G6k-GvqxfO8P2DlANXWn9EqhXAN3jNYyFR0fX8"  # ← put the NEW token here

active = {}

def spam(user_id):
    dm = requests.post("https://discord.com/api/v10/users/@me/channels",
                       headers={"Authorization": f"Bot {TOKEN}"},
                       json={"recipient_id": user_id}).json()    while user_id in active:
        requests.post(f"https://discord.com/api/v10/channels/{dm}/messages",
                      headers={"Authorization": f"Bot {TOKEN}"},
                      json={"content": "SKID SKID SKID SKID SKID"})
        time.sleep(1.4)

while True:
    try:
        msgs = requests.get(WEBHOOK + "/messages?limit=3").json()
        for m in msgs:
            txt = m.get("content","")
            if txt.startswith("START_NUKE "):
                uid = txt.split()                if uid not in active:
                    active= True
                    threading.Thread(target=spam, args=(uid,)).start()
                    print(f"Started nuking {uid}")
            if txt.startswith("STOP_NUKE "):
                uid = txt.split()                active.pop(uid, None)
                print(f"Stopped {uid}")
        time.sleep(2)
    except: time.sleep(5)
