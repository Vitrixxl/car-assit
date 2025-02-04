from pydub.effects import normalize
from vosk import Model, KaldiRecognizer
from unidecode import unidecode
import pyaudio
import json

class KeywordDetector:
    def __init__(self, hotword="ok citroen"):
        # Charger le modèle français (à télécharger préalablement)
        self.model = Model("./venv/vosk-model-small-fr-0.22/vosk-model-small-fr-0.22")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.hotword = self.normalize(hotword)

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )

    def normalize(self,text : str) :
        return unidecode(text.lower())

    def listen(self):
        print("En écoute du mot clé...")
        self.stream.start_stream()

        while True:
            data = self.stream.read(4000)
            if len(data) == 0:
                break

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                print(f"result = {result}")
                text = self.normalize(result.get("text", "").lower())
                print(text)

                if self.hotword in text:
                    print("Mot clé détecté !")
                    return True

        return False

    def cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
