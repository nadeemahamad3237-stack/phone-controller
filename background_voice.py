import os, time
from controller import PhoneController
phone = PhoneController()
def listen():
    os.system("termux-speech-to-text > voice.txt 2>/dev/null")
    try: return open("voice.txt").read().lower().strip()
    except: return ""
while True:
    cmd = listen()
    if "youtube" in cmd: phone.open_app("com.google.android.youtube")
    elif "vibrate" in cmd: phone.vibrate(1000)
    elif "stop" in cmd: break
    time.sleep(1)
