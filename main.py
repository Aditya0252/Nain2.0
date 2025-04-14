# import requests
# from config import LLAMA_CPP_SERVER_URL, DEFAULT_MODEL_NAME

# # Set your system prompt here
# SYSTEM_PROMPT = (
#     "You are an intelligent assistant built to help users with their queries clearly and concisely. "
#     "Keep responses relevant to the user's questions and avoid unnecessary information.\n"
# )

# def generate_response(user_prompt, model_name=DEFAULT_MODEL_NAME):
#     """
#     Generate a response from the model using a system-level instruction and user input.
#     """
#     url = f"{LLAMA_CPP_SERVER_URL}/v1/completions"
#     headers = {"Content-Type": "application/json"}
    
#     # Combine system + user prompts
#     full_prompt = f"{SYSTEM_PROMPT}User: {user_prompt}\nAssistant:"
    
#     data = {
#         "model": model_name,
#         "prompt": full_prompt,
#         "max_tokens": 100,
#         "temperature": 0.7,
#         "stop": ["User:", "Assistant:"]
#     }
    
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#     return response.json()["choices"][0]["text"]

# # Start interactive chat
# if __name__ == "__main__":
#     while True:
#         user_prompt = input("You: ")
#         if user_prompt.lower() in ["exit", "quit"]:
#             print("Exiting chat.")
#             break
#         response_text = generate_response(user_prompt)
#         print("AI:", response_text.strip())
# Implementing voice based interaction




# import requests
# import speech_recognition as sr
# import pyttsx3
# from config import LLAMA_CPP_SERVER_URL, DEFAULT_MODEL_NAME

# # System-level behavior prompt
# SYSTEM_PROMPT = (
#     "You are an intelligent assistant built to help users with their queries clearly and concisely. "
#     "Keep responses relevant to the user's questions and avoid unnecessary information.\n"
# )

# # Text-to-Speech engine setup
# engine = pyttsx3.init()
# engine.setProperty('rate', 170)  # Speed of speech

# def speak(text):
#     """Convert text to voice."""
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     """Capture user voice input and convert to text."""
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()
    
#     with mic as source:
#         print("🎤 Listening... (say 'exit' to quit)")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
    
#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "Sorry, I didn't catch that."
#     except sr.RequestError:
#         return "Speech recognition service is unavailable."

# def generate_response(user_prompt, model_name=DEFAULT_MODEL_NAME):
#     """Generate a model response based on system + user prompt."""
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
    
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#     return response.json()["choices"][0]["text"]

# # 🔁 Voice-based conversation loop
# if __name__ == "__main__":
#     while True:
#         user_prompt = listen().lower()
        
#         if user_prompt in ["exit", "quit"]:
#             print("👋 Exiting voice chat.")
#             speak("Goodbye!")
#             break
        
#         print("You:", user_prompt)
#         response_text = generate_response(user_prompt).strip()
#         print("AI:", response_text)
#         speak(response_text)


import requests
import speech_recognition as sr
import pyttsx3
from config import LLAMA_CPP_SERVER_URL, DEFAULT_MODEL_NAME

SYSTEM_PROMPT = (
    "You are an intelligent assistant built to help users with their queries clearly and concisely. "
    "Keep responses relevant to the user's questions and avoid unnecessary information.\n"
)

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
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
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

def generate_response(user_prompt, model_name=DEFAULT_MODEL_NAME):
    url = f"{LLAMA_CPP_SERVER_URL}/v1/completions"
    headers = {"Content-Type": "application/json"}
    full_prompt = f"{SYSTEM_PROMPT}User: {user_prompt}\nAssistant:"
    data = {
        "model": model_name,
        "prompt": full_prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "stop": ["User:", "Assistant:"]
    }

    print("\n🔍 Sending prompt:", full_prompt)

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        print("❌ Request failed:", e)
        return "Sorry, failed to get a response from the model."

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
        print("You:", user_input)
        if user_input in ["exit", "quit"]:
            speak("Goodbye!")
            print("👋 Exiting voice chat.")
            break
        response = generate_response(user_input)
        print("AI:", response)
        speak(response)

if __name__ == "__main__":
    print("\nWelcome! Choose interaction mode:\n1. Text\n2. Voice")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        run_text_mode()
    elif mode == "2":
        run_voice_mode()
    else:
        print("Invalid choice. Exiting.")