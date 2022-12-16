import speech_recognition as sr  # recognize speech to text
import pyttsx3  # speech engine
import webbrowser  # browse internet
from datetime import date, timedelta, datetime  # access date and time
import time  # import system time
import random  # will be used throughout for random response choices
import os  # used to interact with the computer's directory
import wikipedia

# General setup for pyttsx3

engine = pyttsx3.init('sapi5')  # sapi5 is the Microsoft text to speech engine
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')  # voice 0 male, 1 female
engine.setProperty("rate", 170)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Wake word to start the assitant

WAKE = "wake up"
SEARCH = {"who": "who", "what": "what", "when": "when", "where": "where", "why": "why", "how": "how"}
CONVERSATION_LOG = "Conversation Log.txt"
SLEEP = 'stop'


class Doba:

    def __init__(self):
        self.recognizer = recognizer
        self.microphone = microphone

    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000

                # timeout 5s
                audio = recognizer.listen(source, timeout=5.0)
                command = recognizer.recognize_google(audio)
                d.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    # Used to listen for the wake word
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Listening...")

                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000

                    audio = recognizer.listen(source, timeout=5.0)
                    response = recognizer.recognize_google(audio)

                    if response == WAKE:

                        d.speak("How can I help you?")
                        return response.lower()

                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error.")

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def greet(self):

        print("Welcome back")
        d.speak("Welcome back")

        # import the time
        hour = datetime.datetime.now().hour

        # greet user depending on time of the day
        if 0 <= hour < 12:
            print("Good morning sir")
            d.speak("Good morning sir")

        elif 12 <= hour < 18:
            print("Good afternoon sir")
            d.speak("Good afternoon sir")

        else:
            print("Good evening sir")
            d.speak("Good evening sir")

        # Used to open the browser or specific folders

    def open_things(self, command):
        # Will need to expand on "open" commands
        if "open youtube" in command:
            d.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com/")
            pass

        elif "open facebook" in command:
            d.speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
            pass

        elif "open my documents" in command:
            d.speak("Opening My Documents.")
            os.startfile("C:/Users/Notebook/Documents")
            pass

        elif "open my downloads folder" in command:
            d.speak("Opening your downloads folder.")
            os.startfile("C:/Users/Notebook/Downloads")
            pass
        elif "open google" in command:
            webbrowser.open_new_tab("https://www.google.com")
            d.speak("Google chrome is open now")
            time.sleep(5)
        else:
            d.speak("I don't know how to open that yet.")
            pass

    def understand_time(self, command):

        today = date.today()
        now = datetime.now()

        if "what day is today" in command:
            d.speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif "what time is it" in command:
            d.speak("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")

        elif "yesterday" in command:
            date_intent = today - timedelta(days=1)
            return date_intent
        else:
            pass

    def use_search_words(self, command):

        d.speak("Here is what I found.")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    def wikipedia(self, command):

        d.speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=3)
        d.speak("According to Wikipedia")
        print(results)
        d.speak(results)

        # Analyzes the command

    def start_conversation_log(self):

        today = str(date.today())
        today = today

        with open(CONVERSATION_LOG, "a") as f:
            f.write("Conversation started on: " + today + "\n")

    # Writes each command from the user to the conversation log
    def remember(self, command):

        with open(CONVERSATION_LOG, "a") as f:
            f.write("User: " + command + "\n")

    def analyze(self, command):
        try:

            if command.startswith('open'):
                self.open_things(command)

            if "take over the world" in command:

                d.speak("Skynet activated.")
                d.speak("hahahahaha im kidding")

            elif "introduce yourself" in command:
                d.speak("I am Doba your virtual assistant.")

            elif "what time is it" in command:

                self.understand_time(command)

            elif "how are you" in command:

                current_feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]

                # selects a random choice of greetings
                greeting = random.choice(current_feelings)
                d.speak(greeting)

            # Keep this at the end
            elif SEARCH.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            else:
                d.speak("I don't know how to do that yet.")

        except TypeError:
            print("Warning: You're getting a TypeError somewhere.")
            pass
        except AttributeError:
            print("Warning: You're getting an Attribute Error somewhere.")
            pass


def run():
    previous_response = ""

    while True:

        response = d.listen(recognizer, microphone)
        command = d.hear(recognizer, microphone, response)

        if command == previous_response:

            d.speak("You already asked that.")
            previous_command = ""

            response = d.listen(recognizer, microphone)
            command = d.hear(recognizer, microphone, response)

        elif command == SLEEP:

            d.speak('Doba is shutting down, good bye sir!')
            print('your personal assistant Doba is shutting down,Good bye')

            break

        d.analyze(command)
        previous_response = command


d = Doba()
run()
