import datetime
import pyttsx3 as p
import speech_recognition as sr
import randfacts
import pywhatkit
from Selenium_web import *
from jokes import *
from tkinter import *
from PIL import ImageTk, Image
import threading
import subprocess

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('NOVA')
        self.root.geometry('600x600')

        # Background Image
        background_image = Image.open("Nova.jpg")
        self.photo = ImageTk.PhotoImage(background_image)

        self.panel = Label(self.root, image=self.photo)
        self.panel.pack(fill='both', expand=True)

        # User Text Frame
        userFrame = Frame(self.root, bg='#f0f0f0', bd=5)
        userFrame.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

        self.userText = StringVar()
        self.userText.set("It's Me NOVA: Your Voice Assistant")

        top = Label(userFrame, textvariable=self.userText, bg='#f0f0f0', fg='#e67813', font=('Georgia', 22))
        top.pack(fill='both', expand=True)

        # Buttons
        btnFrame = Frame(self.root, bg='#f0f0f0')
        btnFrame.place(relx=0.5, rely=0.9, relwidth=0.75, relheight=0.1, anchor='n')

        btn1 = Button(btnFrame, text='Speak', font=('Arial', 18), bg='#C0392B', fg='white', command=self.clicked)
        btn1.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        btn2 = Button(btnFrame, text='Close', font=('Arial', 18), bg='#C0392B', fg='white', command=self.close)
        btn2.pack(side='right', fill='both', expand=True, padx=10, pady=10)



        self.voice_assistant_initialized = False
        self.r = sr.Recognizer()
        self.listening = False

        self.root.protocol("WM_DELETE_WINDOW", self.close)  # Ensure the app closes properly
        self.root.mainloop()

    def speak(self, text):
        self.userText.set(text)  # Display the spoken text on the screen
        self.root.update()  # Update the GUI to reflect changes
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 190)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

    def greet_user(self):
        self.speak("Hello, I am your voice Assistant. What can I do for you?")
        self.voice_assistant_initialized = True
        self.listen_and_respond_thread()  # Call method to listen for user input and respond in a new thread

    def listen_and_respond_thread(self):
        threading.Thread(target=self.listen_and_respond).start()

    def listen_and_respond(self):
        self.listening = True

        try:
            with sr.Microphone() as source:
                self.userText.set("Listening...")
                self.root.update()  # Update the GUI to reflect changes
                try:
                    audio = self.r.listen(source, timeout=120)  # Increased timeout to 120 seconds
                except sr.WaitTimeoutError:
                    self.speak("Listening timed out. Please try again.")
                    if self.listening:
                        self.listen_and_respond()
                    return

                text2 = self.r.recognize_google(audio)
                self.userText.set(text2)  # Display recognized text

            NOTE_STRS = ["make a note", "write this down", "remember this"]
            if any(phrase in text2 for phrase in NOTE_STRS):
                self.speak("What would you like to note?")
                with sr.Microphone() as source:
                    audio = self.r.listen(source, timeout=120)  # Increased timeout to 120 seconds
                    note_text = self.r.recognize_google(audio).lower()
                self.note(note_text)
                self.speak("I have made a note of that.")

            elif "information" in text2:
                self.speak("What information do you need?")
                with sr.Microphone() as source:
                    audio = self.r.listen(source, timeout=120)  # Increased timeout to 120 seconds
                    infor = self.r.recognize_google(audio)
                self.speak("Searching {} in Wikipedia".format(infor))
                assist = infow()
                info=assist.get_info(infor)
                self.speak("Here is what I found: " + info[:400])
                # Perform Wikipedia search here

            elif "play" in text2 and "video" in text2:
                self.speak("You want me to play which video?")
                with sr.Microphone() as source:
                    audio = self.r.listen(source, timeout=120)  # Increased timeout to 120 seconds
                    vid = self.r.recognize_google(audio)
                self.speak("Playing {} on YouTube".format(vid))
                self.listening = False  # Stop listening when playing a video
                pywhatkit.playonyt(vid)

            elif "fact" in text2 or "facts" in text2:
                self.speak("Sure")
                x = randfacts.get_fact()
                self.userText.set(x)
                self.speak("Did you know that, " + x)

            elif "joke" in text2 or "jokes" in text2:
                ar = joke()
                self.speak(ar[0])
                self.speak(ar[1])

            elif "date and time" in text2 or "current time" in text2:
                now = datetime.datetime.now()
                current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
                self.speak(f"The current date and time is {current_datetime}")


            elif "your name" in text2 or "who are you" in text2:
                self.speak("My name is Nova")

            elif "goodbye" in text2 or "bye" or "ok Thank you" or "ok you can leave"in text2:
                self.speak("Goodbye! Have a great day.")
                self.close()  # Call close method to exit the application


            #else:

                #self.speak("I didn't understand that. Please try again.")

            if self.listening:
                self.listen_and_respond_thread()  # Continue listening for further input in a new thread

        except sr.UnknownValueError:
            if self.listening:
                self.speak("Sorry, I couldn't understand that. Please try again.")
                self.listen_and_respond_thread()  # Continue listening for further input in a new thread

    def note(self, text):
        date = datetime.datetime.now()
        fname = str(date).replace(":", "-") + "-note.txt"
        with open(fname, "w") as f:
            f.write(text)
        subprocess.Popen(["notepad.exe", fname])

    def clicked(self):
        if not self.voice_assistant_initialized:
            self.greet_user()
        else:
            self.listen_and_respond_thread()  # Start listening and responding immediately if already initialized

    def close(self):
        self.listening = False  # Stop the listening loop
        self.root.destroy()  # Close the GUI

# Initialize the pyttsx3 engine
engine = p.init()

# Initialize the GUI
gui = GUI()



