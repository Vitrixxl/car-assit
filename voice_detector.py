import threading
from pydub import AudioSegment
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class VoiceDetector:
    def __init__(self,timeout=3):
        self.recognizer = sr.Recognizer()
        # self.timeout_duration = timeout_duration
        
        # Paramètres pour la détection de parole
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.8
        self.timeout = timeout
    
    def listen(self):
        self.listening = True
        
        # Démarrage du timer
        def return_false():
            return False

        self.timer = threading.Timer(self.timeout, return_false)
        self.timer.start()
        
        try:
            with sr.Microphone() as source:
                print("En attente de parole...")
                audio = self.recognizer.listen(source, timeout=self.timeout)
                
                # Si on a capté de l'audio, on annule le timer
                if self.timer:
                    self.timer.cancel()
                
                if audio:
                    return self.speech_to_text(audio)
                return False
                
        except sr.WaitTimeoutError:
            if self.timer:
                self.timer.cancel()
            return False
    def speech_to_text(self,audio):


        with open("output.wav", "wb") as audio_file:
            audio_file.write(audio.get_wav_data())
        audio_segment = AudioSegment.from_wav("output.wav")
        audio_segment.export("output.mp3", format="mp3")
        audio_file = open("./output.mp3","rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            language="fr",
            response_format="text",
                
        )
        if "Amara.org" in transcription or not transcription.strip():
            return False
        return transcription
        

def main():
    # Exemple d'utilisation

    detector = VoiceDetector(timeout =3)
    
    text = detector.listen()
    if text:
        print(text)
    else: 
        print("stopped because you didn't speak")
            
if __name__ == "__main__":
    main()
