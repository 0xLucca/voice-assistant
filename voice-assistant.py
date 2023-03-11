import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import os

def transcribe_audio_to_test(filename):
    recognizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recognizer.record(source) 
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Error: Could not transcribe audio to text.")

def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
    )
    return response ["choices"][0]["text"]
    
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #Wait for user to say "genius"
        print("Say 'Genius' to start recording your question")
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            audio=recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="genius":
                    #Record audio
                    filename ="input.wav"
                    print("Say your question")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                            
                    #Transcript audio to test 
                    text=transcribe_audio_to_test(filename)
                    if text:
                        print(f"You said {text}")
                        
                        #Generate the response
                        response = generate_response(text)
                        print(f"The assistant said {response}")
                            
                        #Read the response out loud
                        speak_text(response)
            except Exception as e:  
                print("An error ocurred : {}".format(e))

if __name__=="__main__":
    load_dotenv()

    # Initialize OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the text to speech engine 
    engine=pyttsx3.init()

    main()
    
    
