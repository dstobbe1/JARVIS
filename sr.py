from keybert import KeyBERT
import wikipedia
# import speech_recognition

# recognizer = speech_recognition.Recognizer()
# while True:
#     try:
#         with speech_recognition.Microphone() as mic:

#             # recognizer.adjust_for_ambient_noise(mic, duration=0.2)
#             audio = recognizer.listen(mic)

#             text = recognizer.recognize_google(audio)
#             text = text.lower()
#             print(f"recognized: {text}")
#             keywords = KeyBERT().extract_keywords(
#                 text, keyphrase_ngram_range=(1, 2), stop_words='english')
#             print(keywords)
#             print(keywords[0][0])
#             print(wikipedia.summary(keywords[0][0], sentences=3))

#     except speech_recognition.UnknownValueError:
#         print("unknown value")
#         recognizer = speech_recognition.Recognizer()
#         continue
