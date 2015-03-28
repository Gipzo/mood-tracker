
from osascript import osascript
import time
import json
import urllib2

URL = "http://127.0.0.1:8080/"

def set_mood(mood):
    print 'Setting to {}'.format(mood)
    osascript("tell application \"Skype\"\n send command \"SET PROFILE MOOD_TEXT "+mood+"\" script name \"1\"  \n end tell")

mood_count=0
max_mood_count = 15
moods = {}
human_moods = {'happy': 'Im Happy',
                     'disgust': 'Not very good',
                     'sadness': 'So sad',
                     'surprise': 'OMG! WOW!',
                     'normal': 'meh...'}

while True:
    data = json.load(urllib2.urlopen(URL))
    det_mood = data['data']['detected_mood']
    print det_mood
    if det_mood in moods.keys():
        moods[det_mood]+=1
    else:
        moods[det_mood]=0
    mood_count +=1
    if mood_count >= max_mood_count:
        mood_count = 0
        m = 0
        print moods
        current_mood = 'normal'
        for mood, count in moods.iteritems():
            if count>m and mood != 'normal':
                current_mood = mood
                m=count
        
        if m>max_mood_count/3:
            set_mood(human_moods[current_mood])
        else:
            set_mood(human_moods['normal'])
        moods = {}
        
        
    time.sleep(1)

    
#set_mood('2')