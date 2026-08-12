import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class LocalAIBot:
    """Offline Rule & Pattern Based AI Engine (No API Needed)"""
    def generate_reply(self, text):
        text = text.lower().strip()
        
        if not text:
            return "Please say or type something."
            
        # Greeting patterns
        if re.search(r'\b(hi|hello|hey|greetings|hola)\b', text):
            return "Hello! I am your local phone assistant. How can I help you today?"
            
        # Device Control Commands
        elif "mic" in text or "listen" in text:
            return "You can use the 'Turn Mic ON' toggle button at the top to start/stop background listening."
        elif "status" in text:
            return "All local services are active. Background voice listener and local bot are ready."
        elif "who are you" in text or "name" in text:
            return "I am your offline Phone Controller Bot built directly into this app."
        elif "help" in text:
            return "You can type commands like 'status', 'mic', or ask general questions. I work completely offline!"
        elif "time" in text or "date" in text:
            from datetime import datetime
            return f"Current local time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
        # Fallback default response
        else:
            return f"Processed command: '{text}'. (Local AI Active - No API needed)"

class PhoneControllerApp(App):
    def build(self):
        self.mic_active = False
        self.ai_engine = LocalAIBot()
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header Status
        self.status_label = Label(
            text="[ Status: Mic OFF | Offline AI Bot Ready ]", 
            size_hint_y=0.08,
            color=(0.3, 0.8, 1, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Mic Toggle Button
        self.mic_btn = Button(
            text="Turn Mic ON (Background Active)", 
            size_hint_y=0.12, 
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.mic_btn.bind(on_press=self.toggle_mic)
        main_layout.add_widget(self.mic_btn)
        
        # Chat Display Area
        self.chat_logs = Label(
            text="[Offline AI Bot]: Hello! I work 100% offline without any API key.\n", 
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.chat_logs.bind(texture_size=self._update_chat_height)
        
        scroll = ScrollView(size_hint_y=0.6, do_scroll_x=False)
        scroll.add_widget(self.chat_logs)
        main_layout.add_widget(scroll)
        
        # Input Section
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=5)
        self.user_input = TextInput(
            hint_text="Type command or chat (e.g. hi, status, time)...", 
            multiline=False
        )
        send_btn = Button(text="Send", size_hint_x=0.25, background_color=(0.2, 0.6, 1, 1))
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        
        return main_layout

    def _update_chat_height(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width, None)

    def toggle_mic(self, instance):
        self.mic_active = not self.mic_active
        if self.mic_active:
            self.mic_btn.text = "Turn Mic OFF"
            self.mic_btn.background_color = (0.9, 0.2, 0.2, 1)
            self.status_label.text = "[ Status: Mic Listening in Background... ]"
            self.chat_logs.text += "\n[System]: Background listener active."
        else:
            self.mic_btn.text = "Turn Mic ON (Background Active)"
            self.mic_btn.background_color = (0.2, 0.8, 0.2, 1)
            self.status_label.text = "[ Status: Mic OFF | Offline AI Bot Ready ]"
            self.chat_logs.text += "\n[System]: Background listener stopped."

    def send_message(self, instance):
        msg = self.user_input.text.strip()
        if msg:
            self.chat_logs.text += f"\n[You]: {msg}"
            self.user_input.text = ""
            
            # Instant Offline Bot Reply
            reply = self.ai_engine.generate_reply(msg)
            Clock.schedule_once(lambda dt: self.bot_reply(reply), 0.1)

    def bot_reply(self, reply_text):
        self.chat_logs.text += f"\n[Offline AI Bot]: {reply_text}"

if __name__ == "__main__":
    PhoneControllerApp().run()
