from ibm_watson import NaturalLanguageUnderstandingV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, EntitiesOptions, KeywordsOptions
from google.cloud import translate_v2
import os
from time import sleep


def main():
    text = ""
    while len(text) < 13:
        text = input("Digite o comentário: ")
        if len(text) < 13:
            print("Numero de caracteres insuficiente.")
    return text


def googleTranslator():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Diretório para as credenciais do Google" #Mudar aqui
    translate_client = translate_v2.Client()
    text = main() 
    target = "en"
    output = translate_client.translate(
        text,
        source_language='pt',
        target_language=target
    )
    return str(output["translatedText"])



def watson():
    try:
        text = googleTranslator()
        authenticator = IAMAuthenticator(
            'Sua API KEY do Watson NLU') #Mudar aqui
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2020-11-11',
            authenticator=authenticator
        )

        natural_language_understanding.set_service_url(
            'URL') #Mudar aqui

        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                keywords=KeywordsOptions(emotion=True, sentiment=True,
                                    limit=2))).get_result()

        if not response["keywords"] == []:
            if not response["keywords"][0] == []:
                label = response["keywords"][0]["sentiment"]["label"]
                anger = response["keywords"][0]["emotion"]["anger"]
                disgust = response["keywords"][0]["emotion"]["disgust"]
                sadness = response["keywords"][0]["emotion"]["sadness"]
            person = []

            if not response["entities"] == []:
                person = response["entities"][0]["type"]
                name = response["entities"][0]["text"]
                if person == "Person":
                    print(f"Foi detectado que {name} é uma pessoa.")
                    if person == "Person" and label == "negative":
                        if anger > 0.74:
                            print(f"Você possivelmente ofendeu {name}.")
                        elif anger > 0.55 and disgust > 0.7:
                            print(f"Você possivelmente ofendeu {name}.")
                        elif anger > 0.6 or disgust > 0.7:
                            print(f"Você possivelmente ofendeu {name}.")
                        elif anger > 0.4 and disgust > 0.5:
                            print(f"Você possivelmente ofendeu {name}.")
                        elif anger > 0.43 and disgust > 0.38 and sadness > 0.31:
                            print(f"Você possivelmente ofendeu {name}.")
                    else:
                        print("Seu comentário aparentemente não é tóxico.")
            if label == "negative" and sadness > 0.7:
                print("Você está bem? Parece deprimido(a).")
            elif label == "negative" and response["entities"] == []:
                if anger > 0.74:
                    print(f"Você possivelmente ofendeu alguem.")
                elif anger > 0.55 and disgust > 0.7:
                    print(f"Você possivelmente ofendeu alguem.")
                elif anger > 0.6 or disgust > 0.7:
                    print(f"Você possivelmente ofendeu alguem.")
                elif anger > 0.4 and disgust > 0.5:
                    print(f"Você possivelmente ofendeu alguem.")
                elif anger > 0.43 and disgust > 0.38 and sadness > 0.31:
                    print(f"Você possivelmente ofendeu alguem.")
                else:
                    print("Seu comentário aparentemente não é tóxico.")
        else:
            print("Watson falhou em interpretar.")
        sleep(6)
        os.system("cls")
    except:
        print("Watson não detectou o idioma, muitos caracteres aleatórios.")
        sleep(3)
        os.system("cls")
        pass

while True:
    watson()
