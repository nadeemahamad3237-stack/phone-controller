import os
import time

class VoicePhoneController:
    def __init__(self):
        print("=== Phone Controller Server Started ===")

    def listen(self):
        try:
            res = os.popen('termux-speech-to-text').read().lower().strip()
            return res
        except Exception:
            return ""

    def execute_command(self, cmd):
        if not cmd:
            return

        print(f"Recognized Command: {cmd}")

        # 1. Apps Open Commands
        if "youtube" in cmd:
            os.system("termux-open-url https://www.youtube.com")
        elif "whatsapp" in cmd:
            os.system("am start -n com.whatsapp/.Main")
        elif "chrome" in cmd:
            os.system("am start -n com.android.chrome/com.google.android.apps.chrome.Main")

        # 2. UI Control inside Apps (Touch / Scroll)
        elif "scroll down" in cmd or "down" in cmd:
            os.system("input swipe 500 1500 500 500 300")
        elif "scroll up" in cmd or "up" in cmd:
            os.system("input swipe 500 500 500 1500 300")
        elif "click center" in cmd or "select" in cmd:
            os.system("input tap 500 1000")
        elif "back" in cmd:
            os.system("input keyevent 4")
        elif "home" in cmd:
            os.system("input keyevent 3")

        # 3. Hardware Commands
        elif "vibrate" in cmd:
            os.system("termux-vibrate -d 1000")
        elif "torch on" in cmd:
            os.system("termux-torch on")
        elif "torch off" in cmd:
            os.system("termux-torch off")

    def run_forever(self):
        while True:
            cmd = self.listen()
            if cmd:
                self.execute_command(cmd)
            time.sleep(1)

if __name__ == "__main__":
    controller = VoicePhoneController()
    controller.run_forever()
