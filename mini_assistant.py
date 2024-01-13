import os

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

recognizer = sr.Recognizer()

engine = pyttsx3.init()


def speak_text(command):
    """
    Convert text to speech and play it back.
    :param command: Command to be spoken
    """
    engine.say(command)
    engine.runAndWait()


def record_text():
    """
    Record audio from microphone and return it as text.
    :return: Text from recorded audio
    """
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)
                text = recognizer.recognize_sphinx(audio)
                print(text)
                return text
        except sr.RequestError as e:
            print("Sorry, I did not get that.")
            print(e)
        except sr.UnknownValueError:
            print("Unknown error occurred")
            print(e)


def send_to_chatgpt(input_message):
    """
    Send text to chatGPT and return response.
    :param input_message: Text to send to chatGPT
    :return: Response from chatGPT
    """
    chatgpt_response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                      messages=[
                                                          {"role": "system", "content": "You are a helpful lovely assistant with UwU energy."},
                                                          {"role": "user", "content": input_message}
                                                      ],
                                                      temperature=0)
    return chatgpt_response.choices[0].message.content


while True:
    text = record_text()
    response = send_to_chatgpt(text)
    speak_text(response)
    print(response)
