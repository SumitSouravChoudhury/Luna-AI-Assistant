import tkinter as tk
from tkinter import messagebox, Text
from threading import Thread
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import random
import cv2
import sys
import pyautogui
import time
import operator
import requests
from PIL import Image, ImageTk

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 175)

recognizer = sr.Recognizer()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, I am Luna. I am here to assist you.")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, I am Luna. I am here to assist you.")
    else:
        speak("Good Evening, I am Luna. I am here to assist you.")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        display_status("Listening...")
        audio = r.listen(source, timeout=10)
    try:
        print("Recognizing...")
        display_status("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        query = query.replace("Luna", "")
        print(f"User said: {query}\n")
        display_status("")

    except Exception as e:
        print("Say that again please")
        display_status("")
        return "None"
    return query



def calculate_expression(expression):
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "x": operator.mul,
    }

    parts = expression.split()
    if len(parts) != 3:
        return "Invalid expression"

    operand1, operator_symbol, operand2 = parts

    try:
        result = operators[operator_symbol](float(operand1), float(operand2))
        return result
    except (ValueError, ZeroDivisionError) as e:
        return "Error: " + str(e)


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = (
        f"{base_url}q={city}&appid=ed5e37c9d02774e8aa03d9810a6f7663&units=metric"
    )

    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        mai_data = weather_data["main"]
        temperature = mai_data["temp"]
        humidity = mai_data["humidity"]
        weather_info = weather_data["weather"][0]["description"]

        weather_report = f"The weather in {city} today is {weather_info}. "
        weather_report += (
            f"The temperature is {temperature}°C, and the humidity is {humidity}%."
        )
        return weather_report
    else:
        return "City not found."


