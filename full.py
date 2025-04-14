# import requests
# import speech_recognition as sr
# import pyttsx3
# import threading
# from config import LLAMA_CPP_SERVER_URL, DEFAULT_MODEL_NAME

# # System-level behavior prompt
# SYSTEM_PROMPT = (
#     "You are an intelligent assistant built to help users with their queries clearly and concisely. "
#     "Keep responses relevant and consider the ongoing conversation history for context.\n"
# )

# # Text-to-Speech setup
# engine = pyttsx3.init()
# engine.setProperty('rate', 170)

# stop_talking = False

# def speak(text):
#     """Speak text with interrupt capability."""
#     def run():
#         engine.say(text)
#         engine.runAndWait()
    
#     t = threading.Thread(target=run)
#     t.start()
    
#     while t.is_alive():
#         command = listen_interrupt()
#         if "stop" in command:
#             engine.stop()
#             print("🔇 Stopped speaking.")
#             break

# def listen():
#     """Listen for user query (full input)."""
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         print("🎤 Listening... (say 'exit' to quit)")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return ""
#     except sr.RequestError:
#         return "Speech recognition service unavailable."

# def listen_interrupt():
#     """Listen briefly for interrupt commands like 'stop'."""
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()
#     try:
#         with mic as source:
#             recognizer.adjust_for_ambient_noise(source, duration=0.2)
#             audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
#         return recognizer.recognize_google(audio).lower()
#     except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
#         return ""


# def generate_response(user_prompt, history, model_name=DEFAULT_MODEL_NAME):
#     """Generate a model response with conversational context."""
#     # Build prompt with history
#     context = SYSTEM_PROMPT
#     for pair in history:
#         context += f"User: {pair['user']}\nAssistant: {pair['assistant']}\n"
#     context += f"User: {user_prompt}\nAssistant:"

#     data = {
#         "model": model_name,
#         "prompt": context,
#         "max_tokens": 150,
#         "temperature": 0.7,
#         "stop": ["User:", "Assistant:"]
#     }

#     response = requests.post(a/
#         f"{LLAMA_CPP_SERVER_URL}/v1/completions",
#         headers={"Content-Type": "application/json"},
#         json=data
#     )
#     response.raise_for_status()
#     return response.json()["choices"][0]["text"].strip()

# def main():
#     mode = input("Choose mode - (1) Text (2) Voice: ").strip()
#     history = []

#     if mode == "1":
#         print("📝 Text mode activated. Type 'exit' to quit.")
#         while True:
#             user_input = input("You: ").strip()
#             if user_input.lower() in ["exit", "quit"]:
#                 print("👋 Exiting chat.")
#                 break
#             response = generate_response(user_input, history)
#             print("AI:", response)
#             history.append({"user": user_input, "assistant": response})

#     elif mode == "2":
#         print("🎙️ Voice mode activated. Say 'exit' to quit.")
#         while True:
#             user_input = listen().lower()
#             if "exit" in user_input:
#                 speak("Goodbye!")
#                 break
#             if not user_input:
#                 continue
#             print("You:", user_input)
#             response = generate_response(user_input, history)
#             print("AI:", response)
#             speak(response)
#             history.append({"user": user_input, "assistant": response})

#     else:
#         print("❌ Invalid selection. Restart the program.")

# if __name__ == "__main__":
#     main()
