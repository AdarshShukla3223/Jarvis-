import random
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import time

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold = 0.5
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network issue, please check your connection.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

def wait_for_jarvis():
    speak("Task completed. Say 'Jarvis' to wake me up.")
    while True:
        query = takecommand()
        if "jarvis" in query:
            speak("I am back! What can I do for you?")
            break

def wish():
    hour = int(datetime.datetime.now().hour)
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    speak(f"{greeting}, Adarsh Sir! I am Jarvis. How can I assist you today?")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        email = 'your-email@gmail.com'  # Replace with your email
        app_password = 'your-app-password'  # Use app password if 2FA is enabled
        server.login(email, app_password)
        server.sendmail(email, to, content)
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

if __name__ == "__main__":
    wish()
    while True:
        query = takecommand()

        if "open notepad" in query:
            os.system("notepad.exe")
            wait_for_jarvis()

        elif "open command prompt" in query:
            os.system("start cmd")
            wait_for_jarvis()

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while cap.isOpened():
                ret, img = cap.read()
                if not ret:
                    break
                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) == 27:  # ESC key
                    break
            cap.release()
            cv2.destroyAllWindows()
            wait_for_jarvis()

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak(results)
            print(results)
            wait_for_jarvis()

        elif "play my song" in query:
            speak("Which song should I play?")
            song_name = takecommand()
            kit.playonyt(song_name)

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            wait_for_jarvis()

        elif "open google" in query:
            speak("What should I search?")
            cm = takecommand()
            webbrowser.open(f"https://www.google.com/search?q={cm}")
            wait_for_jarvis()

        elif "send message" in query:
            kit.sendwhatmsg_instantly("+9305263223", "Hello, this is Jarvis!")
            wait_for_jarvis()

        elif "erp" in query:
            speak("Opening ERP portal.")
            webbrowser.open("https://erp.psit.ac.in/")
            wait_for_jarvis()

        elif "lead code" in query:
            webbrowser.open("https://leetcode.com/")
            wait_for_jarvis()

        elif "play music" in query:
            music_dir = "C:\\Users\\shukl\\Music"
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                speak("No songs found in the music directory.")
            wait_for_jarvis()

        elif "email" in query:
            speak("What should I say?")
            content = takecommand()
            sendEmail("2k22.csiot.2212150@gmail.com", content)
            wait_for_jarvis()

        elif "no thanks" in query:
            speak("Thanks for using me. Have a great day!")
            sys.exit()

        elif "sleep" in query:
            speak("Going to sleep. Say 'Jarvis' to wake me up.")
            wait_for_jarvis()

        elif "stop" in query or "shutdown" in query or "exit" in query or "bye" in query:
            speak("Shutting down. Have a great day!")
            sys.exit()
