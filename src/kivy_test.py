# coding: utf-8
import glob
import json
import os

from kivy.support import install_twisted_reactor
from cvTracker import CVTracker

install_twisted_reactor()

import kivy
import cv2
import numpy as np

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty, Clock, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from twisted.internet import reactor
from twisted.web import server, resource
import sys
import shutil

Builder.load_file('data/main.kv')

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '200')


class Simple(resource.Resource):
    isLeaf = True
    moodTrackerLayout = None

    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        if self.moodTrackerLayout is not None:
            data = {
                'detected_mood': self.moodTrackerLayout.detected_mood,
                'current_mood': self.moodTrackerLayout.current_mood,
                'mood_coef': {
                    'happy': self.moodTrackerLayout.mood_stat['happy'],
                    'disgust': self.moodTrackerLayout.mood_stat['disgust'],
                    'sadness': self.moodTrackerLayout.mood_stat['sadness'],
                    'surprise': self.moodTrackerLayout.mood_stat['surprise'],
                    'normal': self.moodTrackerLayout.mood_stat['normal']
                }
            }
            return json.dumps({'data': data}, ensure_ascii=False, indent=2)
        return "{'data':false}"


class MoodTrackerLayout(BoxLayout):
    texture = ObjectProperty()

    happy_val = NumericProperty(0.0)
    disgust_val = NumericProperty(0.5)
    sadness_val = NumericProperty(0.75)
    surprise_val = NumericProperty(1.0)
    normal_val = NumericProperty(1.0)

    moods = ['happy', 'disgust', 'sadness', 'surprise', 'normal']
    mood_stat = {'happy': 0.0,
                 'disgust': 0.0,
                 'sadness': 0.0,
                 'surprise': 0.0,
                 'normal': 1.0}

    mood_inc = {'happy': 0.0,
                'disgust': 0.0,
                'sadness': 0.0,
                'surprise': 0.0,
                'normal': 0.0}

    mood_coef_inc = {'happy': 0.6,
                     'disgust': 0.6,
                     'sadness': 0.4,
                     'surprise': 1.0,
                     'normal': 0.6}

    mood_coef_dec = {'happy': 0.5,
                     'disgust': 0.5,
                     'sadness': 0.5,
                     'surprise': 0.5,
                     'normal': 0.2}

    face_pos = [0, 0, 0, 0]
    detect_face = BooleanProperty(True)
    status = StringProperty("")

    state = StringProperty("learning")

    # frame_scale = [0.25, 0.25]
    frame_scale = [1.0, 1.0]

    current_mood = StringProperty("normal")
    detected_mood = StringProperty("normal")

    def __init__(self, **kwargs):
        super(MoodTrackerLayout, self).__init__(**kwargs)

        self.cvTracker = CVTracker(layout=self)
        if self.cvTracker.model_trained:
            self.state = 'running'
        self.texture_buf=""
        res = Simple()
        res.moodTrackerLayout = self
        site = server.Site(res)
        reactor.listenTCP(8080, site)
        self.texture = Texture.create(size=(100, 100), colorfmt='luminance')
        Clock.schedule_interval(self.update, 1.0 / 33.0)
        Window.size = (500, 200)
        keyboard = Window.request_keyboard(self._keyboard_released, self)
        self._keyboard = keyboard
        keyboard.bind(on_key_down=self._keyboard_on_key_down)

        self.cvTracker.start()


    def _keyboard_released(self):
        self.focus = False

    def set_to_learning(self, *largs):
        self.cvTracker.init_learning()
        self.state = 'learning'

    def _keyboard_on_key_down(self, key, scancode, codepoint, modifier):
        code, key = scancode
        print key
        if key == '1':
            self.current_mood = 'happy'
        if key == '2':
            self.current_mood = 'disgust'
        if key == '3':
            self.current_mood = 'sadness'
        if key == '4':
            self.current_mood = 'surprise'
        if key == '5':
            self.current_mood = 'normal'
        if key == 'escape' and self.state is not 'learning':
            self.cvTracker.running = False
            App.get_running_app().stop()

        if key == 'escape' and self.state == 'learning':
            self.stop_learning()
        if key == 'spacebar' and self.state == 'learning':
            self.learning_next_step()
        if key == 's' and self.state == 'learning':
            self.learning_save_photo()
        return True

    def update_vals(self, dt):
        increase = 0.09

        cur_mood = self.current_mood.lower()
        self.mood_inc[cur_mood] += 0.02 * self.mood_coef_inc[cur_mood]

        for mood in self.moods:
            if mood != cur_mood:
                self.mood_inc[mood] -= 0.06 * self.mood_coef_dec[mood]
            if self.mood_inc[mood] < -self.mood_coef_dec[mood] * 0.1:
                self.mood_inc[mood] = -self.mood_coef_dec[mood] * 0.1
            if self.mood_inc[mood] > self.mood_coef_inc[mood]:
                self.mood_inc[mood] = self.mood_coef_inc[mood]
            self.mood_stat[mood] += self.mood_inc[mood]
            if self.mood_stat[mood] < 0.0:
                self.mood_stat[mood] = 0.0
                # self.mood_inc[mood] = 0.0
            if self.mood_stat[mood] > 1.0:
                self.mood_stat[mood] = 1.0
                self.mood_inc[mood] = 0.0

        self.happy_val = self.mood_stat['happy']
        self.disgust_val = self.mood_stat['disgust']
        self.sadness_val = self.mood_stat['sadness']
        self.surprise_val = self.mood_stat['surprise']
        self.normal_val = self.mood_stat['normal']

        max = 0.0
        for m, v in self.mood_stat.iteritems():
            if v > max:
                max = v
                self.detected_mood = m

        self.status = "Detected mood - {}, [{}]".format(self.detected_mood, self.current_mood)

    def learning_next_step(self):
        ind = self.moods.index(self.current_mood) + 1
        if ind >= len(self.moods):
            self.current_mood = self.moods[0]
        else:
            self.current_mood = self.moods[ind]

    def set_texture(self, buf, *largs):
        self.texture_buf = buf

    def set_current_mood(self, mood, *largs):
        self.current_mood = mood

    def update_learning(self, dt):
        self.status = "Learning: {}, Press S to save photo. Escape to stop learning.".format(self.current_mood)

    def learning_save_photo(self):
        if self.face_image is not None:
            file_name = len(glob.glob('learning_data/{}/*.jpg'.format(self.current_mood))) + 1
            cv2.imwrite("learning_data/{}/{}.jpg".format(self.current_mood, file_name), self.face_image)
        pass

    def stop_learning(self):
        images = []
        labels = []
        i = 0
        for mood in self.moods:
            onlyfiles = [f for f in os.listdir("learning_data/{}/".format(mood)) if
                         os.path.isfile(os.path.join("learning_data/{}/".format(mood), f))]
            for f in onlyfiles:
                if f[-3:] != 'jpg':
                    continue
                filename = "learning_data/{}/{}".format(mood, f)
                im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
                images.append(np.asarray(im, dtype=np.uint8))
                labels.append(i)
                self.mood_conv[str(i)] = mood
            i += 1
        labels = np.asarray(labels, dtype=np.int32)
        self.model.train(images, labels)
        self.model.save('data/model.xml')
        print self.mood_conv
        self.state = 'running'


    def update(self, dt):

        self.texture = Texture.create(size=(100, 100), colorfmt='luminance')
        self.texture.blit_buffer(self.texture_buf, colorfmt='luminance', bufferfmt='ubyte')
        if self.state == 'running':
            self.frame_scale = [0.25, 0.25]
            self.update_vals(dt)
        if self.state == 'learning':
            self.frame_scale = [0.5, 0.5]
            self.update_learning(dt)


class MoodTrackerApp(App):
    def build(self):
        self.layout = MoodTrackerLayout()
        return self.layout


if __name__ == '__main__':
    MoodTrackerApp().run()