# Copyright @ Rahul Grover
# https://www.github.com/RahulGrover12
# AI Assistant - Chhotu
import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import links
import requests
from openai import OpenAI
from gtts import gTTS
import sys

with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "YOUR_API_KEY"

def speak_old(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    print(text)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def ai_process(command):
    client = OpenAI(
    api_key="YOUR_API_KEY"
)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Give a short description."},
        {
            "role": "user",
            "content": command
        }
    ]
)
  
    return (completion.choices[0].message.content)

def process_command(c):
    print(f"Command recognized: {c}")
    if c.lower().startswith("open"):
        web = c.lower().split(" ")[1]
        sites = links.websites[web]
        webbrowser.open(sites)

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music_library.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if res.status_code==200:
            # Parse the JSON response
            data = res.json()

            # Extract and print the article
            speak("Top Headlines are: ")
            for article in data["articles"]:
                speak(article['title'])

    else:
        output = ai_process(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Chhotu....")
    while True:
        try:
            # Listen for the wake word "chotu"
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}")
            if word.lower() == "chhotu":
                speak("Ji, Rahul!")
                
                # Listen for the next command
                with sr.Microphone() as source:
                    print("Chotu Active, listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)
                    print("Finished listening for command...")
                    command = recognizer.recognize_google(audio)
                    # print(f"Command: {command}")

                    process_command(command)
            if(word.lower()=="exit"):
                break
                    
        except Exception as e:
            print(f"An error occurred: {e}")
