import requests
import speech_recognition
import time
import subprocess
import board
import adafruit_dotstar
import os
from ctypes import *
from contextlib import contextmanager

DOTSTAR_DATA = board.D5
DOTSTAR_CLOCK = board.D6
dots = adafruit_dotstar.DotStar(DOTSTAR_CLOCK, DOTSTAR_DATA, 3, brightness=0.2)


def showdots(rgb):
    for i in range(len(dots)):
        dots[i] = (rgb[0], rgb[1], rgb[2])
    dots.show()


text = ''


class KeyPhrase:
    def __init__(self, words, callback):
        self.words = words
        self.callback = callback


def getweather():

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = os.getenv('WEATHER_KEY')
    print(API_KEY)
    CITY = "Edmonton"

    url = BASE_URL + "appid=" + "8086e7ac6aca55da6f5a61ecf8149805" + "&q=" + CITY
    response = requests.get(url).json()

    temp = round(response['main']['temp'] - 273.15)
    feels_like = round(response['main']['feels_like'] - 273.15)
    description = response['weather'][0]['description']
    high = round(response['main']['temp_max'] - 273.15)
    low = round(response['main']['temp_min'] - 273.15)

    if text.find("temperature") >= 0:
        textToSpeach(f'"the temperature in edmonton is {temp} degrees"')
    elif text.find("weather") >= 0:
        textToSpeach(
            f'"It is currently {temp} but feels like {feels_like} degrees, with {description}"')
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


ERROR_HANDLER_FUNC = CFUNCTYPE(
    None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


activated = False
with noalsaerr():
    while True:
        recognizer = speech_recognition.Recognizer()
        if activated:
            if time.time() > t_stop:
                activated = False
                showdots([0, 0, 0])
        with speech_recognition.Microphone(device_index=0, sample_rate=48000) as source:

            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"recognized: {text}")
            if not activated:
                wakeword = text.find("okay computer")
                if wakeword >= 0:
                    activated = True
                    t_stop = time.time() + 5
                    showdots([255, 0, 0])
            else:
                for i in tasks:
                    for j in i.words:
                        if text.find(j) >= 0:
                            i.callback()
                activated = False
                showdots([0, 0, 0])
        except speech_recognition.UnknownValueError:
            print("unrecognized")
            continue
