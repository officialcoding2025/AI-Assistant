import speech_recognition as sr
import pyttsx3
import requests
import json

# Gemini API Setup
API_KEY = "AIzaSyAwcL_LQXUeZS2MSaXEAvKVC4jIbkp_6fM" # Add API From Gemini API Website
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Voice Engine
engine = pyttsx3.init()
engine.setProperty("rate", 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

def ask_gemini(prompt):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Error with Gemini API."

# Main Loop
speak("Hello, I am your Gemini Voice Assistant.")
while True:
    query = listen().lower()
    if "exit" in query or "quit" in query:
        speak("Goodbye!")
        break
    if query:
        print(f"🗣️ You: {query}")
        response = ask_gemini(query)
        print(f"🤖 Gemini: {response}")
        speak(response)
