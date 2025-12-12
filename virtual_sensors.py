import time
import random
import requests

BLYNK_AUTH = "Your_Auth_Token"
BASE_URL = "https://blr1.blynk.cloud/external/api"


def blynk_set(pin, value):
    url = f"{BASE_URL}/update?token={BLYNK_AUTH}&{pin}={value}"
    r = requests.get(url, timeout=5)
    print("REQUEST:", url, "STATUS:", r.status_code, "BODY:", r.text)

print("Virtual sensors pushing data to Blynk...")

while True:
    temp = random.randint(20, 35)
    light = random.randint(0, 100)
    motion = random.randint(0, 1)

    blynk_set("V1", temp)
    blynk_set("V2", light)
    blynk_set("V3", motion)

    time.sleep(2)

