import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')
    RecognizerIntent = autoclass('android.speech.RecognizerIntent')

class PhoneControllerApp(App):
    def build(self):
        self.mic_active = False
        self.recognizer = None
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.status_label = Label(
            text="[ Status: Mic OFF | Native Engine Ready ]", 
            size_hint_y=0.08,
            color=(0.3, 0.8, 1, 1)
        )
        main_layout.add_widget(self.status_label)
        
        self.mic_btn = Button(
            text="Turn Mic ON (Real Background Listening)", 
            size_hint_y=0.12, 
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.mic_btn.bind(on_press=self.toggle_mic)
        main_layout.add_widget(self.mic_btn)
        
        self.chat_logs = Label(
            text="[System]: App Started. Native Speech Engine Ready.\n", 
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.chat_logs.bind(texture_size=self._update_chat_height)
        
        scroll = ScrollView(size_hint_y=0.6, do_scroll_x=False)
        scroll.add_widget(self.chat_logs)
        main_layout.add_widget(scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=5)
        self.user_input = TextInput(hint_text="Type command or speak...", multiline=False)
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
            self.status_label.text = "[ Status: ACTIVE - Real Mic Listener ]"
            self.chat_logs.text += "\n[System]: Hardware Microphone Turned ON."
            self.start_native_speech_recognition()
        else:
            self.mic_btn.text = "Turn Mic ON (Real Background Listening)"
            self.mic_btn.background_color = (0.2, 0.8, 0.2, 1)
            self.status_label.text = "[ Status: Mic OFF | Native Engine Ready ]"
            self.chat_logs.text += "\n[System]: Hardware Microphone Turned OFF."
            self.stop_native_speech_recognition()

    def start_native_speech_recognition(self):
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, True)
                
                if not self.recognizer:
                    self.recognizer = SpeechRecognizer.createSpeechRecognizer(activity)
                self.recognizer.startListening(intent)
            except Exception as e:
                self.chat_logs.text += f"\n[Mic Error]: {str(e)}"

    def stop_native_speech_recognition(self):
        if platform == 'android' and self.recognizer:
            try:
                self.recognizer.stopListening()
            except Exception as e:
                pass

    def send_message(self, instance):
        msg = self.user_input.text.strip()
        if msg:
            self.chat_logs.text += f"\n[You]: {msg}"
            self.user_input.text = ""
            reply = f"Executed: {msg}"
            Clock.schedule_once(lambda dt: self.bot_reply(reply), 0.1)

    def bot_reply(self, reply_text):
        self.chat_logs.text += f"\n[AI Bot]: {reply_text}"

if __name__ == "__main__":
    PhoneControllerApp().run()
