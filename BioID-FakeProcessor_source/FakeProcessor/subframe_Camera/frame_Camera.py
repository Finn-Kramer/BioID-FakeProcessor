from __future__ import print_function
from customtkinter import *
from FakeProcessor.BioID_HelpMethods.SettingParameter import getCamera
from FakeProcessor.subframe_Camera.LiveCamera import VideoCapture
from FakeProcessor.BioID_HelpMethods.getApp import Page
from PIL import Image, ImageTk
from threading import Thread
import cv2


class ID_Camera(Page):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.preview = CTkLabel(self, height=80, text="Camera Preview", text_font=("Arial", 16))
        self.preview.grid(row=0, column=0)

        self.canvas = CTkCanvas(self, bg="gray16", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky=NSEW)

    def startCam(self):
        self.vid = VideoCapture(getCamera())
        self.delay = 10
        self.pt = Thread(target=self.update)
        self.pt.setDaemon(True)
        self.pt.start()

    def stopCam(self):
        if self.vid.vid.isOpened():
            self.vid.vid.release()
            cv2.destroyAllWindows()

    def update(self):
        if self.vid.vid.isOpened():
            ret, frame = self.vid.get_frame()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(40, 0, image=self.photo, anchor=NW)
            self.after(self.delay, self.update)

