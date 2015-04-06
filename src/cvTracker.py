from functools import partial
import glob
import os
import threading
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import shutil
import numpy as np
import time

__author__ = 'gipzo'


class CVTracker(threading.Thread):
    def __init__(self, **kwargs):
        super(CVTracker, self).__init__()
        self.layout = kwargs.get('layout')
        self.detect_face = True
        self.detect_mood = True
        self.is_training = False
        self.start_learning = False
        self.zoom = 0.1
        self.finish_learning = False

        self.next_step = False
        self.moods = ['happy', 'disgust', 'sadness', 'surprise', 'normal']
        self.learning_save_photo = False
        self.face_pos = None
        self.model_trained = False
        self.running = True
        self.current_mood = 'normal'
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
        self.model = cv2.createEigenFaceRecognizer()
        self.model.train(images, labels)
        self.model.save('data/model.xml')
        self.state = 'running'

    def do_save_photo(self):
        if self.face_image is not None:
            file_name = len(glob.glob('learning_data/{}/*.jpg'.format(self.current_mood))) + 1
            cv2.imwrite("learning_data/{}/{}.jpg".format(self.current_mood, file_name), self.face_image)
        pass


    def run(self):
        while self.running:
            rval, frame = self.vc.read()
            gray_frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
            if self.is_training:
                gray_frame = cv2.resize(gray_frame, (0, 0), fx=0.5, fy=0.5)
            else:
                gray_frame = cv2.resize(gray_frame, (0, 0), fx=0.5, fy=0.5)
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
                shift = int(w * self.zoom)
                self.face_image = gray_frame[y + shift:y + h - shift, x + shift:x + w - shift]
                self.face_image = cv2.resize(self.face_image, (100, 100), 0, 0)
                if self.detect_mood and not self.is_training:
                    mood_label, cor = self.model.predict(self.face_image)
                    self.set_current_mood(self.mood_conv[str(mood_label)])
                if self.is_training:
                    self.set_current_mood(self.current_mood)
                buf1 = cv2.flip(self.face_image, 0)
                buf = buf1.tostring()

                if self.start_learning:
                    print 'Start {}'.format(self.current_mood)
                    self.start_learning = False
                    self.is_training = True
                    self.init_learning()

                if self.finish_learning:
                    print 'Finish'
                    self.finish_learning = False
                    self.stop_learning()
                    self.is_training = False

                if self.next_step:
                    self.next_step = False
                    ind = self.moods.index(self.current_mood) + 1
                    if ind >= len(self.moods):
                        self.current_mood = self.moods[0]
                    else:
                        self.current_mood = self.moods[ind]

                    print 'Next step {}'.format(self.current_mood)

                if self.learning_save_photo:
                    print 'Saving'
                    self.learning_save_photo = False
                    self.do_save_photo()

                self.set_texture(buf)