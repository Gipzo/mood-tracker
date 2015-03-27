# coding: utf-8

import kivy
import cv2

from kivy.app import App
from kivy.config import Config
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '200')
Builder.load_file('data/main.kv')


class MoodTrackerLayout(BoxLayout):
    texture = ObjectProperty()

    def __init__(self, **kwargs):
        super(MoodTrackerLayout, self).__init__(**kwargs)
        self.vc = cv2.VideoCapture(0)
        self.texture = Texture.create(size=(100, 100), colorfmt='luminance')
        self.faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_alt.xml")
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def update(self, dt):
        rval, frame = self.vc.read()
        gray_frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
        gray_frame = cv2.resize(gray_frame, (0, 0), fx=0.25, fy=0.25)
        faces = self.faceCascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_image = gray_frame[y:y + h, x:x + w]
            face_image = cv2.resize(face_image, (100, 100), 0, 0)

            buf1 = cv2.flip(face_image, 0)
            buf = buf1.tostring()
            self.texture = Texture.create(size=(100, 100), colorfmt='luminance')
            self.texture.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')


class MoodTrackerApp(App):
    def build(self):
        self.layout = MoodTrackerLayout()
        return self.layout


if __name__ == '__main__':
    MoodTrackerApp().run()