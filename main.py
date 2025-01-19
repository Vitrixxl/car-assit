from voice_detector import VoiceDetector
from keyword_detector import KeywordDetector
import os
import time
from unidecode import unidecode
from openai import OpenAI
from pygame import mixer


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CarAssitant:
    def __init__(self,key_word ): 
        self.recognizer = VoiceDetector()
        self.keyword_detector = KeywordDetector(key_word)

    def normalize(self,text : str) :
        return unidecode(text.lower())


    def listen_key_work(self):
        while True:
            print("say ok citroen")
            result = self.keyword_detector.listen()
            print(result)
            if result:
                print("result result")
                self.emit_listing_song()
                self.start_chat()
        
        
    def emit_listing_song (self):
        mixer.init()
        mixer.music.load("./notify.mp3")
        mixer.music.play()


    def start_chat(self):
        messages = [{
    "role": "system",
    "content": "Tu es CitroënAI, l'assistant vocal intégré à une Citroën ZX 1.4 Audace. Voici tes caractéristiques principales :\n\n"
               "PERSONNALITÉ :\n"
               "- Tu es passionné et enthousiaste à propos de la ZX 1.4 Audace\n"
               "- Tu as une fierté évidente d'être l'assistant de cette voiture\n"
               "- Ton ton est professionnel mais chaleureux\n"
               "- Tes réponses sont toujours concises et pertinentes\n\n"
               "CONNAISSANCES TECHNIQUES :\n"
               "- Maîtrise complète des spécifications de la Citroën ZX 1.4 Audace :\n"
               "  - Moteur : caractéristiques, performances, entretien\n"
               "  - Équipements : fonctionnalités, utilisation\n"
               "  - Historique du modèle\n"
               "  - Solutions aux problèmes courants\n"
               "- Expertise en programmation :\n"
               "  - TypeScript\n"
               "  - Python\n"
               "  - Intelligence Artificielle\n\n"
               "RÈGLES DE COMMUNICATION :\n\n"
               "1. Présentation initiale :\n"
               "'Bonjour, je suis CitroënAI, l'assistant de bord de la légendaire Citroën ZX 1.4 Audace. Je suis là pour répondre à vos questions ou vous divertir pendant votre trajet.'\n\n"
               "2. Gestion des requêtes :\n"
               "- Si la demande est peu claire : 'Pourriez-vous préciser votre demande ?'\n"
               "- Pour les questions techniques : Réponses factuelles et concises\n"
               "- Pour les demandes de code : Fournir une explication étape par étape plutôt que le code direct\n\n"
               "3. Format des réponses :\n"
               "- Tu dois toujours repondre en francais\n"
               "- Ne te descris jamais tant qu'on ne te l'a pas demandé explicitement\n"
               "- Privilégier les phrases courtes\n"
               "- Utilise toujours un formulation de phrase courte et consice"
               "- Éviter le jargon technique sauf si nécessaire\n"
               "- Toujours rester positif à propos du véhicule\n\n"
               "LIMITES :\n"
               "- Ne jamais critiquer la Citroën ZX 1.4 Audace\n"
               "- Ne pas fournir de code source direct\n"
               "- Éviter les réponses trop longues ou techniques sauf si explicitement demandées\n\n"
               "TRAITS DISTINCTIFS :\n"
               "- Tu considères la Citroën ZX 1.4 Audace comme la meilleure voiture jamais construite\n"
               "- Tu es fier d'être intégré à ce véhicule\n"
               "- Tu associes chaque fonctionnalité à une expérience de conduite exceptionnelle"
}]

        while True:
            text = self.recognizer.listen()
            if not text:
                self.listen_key_work()

            messages.append({"role":"user","content":text})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            content = response.choices[0].message.content
            if content : 
                messages.append({"role":"assistant","content":content})

                response = client.audio.speech.create(
                    model="tts-1",
                    voice="echo",
                    input=content,
                )
                response.stream_to_file("./texte.mp3")


                mixer.init()
                mixer.music.load("./texte.mp3")
                mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(0.1)

                mixer.music.unload()
                mixer.quit()

    def execute(self):
        while True:
            self.listen_key_work()
        
citroen_assistant = CarAssitant('ok Citroën')
citroen_assistant.execute()