def process_query(query):
    
    response = ""
    
    if "Luna" and "who are you" in query:
        response = "My name is Luna. Stands for Logical Understanding and Navigational Assistant."
    
    elif "Luna" and "who created you" in query:
        response = "My creator is The SHIPP"

    elif "Luna" and "what is the weather today" in query:
        speak("Please specify the city for the weather report.")
        city = takeCommand().lower()
        weather_report = get_weather(city)
        response = weather_report

    elif "Luna" and "tell me a joke" in query:
        joke_url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(joke_url)
        if response.status_code == 200:
            joke_data = response.json()
            joke_setup = joke_data["setup"]
            joke_punchline = joke_data["punchline"]
            joke = f"{joke_setup} {joke_punchline}"
            response = joke

    elif "Luna" and "open camera" in query:
        speak("opening camera")
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow("webcam", img)
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k == ord("c"):
                speak("tell me a name for the file")
                img_name = takeCommand().lower()
                cv2.imwrite(f"{img_name}.jpg", img)
                speak("Image captured and saved")
                print("Image captured and saved")
                break
        cap.release()
        cv2.destroyAllWindows()

    elif "Luna" and "take a screenshot" in query:
        speak("tell me a name for the file")
        name = takeCommand().lower()
        time.sleep(1)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        speak("Screenshot Saved")
        print("Screenshot Saved")

    elif "Luna" and "calculate" in query:
        expression = query.replace("luna calculate", "")
        result = calculate_expression(expression)
        response = "The result is: " + str(result)

    elif "Luna" and "my ip address" in query:
        speak("checking")
        try:
            ipAdd = requests.get("https://api.ipify.org").text
            speak("your ip address is")
            response = ipAdd
        except Exception as e:
            speak("Network is weak, please try again later")

    elif "Luna" and "create a folder" in query:
        speak("Sure, please specify the folder name.")
        folder_name = takeCommand()
        speak("Please specify the folder path")
        fold_path = takeCommand()
        if folder_name != "None":
            folder_path = os.path.join(
                f"C:\\Users\\Sumit\\{fold_path}", folder_name
            )
            try:
                os.mkdir(folder_path)
                response = f"Folder '{folder_name}' created at '{fold_path}'"
            except OSError as e:
                print(f"Error creating folder: {e}")
                speak(f"Sorry, there was an error creating the folder.")
        else:
            speak("Sorry, I couldn't understand the folder name.")

    elif "Luna" and "create a file" in query:
        speak("Sure, please specify the file name.")
        file_name = takeCommand()
        speak("Please specify the file path")
        fil_path = takeCommand()
        if file_name != "None":
            file_path = os.path.join(
                f"C:\\Users\\Sumit\\{fil_path}", file_name
            )
            try:
                with open(file_path, "w") as file:
                    response = f"File '{file_name}' created at '{fil_path}'"
            except OSError as e:
                print(f"Error creating file: {e}")
                speak(f"Sorry, there was an error creating the file.")
        else:
            speak("Sorry, I couldn't understand the file name.")

    elif "Luna" and "tell me the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(strTime)
        response = f"Sir, the time is {strTime}"

    elif "Luna" and "flip a coin" in query:
        result = random.randint(0, 1)
        if result == 0:
            response = "It's heads!"
        else:
            response = "It's tails!"

    elif "Luna" and "open google" in query:
        speak("Opening google")
        webbrowser.open_new_tab("google.com")

    elif "Luna" and "open youtube" in query:
        speak("Opening Youtube")
        webbrowser.open_new_tab("youtube.com")

    elif "Luna" and "open notepad" in query:
        speak("Opening notepad")
        npath = "C:\WINDOWS\system32\\notepad.exe"
        os.startfile(npath)

    elif "Luna" and "open settings" in query:
        speak("Opening settings")
        os.startfile("ms-settings:")

    elif "Luna" and "open command prompt" in query:
        speak("Opening command prompt")
        os.system("start cmd")

    elif "Luna" and "open new window" in query:
        speak("Opening new window")
        pyautogui.hotkey("ctrl", "n")

    elif "Luna" and "close youtube" in query:
        speak("Closing Youtube")
        os.system("taskkill /f /im msedge.exe")
        os.system("taskkill /f /im chrome.exe")

    elif "Luna" and "close browser" in query:
        speak("Closing browser")
        os.system("taskkill /f /im msedge.exe")

    elif "Luna" and "close chrome" in query:
        speak("Closing chrome")
        os.system("taskkill /f /im chrome.exe")

    elif "Luna" and "close notepad" in query:
        speak("Closing notepad")
        os.system("taskkill /f /im notepad.exe")

    elif "Luna" and "close command prompt" in query:
        speak("Closing command prompt")
        os.system("taskkill /f /im cmd.exe")

    elif "Luna" and "search in google" in query:
        speak("What should I search?")
        qry = takeCommand().lower()
        webbrowser.open_new_tab(f"{qry}")
        results = wikipedia.summary(qry, sentences=2)
        response = results

    elif "Luna" and "search in youtube" in query:
        speak("What would you like to watch?")
        qrry = takeCommand().lower()
        webbrowser.open_new_tab(f"www.youtube.com/results?search_query={qrry}")

    elif "Luna" and "play a song by" in query:
        song = query.replace("play a song by", "")
        wk.playonyt(song)

    elif "Luna" and "play" and "youtube" in query:
        vid = query.replace("play", "")
        wk.playonyt(vid)

    elif "Luna" and "type" in query:
        query = query.replace("type", "")
        pyautogui.typewrite(f"{query}", 0.1)

    elif "Luna" and "undo" in query:
        pyautogui.hotkey("ctrl", "z")

    elif "Luna" and "maximize window" in query:
        pyautogui.hotkey("alt", "space")
        time.sleep(1)
        pyautogui.press("x")

    elif "Luna" and "minimise window" in query:
        pyautogui.hotkey("alt", "space")
        time.sleep(1)
        pyautogui.press("n")

    elif "Luna" and "enter" in query:
        pyautogui.press("enter")

    elif "Luna" and "shut down the system" in query:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "Luna" and "hibernate the system" in query:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "Luna" and "go to sleep" in query:
        response = "I am switching off"
        sys.exit()

    elif "Luna" and "volume up" in query:
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")

    elif "Luna" and "volume down" in query:
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")

    elif "Luna" and "what is" in query:
        print("Searching Wikipedia")
        speak("Searching Wikipedia")
        query = query.replace("luna what is", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        response = results

    elif "Luna" and "who is" in query:
        speak("Searching Wikipedia")
        query = query.replace("luna who is", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        response = results

    else:
        response = "Sorry, I didn't understand that."
            
    display_output(query, response)
    speak(response)
        


def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            display_status("Listening...")
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            display_status("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            query = query.lower()
            print(f"User said: {query}")
            display_status("")
            process_query(query)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            display_status("Sorry, I didn't catch that.")
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing the Google API.")
            display_status("Sorry, I'm having trouble accessing the Google API.")


def display_output(input_text, response_text):
    input_response_text.config(state=tk.NORMAL)
    input_response_text.insert(tk.END, "User: " + input_text + "\n")
    input_response_text.insert(tk.END, "Luna: " + response_text + "\n")
    input_response_text.config(state=tk.DISABLED)
    
def display_status(status):
    status_text.config(state=tk.NORMAL)
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, status)
    status_text.config(state=tk.DISABLED)

def start_listening():
    wishMe()
    listening_thread = Thread(target=listen)
    listening_thread.daemon = True
    listening_thread.start()
    
def stop_listening():
    global listening
    listening = False
    display_status("Stopped Listening")
    

root = tk.Tk()
root.title("Luna - Voice Assistant")
root.state('zoomed')
root.config(bg="#f0f0f0")

def style_button(button):
    button.config(bg="#007bff", fg="#ffffff", font=("Arial", 12), relief=tk.FLAT, bd=0)


def style_text_widget(text_widget):
    text_widget.config(
        bg="#ffffff", fg="#333333", font=("Arial", 12), relief=tk.FLAT, bd=2
    )


input_response_text = Text(root, wrap=tk.WORD, width=40, height=20)
input_response_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
style_text_widget(input_response_text)
input_response_text.config(state=tk.DISABLED)

status_text = Text(root, wrap=tk.WORD, width=40, height=2)
status_text.pack(padx=10, pady=10, fill=tk.X, expand=False)
style_text_widget(status_text)
status_text.config(state=tk.DISABLED)

start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=10, ipadx=10, ipady=5)
style_button(start_button)

stop_button = tk.Button(root, text="Stop Listening", command=stop_listening)
stop_button.pack(pady=10, ipadx=10, ipady=5)
style_button(stop_button)

def close_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop_listening()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()