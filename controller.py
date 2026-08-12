import os
class PhoneController:
    def toast(self, m): os.system(f"termux-toast '{m}'")
    def speak(self, t): os.system(f"termux-tts-speak '{t}'")
    def vibrate(self, d=500): os.system(f"termux-vibrate -d {d}")
    def open_app(self, p): os.system(f"monkey -p {p} -c android.intent.category.LAUNCHER 1")
