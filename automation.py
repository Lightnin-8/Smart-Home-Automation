import time
import requests

# -------------------------
# BLYNK AUTH TOKEN
# -------------------------
BLYNK_AUTH = "MAAnB2H2BhnKSs2uQzURiCS0mMZxWt6w"    # <-- replace this!

BASE_URL = "https://blr1.blynk.cloud/external/api"


# -------------------------
# Sensor Values (live)
# -------------------------
temperature = 25
light_level = 50
motion = 0

# -------------------------
# Appliance States
# -------------------------
light_state = 0
fan_state = 0
ac_state = 0

# -------------------------
# Thresholds
# -------------------------
TEMP_THRESHOLD = 30
LIGHT_THRESHOLD = 30

# -------------------------
# Helper Functions
# -------------------------
def blynk_get(pin):
    try:
        url = f"{BASE_URL}/get?token={BLYNK_AUTH}&{pin}"
        r = requests.get(url).json()
        return int(r[0])
    except:
        return None

def blynk_set(pin, value):
    url = f"{BASE_URL}/update?token={BLYNK_AUTH}&{pin}={value}"
    requests.get(url)

# -------------------------
# Main Automation Logic
# -------------------------
def automation_logic():
    global temperature, light_level, motion
    global light_state, fan_state, ac_state

    # Read Live Sensor Data
    temperature = blynk_get("V1")
    light_level = blynk_get("V2")
    motion = blynk_get("V3")

    print(f"T={temperature}, Light={light_level}, Motion={motion}")

    # --------- AC Logic ---------
    if temperature is not None and temperature >= TEMP_THRESHOLD:
        ac_state = 1
    else:
        ac_state = 0

    # --------- Fan Logic ---------
    if temperature is not None and temperature >= 28:
        fan_state = 1
    else:
        fan_state = 0

    # --------- Light Logic ---------
    if light_level is not None and motion is not None:
        if light_level < LIGHT_THRESHOLD and motion == 1:
            light_state = 1
        else:
            light_state = 0

    # Upload States Back to Blynk
    blynk_set("V4", light_state)
    blynk_set("V5", fan_state)
    blynk_set("V6", ac_state)

# -------------------------
# Main Loop
# -------------------------
print("Smart Home Automation Running...")

while True:
    automation_logic()
    time.sleep(1)
