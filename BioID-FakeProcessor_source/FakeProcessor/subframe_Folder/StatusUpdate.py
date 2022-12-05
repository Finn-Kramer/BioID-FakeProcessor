from FakeProcessor.BioID_HelpMethods.SettingParameter import getCamera
from FakeProcessor.subframe_Camera.LiveCamera import VideoCapture
from customtkinter import *
from tkinter import Label
from PIL import Image, ImageTk
import threading
import cv2

valueOld = True
stringOld = ""
double = False

class StatusUpdate(CTkFrame):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)
        self.count = 0
        self.labelList = []

        self.grid_rowconfigure(0, minsize=50)
        self.grid_columnconfigure(0, weight=1)

        self.progressBar = CTkProgressBar(self)

        self.statusLabel = Label(self, text="", justify=CENTER, bg="gray16", fg="gray90", font=("Arial", 9))

        self.progressFrame = CTkFrame(self, fg_color="gray10")

        self.progressFrame.grid_columnconfigure((0,1), weight=1)

        self.currentStatus = CTkLabel(self, height=80, text="Current Status:", text_font=("Arial", 16))
        self.currentStatus.grid(column=0, row=0)

        self.canvas = CTkCanvas(self, bg="gray16", highlightthickness=0)
        self.continueBtn = CTkButton(self, text="Continue")

        self.finishTime = CTkLabel(self, height=20, text="", text_font=("Arial", 9))
        self.finishTime.grid(column=0, row=5, padx=75, sticky=W)

    def refCameraButton(self, b, s, folder, parent):
        self.progressFrame.grid_forget()
        self.finishTime.grid_forget()
        self.canvas.grid(row=4, column=0, pady=10, padx=80, ipadx=80, sticky=NSEW)
        self.continueBtn.configure(command=lambda: self.refContinue(b, s, folder, parent))
        self.continueBtn.grid(column=0, row=5, sticky=E, padx=80)
        self.startCam()

    def refContinue(self, b, s, folder, parent):
        self.stopCam()
        if not self.progressFrame.winfo_ismapped():
            self.progressFrame.grid(row=4, column=0, pady=20, padx=75, ipadx=75, sticky=NSEW)
        self.finishTime.grid(column=0, row=5, padx=75, sticky=W)
        self.t = threading.Thread(target=parent.openWin, args=(b, s, folder))
        self.t.setDaemon(True)
        self.t.start()

    def setProgressValue(self, value):
        if not self.progressBar.winfo_ismapped():
            self.progressBar.set(0)
            self.progressBar.update()
            self.progressBar.grid(row=2, column=0, columnspan=2)
        self.progressBar.set(value)
        self.progressBar.update()

    def setWorkingOn(self, string="1. starting Thread", dub=False):
        global stringOld
        if not self.statusLabel.winfo_ismapped():
            self.statusLabel.grid(row=3, column=0, sticky=EW)
            stringOld = string
        self.statusLabel.configure(text=string + "...")
        print(string)
        if stringOld is not string and string and not dub:
            if not self.progressFrame.winfo_ismapped():
                self.progressFrame.grid(row=4, column=0, pady=20, padx=75, ipadx=75, sticky=NSEW)
            stringLabel = Label(self.progressFrame, text=stringOld + ":", justify=LEFT, bg="gray10", fg="gray90", font=("Arial", 9))
            success = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Success.png").resize((23,23)))
            stringIcon = Label(self.progressFrame, image=success, justify=RIGHT, bg="gray10")
            stringIcon.image = success
            stringLabel.grid(row=self.count, column=0, sticky=W)
            stringIcon.grid(row=self.count, column=1, sticky=E, pady=3, padx=10)
            self.labelList.append([stringLabel, stringIcon])
            stringOld = string
            self.count +=1

    def setProgress(self, value, string):
        self.setProgressValue(value)
        self.setWorkingOn(string)

    def setFinishTime(self, time):
        self.finishTime.configure(text="The Script is done at around {time}".format(time=time))

    def setDoubleProgress(self, value, string):
        self.setProgressValue(value)
        self.setWorkingOn(string, True)

    def resetProgress(self):
        global stringOld, valueOld
        for list in self.labelList:
            list[0].destroy()
            list[1].destroy()
        self.progressFrame.grid_forget()
        self.progressBar.grid_forget()
        self.statusLabel.configure(text="")
        self.finishTime.configure(text="")
        self.statusLabel.grid_forget()
        stringOld = "1. starting Thread"
        print("Reset Done")

    def startCam(self):
        self.vid = VideoCapture(getCamera())
        self.delay = 10
        self.update()

    def stopCam(self):
        if self.vid.vid.isOpened():
            self.vid.vid.release()
            cv2.destroyAllWindows()
        self.canvas.grid_forget()
        self.continueBtn.grid_forget()

    def update(self):
        if self.vid.vid.isOpened():
            ret, frame = self.vid.get_frame()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(10, 0, image=self.photo, anchor=NW)
            self.after(self.delay, self.update)
