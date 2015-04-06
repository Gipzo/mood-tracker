# coding: utf-8
import subprocess
import time
import json
import urllib2
import random

URL = "http://127.0.0.1:8080/"

__author__ = 'gipzo'

speechkit_key = 'bf156666-b34a-4ad7-bfc4-9e2806491a0c'

phrases = [u'У тебя так%2bое настроение, что и матом не сформул%2bировать...',
           u'Даже если нет причины для смеха - смейся в кредит... ха ха хах',
       u'В каждом из нас заключено два человека, из которых один порицает то, что делает другой.',
   u'Нетерпимы будьте только к нетерпимости',
u'Чтобы всегда вставать с той ног%2bи, нужно у кровати оставлять один тапочек.',
u'Долой занудство и стандарт, в моей душе до смерти МАРТ!',
u'На вкус и цвет все фломастеры разноцветные.',
u'Не убивайте комаров! В них же течёт ваша кровь!',
u'Советую вам не следовать мо%2bим советам.']

def play_phrase(phrase, ind=0):
    phrase=phrase.replace(' ','%20')
    url = u'tts.voicetech.yandex.net/generate?good=good&text="{}"&format=mp3&lang=ru-RU&speaker=jane&key={}'.format(phrase, speechkit_key)
    print url
    subprocess.call(u"wget \"{}\" -O sound{}.mp3; afplay ./sound{}.mp3".format(url,ind,ind), shell=True)
    
def play_random_phrase():
    ind = random.randint(0, len(phrases)-1)
    play_phrase(phrases[ind], ind)

    
while True:
    data = json.load(urllib2.urlopen(URL))
    det_mood = data['data']['main_mood']
    print det_mood
    if det_mood < 0.3 or 1==1:
        play_random_phrase()
        time.sleep(20)
        
        
    time.sleep(1)
    
#set_mood('2')
