# Rajyalakshmi, Farhan and Nikhil

# Import Libraries
from texttospeech import TTs
import speech_recognition as sr
from fbchat import Client
import time
from fbchat.models import *
from googletrans import Translator
import shutil
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
from google.cloud import translate
import sys
import maintts
from googlesearch import search
from googlesearch.googlesearch import GoogleSearch
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./ruuhvoicebot-5234ddadd06f.json"

# For emoji types
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)



# Facebook Login credentials
client = Client('farhan_mohammed98@outlook.com', 'Farhan @facebook')
num=1

# RUUH ID : 118809975300669

# Function to convert telugu text to english letters (Indic Transliteration)
def tel2eng(sentence, detected_lang):
    return transliterate(sentence, detected_lang, sanscript.ITRANS)

# Function to translate english to telugu
def translate_text(text, target):
    #print("translating into english")
    translate_client = translate.Client()
    result = translate_client.translate(text,target_language=target)
    result = translate_client.translate(text, target_language=target)
    #print(result['translatedText'])
    return result['translatedText']

def detect_language(text):
    # [START translate_detect_language]
    #Detects the text's language
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    print('Text: {}'.format(text))
    #print('Confidence: {}'.format(result['confidence']))
    #print('Language: {}'.format(result['language']))
    return result['language']
    # [END translate_detect_language]
#print(detect_language("నీవు ఏమి చేస్తున్నావు"))



# Main Code
def exec():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Say something : ')
        time.sleep(1)
        audio = r.listen(source)    
        result = r.recognize_google(audio)
        detected_lang = detect_language(result)
        print(detected_lang)
        if(detected_lang!="en"):
            result = translate_text(result,"en")
        if "search" in result:
            #print(result)
            search_pos = result.find("search") - 1
            srch_term=result[search_pos:]
            print(srch_term)
            search_status = maintts.ruuh_search(srch_term)
            if(search_status=="MainTTSDone"):
                print("re-execution")
                exec()
            file=open('word.txt','w')
            file.close()
            instr=result
            file=open('word.txt','a')
            file.write(instr)
            file.close()
        file = open("word.txt",'r')
        text=file.read()
        #print(text)
        file.close()
        client.send(Message(text), thread_id="118809975300669", thread_type=ThreadType.USER)
        time.sleep(8)
        messages = client.fetchThreadMessages(thread_id="118809975300669", limit=2)
        messages.reverse()
        print("\n")
        file1=open('tex.txt','w')
        file1.close()
        for message in messages:
            if(message.text!=text):
                voice=message.text
                #print(voice)
                voice_lol=voice
                voice_lol = translate_text(voice_lol,detected_lang)
                #print(voice_lol)
            messages=[]
            message=[]
        def write_lang(detected_lang):
            if(detected_lang=="te"):
               return sanscript.TELUGU
            elif(detected_lang=="en"):
                return sanscript.ITRANS
            elif(detected_lang=="hi"):
                return sanscript.DEVANAGARI
            elif(detected_lang=="kn"):
                return sanscript.KANNADA
            elif(detected_lang=="bn"):
                return sanscript.BENGALI
            elif(detected_lang=="ml"):
                return sanscript.MALAYALAM        
            else:
                return sanscript.ITRANS
        if(detected_lang!="en"):
            x = write_lang(detected_lang)
            voice_lol = tel2eng(voice_lol, x)
        print("final: ",voice_lol.translate(non_bmp_map))
        telugu = open('telugu.txt','w')
        telugu.close()
        #telugu=open('telugu.txt','a')
        #telugu.write(final)
        #telugu.close()

        with open('telugu.txt','a',encoding='utf-8') as telugu:
            telugu.write(voice_lol)
        TTs.savemp3(detected_lang)
        TTs.openmp3()
        time.sleep(5)
while(1):
    exec()
