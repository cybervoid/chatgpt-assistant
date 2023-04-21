import openai
import pyttsx3
import speech_recognition as sr
import time


openai.api_key=""
engine = pyttsx3.init()

def transcribe_audio_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except:
        print("Error")


def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text
    
def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("Testing")
    while True:
        print("Say 'genius' to start recording your question ...")
        with  sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription =  recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    print("Say your question...")

                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        source.pause_threshold = 1
                        audio = recognizer.listen(source)
                        with open("voice.wav", "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe recorded audio to text
                    text = transcribe_audio_to_text("voice.wav")
                    if text:
                        print("You said: {text}")

                        # generate response using chatgpt
                        response = generate_response(text)
                        print(response)
                        speak(response)

            except Exception as e:
                print(e)

        if text:
            print(text)
            response = generate_response(text)
            print(response)
            speak(response)
        else:
            print("No text")
            time.sleep(1)


if __name__ == "__main__":
    main()