import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Load the WAV audio file
audio_file = sr.AudioFile('your_file.wav')

# Recognize the content
with audio_file as source:
    audio = recognizer.record(source)

# Use Google Web Speech API to transcribe
try:
    text = recognizer.recognize_google(audio)
    print("Transcription: \n" + text)

except sr.UnknownValueError:
    print("Could not understand the audio.")
except sr.RequestError as e:
    print(f"Request error: {e}")
