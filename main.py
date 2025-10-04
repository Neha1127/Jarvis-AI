import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  # your static music list
import requests
import pywhatkit
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import wikipedia

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Website dictionary
websites = {
    "youtube": "https://youtube.com",
    "linkedin": "https://linkedin.com",
    "github": "https://github.com",
    "stack overflow": "https://stackoverflow.com",
    "google drive": "https://drive.google.com",
    "gmail": "https://mail.google.com",
    "my channel": "https://www.youtube.com/@LittleDreamyWonderss",
}

# OpenAI client
client = OpenAI(
    api_key="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"
)

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except:
        return None  # fallback handled separately

def openWebsite(command):
    site = command.lower().replace("open", "").strip()
    url = websites.get(site)
    if url:
        speak(f"Opening {site}")
        webbrowser.open(url)
    else:
        try:
            url = f"https://{site.replace(' ', '')}.com"
            speak(f"Opening {site}")
            webbrowser.open(url)
        except:
            speak(f"Couldn't find {site}, searching on Google.")
            webbrowser.open(f"https://www.google.com/search?q={site}")

def processCommand(c):
    c = c.lower()

    if "open" in c:
        openWebsite(c)

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

    elif "news" in c:
        r = requests.get("https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=6cd7b740e2ef429fa1b3a555971c9add")
        if r.status_code == 200:
            articles = r.json().get('articles', [])[:5]
            for article in articles:
                speak(article['title'])
        else:
            speak("Failed to fetch news.")

    elif "tell me about" in c:
        topic = c.lower().split("tell me about", 1)[1].strip()

        if not topic:
            speak("Please tell me what you'd like to know about.")
        else:
            try:
                # Try Wikipedia first
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)

            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"The topic '{topic}' has multiple meanings. Here are a few:")
                for option in e.options[:3]:  # suggest a few options
                    speak(option)
                speak("Please be more specific.")

            except wikipedia.exceptions.PageError:
                speak(f"I couldn't find a Wikipedia page for {topic}. Let me search it online.")
                webbrowser.open(f"https://www.google.com/search?q={topic}")
                speak(f"Showing results for {topic}.")

            except Exception as e:
                print(f"[Wikipedia Error]: {e}")
                speak("There was a problem accessing information. Searching online instead.")
                webbrowser.open(f"https://www.google.com/search?q={topic}")
                speak(f"Here are some search results for {topic}.")

    else:
        response = aiProcess(c)
        if response:
            speak(response)
        else:
            speak("Sorry, I couldn't fetch that. Searching online...")
            webbrowser.open(f"https://www.google.com/search?q={c}")


# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=6)

            print("Recognizing...")
            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source)

                print("Recognizing...")
                command = r.recognize_google(audio)
                processCommand(command)

        except sr.UnknownValueError:
            pass  # silent fail

        except sr.RequestError:
            speak("Speech service is unavailable.")

        except Exception as e:
            print(f"Error: {e}")
