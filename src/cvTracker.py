from functools import partial
import os
import threading
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import shutil
import time

__author__ = 'gipzo'


class CVTracker(threading.Thread):
    def __init__(self, **kwargs):
        super(CVTracker, self).__init__()
        self.layout = kwargs.get('layout')
        self.detect_face = True
        self.detect_mood = True
        self.is_training = False
        self.face_pos = None
        self.model_trained = False
        self.running = True
        self.mood_conv = {'1': 'disgust', '0': 'happy', '3': 'surprise', '2': 'sadness', '4': 'normal'}
        self.face_image = None
        self.setup_opencv()

    def set_texture(self, buf):
        Clock.schedule_once(partial(self.layout.set_texture, buf))

    def set_current_mood(self, mood, *largs):
        Clock.schedule_once(partial(self.layout.set_current_mood, mood))

    def setup_opencv(self):
        self.model = cv2.createEigenFaceRecognizer()
        self.vc = cv2.VideoCapture(0)
        self.faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_alt.xml")

        if os.path.isfile('data/model.xml'):
            self.model_trained = True
            self.model.load('data/model.xml')

    def init_learning(self, delete_old=True):
        if delete_old:
            shutil.rmtree('learning_data/')
            os.mkdir('learning_data/')
            for mood in self.moods:
                os.mkdir('learning_data/{}'.format(mood))
        self.face_found = False

    def run(self):
        while self.running:
            rval, frame = self.vc.read()
            gray_frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
            if self.is_training:
                gray_frame = cv2.resize(gray_frame, (0, 0), fx=1.0, fy=1.0)
            else:
                gray_frame = cv2.resize(gray_frame, (0, 0), fx=0.25, fy=0.25)
            faces = self.faceCascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.05,
                minNeighbors=4,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
            if len(faces) > 0:
                if self.detect_face:
                    self.face_pos = faces[0]

                (x, y, w, h) = self.face_pos
                self.face_image = gray_frame[y:y + h, x:x + w]
                self.face_image = cv2.resize(self.face_image, (100, 100), 0, 0)
                if self.detect_mood:
                    mood_label, cor = self.model.predict(self.face_image)
                    self.set_current_mood(self.mood_conv[str(mood_label)])
                buf1 = cv2.flip(self.face_image, 0)
                buf = buf1.tostring()
                self.set_texture(buf)