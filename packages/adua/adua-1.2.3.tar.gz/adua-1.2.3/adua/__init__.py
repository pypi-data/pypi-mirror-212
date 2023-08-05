from craiyon import Craiyon
from translate import Translator
from langdetect import detect
from pyttsx3 import init
import speech_recognition as sr
import time
import os
import openai
import wikipedia
import wolframalpha
import webbrowser
class Adua:
    generator = Craiyon()
    engine=init('sapi5')
    voice=engine.getProperty('voices')
    def __init__(self,a:str="f"):
        if a=="m":
            self.engine.setProperty('voice', self.voice[0].id)
        if a=="f":
            self.engine.setProperty('voice', self.voice[1].id)
    def get_time(self):
        return time.localtime()
    def detect_lang(self,query):
        return detect(query)
    def translate(self,query,to_l='en'):
        t= Translator(to_lang=to_l)
        translation = t.translate(query)
        return translation
    def web_search(self,query,engin='g'):
        if engin=='b':
            webbrowser.open('https://www.bing.com/search?q={}'.format(query))
        elif engin=='g':
            webbrowser.open('https://www.google.co.in/search?q={}'.format(query))
        else:
            print('wrong engin')
            return 'wrong engin'
    def open_url(self,query):
        webbrowser.open(query)
    def wiki_search(self,query):
        search_results = wikipedia.search(query)
        result= wikipedia.summary(search_results[0])
        return result
    def get_ans(self,query):
        client=wolframalpha.Client('AYGGRU-P3473P9ETG')
        res=client.query(query)
        result=next(res.results).text
        return result
    def gen_img(self,query:str,path=None):
        result = self.generator.generate(query)
        if path==None:
            result.save_images()
        else:
            result.save_images(path)
    def gpt_img(self,a:str,api):
        openai.api_key = api
        response2 = openai.Image.create(
        prompt="a butterfly in ocean",
        n=1,
        size="1024x1024"
        )
        image_url = response2['data'][0]['url']
        return image_url
    def gpt_ans(self,query,api):
        try:
            openai.api_key = api
            start_sequence = "\nAdua:"
            restart_sequence = "\nYou: "
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" You:", " Adua:"]
            )
        except:
            print('wrong api key')
            return 'Wrong Api Key'
        return response.choices[0].text        
    def get_hour(self):
        t=time.localtime()
        hour=time.strftime("%H",t)
        ihour=int(hour)
        return ihour
    def getfiles(self,directory,only_name=False):
        # iterate over files in
        # that directory
        ld=[]
        ln=[]
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                ld.append(f)
                ln.append(filename)
        if only_name==True:
            return ln
        return ld
    def speak(self,audio):
        print('ADUA::'+ audio)
        self.engine.say(audio)
        self.engine.runAndWait()
    def listen(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold=1
            audio=r.listen(source)
        try:
            query=r.recognize_google(audio,language='en-in')
            print('User: '+query+ '\n')
        except sr.UnknownValueError:
            speak('Sorry Sir!,Can\'t get that! Try typing the command')
            query=str(input('Command: '))
        return query
    

    
if __name__=='__main__':
    a=Adua()
    print(a.get_ans('meaning of abhay'))


#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