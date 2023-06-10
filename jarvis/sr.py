import requests
import speech_recognition
import time
import asyncio
import subprocess
import board
import adafruit_dotstar
import requests
import os


DOTSTAR_DATA = board.D5
DOTSTAR_CLOCK = board.D6

dots = adafruit_dotstar.DotStar(DOTSTAR_CLOCK, DOTSTAR_DATA, 3, brightness=0.2)

recognizer = speech_recognition.Recognizer()

text = ''


class KeyPhrase:
    def __init__(self, words, callback):
        self.words = words
        self.callback = callback


def getweather():

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = os.getenv('WEATHER_KEY')
    CITY = "Edmonton"

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()

    temp = round(response['main']['temp'] - 273.15)
    feels_like = round(response['main']['feels_like'] - 273.15)
    description = response['weather'][0]['description']
    high = round(response['main']['temp_max'] - 273.15)
    low = round(response['main']['temp_min'] - 273.15)

    if text.find("temperature") >= 0:
        textToSpeach(f'"the temperature in edmonton is {temp} degrees"')
    elif text.find("weather") >= 0:
        asyncio.run(textToSpeach(
            f'"It is currently {temp} but feels like {feels_like} degrees, with {description}"'))
    else:
        textToSpeach(
            f'"Today, expect {description}. The high will be {high} degrees and the low will be {low}"')


def music():
    song = text[:5]
    requests.put(
        url="http://localhost:3000/sendQuery", data=song, headers={'Content-Type': 'text/plain'})


tasks = [KeyPhrase(["weather", "temperature", "forecast"], getweather),
         KeyPhrase(["play"], music), ]


def textToSpeach(message):
    subprocess.call([f'espeak {message} --stdout | aplay'], shell=True)


activated = False

while True:
    if activated:
        if time.time() > t_stop:
            activated = False
            dots[0] = (0, 0, 0)
            dots[1] = (0, 0, 0)
            dots[2] = (0, 0, 0)
            dots.show()

    try:
        with speech_recognition.Microphone(device_index=1) as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"recognized: {text}")
            if not activated:
                wakeword = text.find("okay computer")
                if wakeword >= 0:
                    activated = True
                    t_stop = time.time() + 5
                    dots[0] = (255, 0, 0)
                    dots[1] = (255, 0, 0)
                    dots[2] = (255, 0, 0)
                    dots.show()

            else:
                for i in tasks:
                    for j in i.words:
                        if text.find(j) >= 0:
                            i.callback()
                activated = False
                dots[0] = (0, 0, 0)
                dots[1] = (0, 0, 0)
                dots[2] = (0, 0, 0)
                dots.show()
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
        print("unrecognized")
        continue
