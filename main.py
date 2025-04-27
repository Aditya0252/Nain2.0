
# import requests
# import speech_recognition as sr
# import pyttsx3
# from config import LLAMA_CPP_SERVER_URL, DEFAULT_MODEL_NAME

# SYSTEM_PROMPT = (
#     "Your name is leo and You're a friendly humanoid robot. Answer questions naturally, like a human friend, keeping responses clear, concise, and engaging for text-to-speech.\n"
# )

# engine = pyttsx3.init()
# engine.setProperty('rate', 170)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()

#     with mic as source:
#         print("\n🎤 Listening... (say 'exit' to quit)")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "Sorry, I didn't catch that."
#     except sr.RequestError:
#         return "Speech recognition service is unavailable."

# def generate_response(user_prompt, model_name=DEFAULT_MODEL_NAME):
#     url = f"{LLAMA_CPP_SERVER_URL}/v1/completions"
#     headers = {"Content-Type": "application/json"}
#     full_prompt = f"{SYSTEM_PROMPT}User: {user_prompt}\nAssistant:"
#     data = {
#         "model": model_name,
#         "prompt": full_prompt,
#         "max_tokens": 150,
#         "temperature": 0.7,
#         "stop": ["User:", "Assistant:"]
#     }

#     print("\n🔍 Sending prompt:", full_prompt)

#     try:
#         response = requests.post(url, headers=headers, json=data, timeout=10)
#         response.raise_for_status()
#         return response.json()["choices"][0]["text"].strip()
#     except Exception as e:
#         print("❌ Request failed:", e)
#         return "Sorry, failed to get a response from the model."

# def run_text_mode():
#     print("\n📝 Text Mode Activated. Type 'exit' to quit.")
#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Exiting.")
#             break
#         response = generate_response(user_input)
#         print("AI:", response)

# def run_voice_mode():
#     print("\n🎙️ Voice Mode Activated. Say 'exit' to quit.")
#     while True:
#         user_input = listen().lower()
#         print("You:", user_input)
#         if user_input in ["exit", "quit"]:
#             speak("Goodbye!")
#             print("👋 Exiting voice chat.")
#             break
#         response = generate_response(user_input)
#         print("AI:", response)
#         speak(response)

# if __name__ == "__main__":
#     print("\nWelcome! Choose interaction mode:\n1. Text\n2. Voice")
#     mode = input("Enter 1 or 2: ").strip()

#     if mode == "1":
#         run_text_mode()
#     elif mode == "2":
#         run_voice_mode()
#     else:
#         print("Invalid choice. Exiting.")

import requests
import speech_recognition as sr
import pyttsx3
from config import LLAMA_CPP_SERVER_URL, DEFAULT_MODEL_NAME

SYSTEM_PROMPT = "I'm Leo, a friendly robot. Reply naturally, like a friend, keeping answers short and engaging for speech."

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.stop()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("\n🎤 Listening... (say 'exit' to quit)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("I didn’t understand. Could you repeat that?")
        return ""
    except sr.RequestError:
        speak("Sorry, I can’t access the speech service.")
        return ""

def check_server():
    try:
        response = requests.get(f"{LLAMA_CPP_SERVER_URL}/v1/models", timeout=50)
        return response.status_code == 200
    except:
        return False

def generate_response(user_prompt, model_name=DEFAULT_MODEL_NAME):
    url = f"{LLAMA_CPP_SERVER_URL}/v1/completions"
    headers = {"Content-Type": "application/json"}
    full_prompt = f"{SYSTEM_PROMPT}\nUser: {user_prompt}\nAssistant:"
    data = {
        "model": model_name,
        "prompt": full_prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "stop": ["User:", "Assistant:"]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        print("❌ Request failed:", e)
        return "Sorry, I couldn't respond."

def run_text_mode():
    print("\n📝 Text Mode Activated. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting.")
            break
        response = generate_response(user_input)
        print("AI:", response)

def run_voice_mode():
    print("\n🎙️ Voice Mode Activated. Say 'exit' to quit.")
    while True:
        user_input = listen().lower()
        if not user_input:
            continue
        print("You:", user_input)
        if user_input in ["exit", "quit"]:
            speak("Goodbye!")
            print("👋 Exiting voice chat.")
            break
        speak("Let me think for a moment...")
        response = generate_response(user_input)
        print("AI:", response)
        speak(response)

if __name__ == "__main__":
    if not check_server():
        print("❌ LLM server is unreachable. Please check the server.")
        exit(1)
    try:
        print("\nWelcome! Choose interaction mode:\n1. Text\n2. Voice")
        mode = input("Enter 1 or 2: ").strip()
        if mode == "1":
            run_text_mode()
        elif mode == "2":
            run_voice_mode()
        else:
            print("Invalid choice. Exiting.")
    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully.")
        engine.stop()