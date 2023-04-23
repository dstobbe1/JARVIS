import speech_recognition
# import python_weather


# def weather():
#     with python_weather.Client(format=python_weather.IMPERIAL) as client:

#         # fetch a weather forecast from a city
#         weatherEdm = client.get("Edmonton")

#     # returns the current day's forecast temperature (int)
#         print(weatherEdm.current.temperature)


class KeyPhrase:
    def __init__(self, words, callback):
        self.words = words
        self.callback = callback
# test
# defTaskArr = [KeyPhrase("what's the weather", weather)]


recognizer = speech_recognition.Recognizer()
while True:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"recognized: {text}")
            print(text)
            # for phrase in defTaskArr:
            #     if phrase.words == text:
            #         phrase.callback()

    except speech_recognition.UnknownValueError:
        print("unknown value")
        recognizer = speech_recognition.Recognizer()
        continue


# import spotipy
# import json
# import webbrowser


# # Data to be written
# dictionary = {
#     "name": "sathiyajith",
#     "rollno": 56,
#     "cgpa": 8.6,
#     "phonenumber": "9976770500"
# }

# # Serializing json
# json_object = json.dumps(dictionary, indent=4)

# # Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)
