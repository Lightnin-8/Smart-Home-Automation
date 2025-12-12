import streamlit as st
import requests

# ----------------------------
# BLYNK SETTINGS
# ----------------------------
BLYNK_TOKEN = "Your_Auth_Token"

V1_TEMP = "V1"
V2_LIGHT = "V2"
V3_MOTION = "V3"
V4_LIGHT_ACT = "V4"
V5_FAN_ACT = "V5"
V6_AC_ACT = "V6"

API_GET = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}"

# ----------------------------
# Blynk GET helper
# ----------------------------
def blynk_get(pin):
    try:
        r = requests.get(f"{API_GET}&{pin}")
        return int(r.text)
    except:
        return 0

# ----------------------------
# STREAMLIT PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Smart Home Dashboard", page_icon="🏠", layout="wide")
st.title("🏠 Smart Home Automation Dashboard (Live Preview)")

# ----------------------------
# AUTO REFRESH USING JS (Every 1 second)
# ----------------------------
refresh_rate_ms = 1000

st.markdown(
    f"""
    <script>
        function autoRefresh() {{
            setTimeout(function() {{ window.location.reload(); }}, {refresh_rate_ms});
        }}
        autoRefresh();
    </script>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# METRIC BOXES
# ----------------------------
col1, col2 = st.columns(2)

temp_box = col1.metric("🌡 Temperature", "0 °C")
light_box = col1.metric("💡 Light Level", "0 %")
motion_box = col1.metric("🚶 Motion", "0")

st.subheader("⚙ Appliance Status")
light_status = st.empty()
fan_status = st.empty()
ac_status = st.empty()

# ----------------------------
# READ BLYNK VALUES
# ----------------------------
temp = blynk_get(V1_TEMP)
light = blynk_get(V2_LIGHT)
motion = blynk_get(V3_MOTION)

act_light = blynk_get(V4_LIGHT_ACT)
act_fan   = blynk_get(V5_FAN_ACT)
act_ac    = blynk_get(V6_AC_ACT)

# Update metric boxes
temp_box.metric("🌡 Temperature", f"{temp} °C")
light_box.metric("💡 Light Level", f"{light} %")
motion_box.metric("🚶 Motion", "Yes" if motion else "No")

# Update appliance states
light_status.write(f"💡 **Light:** {'ON' if act_light else 'OFF'}")
fan_status.write(f"🌀 **Fan:** {'ON' if act_fan else 'OFF'}")
ac_status.write(f"❄ **AC:** {'ON' if act_ac else 'OFF'}")

