import os
import time

class VoicePhoneController:
    def __init__(self):
        print("=== Silent Background Voice Controller Started ===")

    def listen_silently(self):
        """
        Yeh background me silent rahega. 
        Jab aap bolenge tabhi command capture karega.
        """
        try:
            # Termux API speech recognition
            res = os.popen('termux-speech-to-text').read().lower().strip()
            return res
        except Exception:
            return ""

    def process_command(self, cmd):
        if not cmd:
            return

        print(f"Active Command Received: {cmd}")

        # 1. Open Apps
        if "youtube" in cmd:
            os.system("termux-open-url https://www.youtube.com")
        elif "whatsapp" in cmd:
            os.system("am start -n com.whatsapp/.Main")
        elif "chrome" in cmd:
            os.system("am start -n com.android.chrome/com.google.android.apps.chrome.Main")

        # 2. Inside App Controls
        elif "scroll down" in cmd or "down" in cmd:
            os.system("input swipe 500 1500 500 500 300")
        elif "scroll up" in cmd or "up" in cmd:
            os.system("input swipe 500 500 500 1500 300")
        elif "click" in cmd or "select" in cmd:
            os.system("input tap 500 1000")
        elif "back" in cmd:
            os.system("input keyevent 4")
        elif "home" in cmd:
            os.system("input keyevent 3")

        # 3. System Actions
        elif "vibrate" in cmd:
            os.system("termux-vibrate -d 1000")
        elif "torch on" in cmd:
            os.system("termux-torch on")
        elif "torch off" in cmd:
            os.system("termux-torch off")

    def run(self):
        while True:
            # Silent background listening loop
            cmd = self.listen_silently()
            if cmd:
                self.process_command(cmd)
            time.sleep(2) # CPU waise hi free rahega

if __name__ == "__main__":
    app = VoicePhoneController()
    app.run()
