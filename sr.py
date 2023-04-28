import speech_recognition
import time
import python_weather
import asyncio

recognizer = speech_recognition.Recognizer()


class KeyPhrase:
    def __init__(self, words, callback):
        self.words = words
        self.callback = callback


async def getweather():
    async with python_weather.Client() as client:
        weather = await client.get('Edmonton')
        print(weather.current.temperature)

tasks = [KeyPhrase("what's the weather", getweather)]

text = ''
activated = False

while True:
    if activated:
        if time.time() > t_stop:
            activated = False

    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"recognized: {text}")
            if not activated:
                jarvis = text.find("jarvis")
                if jarvis >= 0:
                    activated = True
                    t_stop = time.time() + 20
            else:
                if text == "what's the weather":
                    for i in tasks:
                        if text == i.words:
                            asyncio.run(i.callback())
                activated = False
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
        continue
