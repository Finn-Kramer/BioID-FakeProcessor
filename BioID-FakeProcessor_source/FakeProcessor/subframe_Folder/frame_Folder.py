import threading
import time
from customtkinter import *
from tkinter import Canvas
from PIL import Image, ImageTk
from FakeProcessor.subframe_Folder.CreatePictures import ImgWindow
from FakeProcessor.BioID_HelpMethods.getApp import Page, CreateToolTip
from FakeProcessor.BioID_HelpMethods.getFiles import getDir, checkDirFiles
from FakeProcessor.BioID_HelpMethods.getFiles import PicCollector as pc
from FakeProcessor.subframe_Folder.StatusUpdate import StatusUpdate

pc = pc()


picsDone = False
collecting = False

class ID_Folder(Page):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)

        self.running = False

        self.buttonCheck = False
        self.configure(fg_color="gray10")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.update = StatusUpdate(self, fg_color="gray16", corner_radius=0)
        self.update.grid(row=0, column=1, sticky=NSEW)

        bg_frame = CTkFrame(self, fg_color="gray10")
        bg_frame.grid(row=0, column=0, sticky=NS)

        self.dirList = CTkFrame(bg_frame, fg_color="gray10")
        self.dirList.pack(side=LEFT, fill=Y)

        self.canvas = Canvas(self.dirList, width=200, height=1000, highlightthickness=0, bg="gray10", bd=0)
        self.canvas.pack(side=LEFT, fill=Y, padx=10, pady=10)

        v = CTkScrollbar(self.dirList, command=self.canvas.yview, fg_color="gray10")
        v.pack(side=LEFT, fill=Y)
        self.canvas.configure(yscrollcommand=v.set)
        self.canvas.bind('<Configure>', self.on_configure)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=(0,0,200,1800))

    def failedToLoadFolders(self):
        self.update.currentStatus.configure(text="Failed to load folders!")
        self.update.currentStatus.text = "Failed to load folders!"
        self.update.currentStatus.update()
        self.update.statusLabel.configure(text="Please make sure to select a valid Folder")
        self.update.statusLabel.text = "Please make sure to select a valid Folder"
        self.update.statusLabel.grid(row=3, column=0, sticky=EW)
        self.update.statusLabel.update()

    def failedReset(self):
        self.update.currentStatus.configure(text="Current Status:")
        self.update.currentStatus.text = "Current Status:"
        self.update.currentStatus.update()
        self.update.statusLabel.configure(text="")
        self.update.statusLabel.text = ""
        self.update.statusLabel.grid_forget()
        self.update.statusLabel.update()

    def getDirButtons(self):
        self.failedReset()
        self.buttonCheck = True
        Dirs = getDir()
        fDirs = getDir(True)
        self.buttons = []
        self.statuses = []

        self.scrollFrame = CTkFrame(self.canvas, fg_color="gray10")
        self.canvas.create_window((0, 0), width=200, window=self.scrollFrame, anchor='nw')

        if Dirs:
            for count in range(0, len(Dirs)):
                self.buttonFrame = CTkFrame(self.scrollFrame, height=25, width=180, fg_color="gray10")
                self.buttonFrame.pack(side=TOP, fill=X, expand=True, pady=5)
                ttp = CreateToolTip(self.buttonFrame, pos=(210,1), text=f"Start the picture taking process for the folder: \"{Dirs[count]}\" ")
                statusImg = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Error.png").resize((23, 23)))
                for fDir in fDirs:
                    if Dirs[count] in fDir and checkDirFiles(fDir) >= checkDirFiles(Dirs[count])-10:
                        statusImg = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Success.png").resize((23, 23)))
                self.status = CTkLabel(self.buttonFrame, height=23, width=23, image=statusImg)
                self.statuses.append(self.status)
                self.status.image = statusImg
                self.subDirButton = CTkButton(self.buttonFrame, text=Dirs[count], height=25, width=150, fg_color="#4b5f9c", hover_color="#b7bfd7")
                self.buttons.append(self.subDirButton)
                self.subDirButton.pack(side=LEFT, fill=Y, expand=True, padx=5, pady=5, anchor=W)
                self.status.pack(side=RIGHT, fill=X, expand=True, padx=5, pady=5)
                self.subDirButton.configure(command=lambda i=count: self.startProgress(self.buttons[i], self.statuses[i], Dirs[i]))
        else:
            Dirs = getDir()

    def remonveDirButtons(self):
        self.buttonCheck = False
        for b in self.buttons:
            b.pack_forget()
            b.destroy()
        for s in self.statuses:
            s.pack_forget()
            s.destroy()
        self.buttonFrame.pack_forget()
        self.buttonFrame.destroy()
        self.canvas.delete('all')

    def startProgress(self, b, s, folder):
        global picsDone
        for button in self.buttons:
            if button is not b:
                button.configure(state=DISABLED)
        self.update.resetProgress()
        statusImg = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Stop.png").resize((23, 23)))
        s.configure(image=statusImg)
        s.image = statusImg
        b.configure(command=lambda: self.stopProgress(b, s, folder))
        b.configure(text="Stop")
        b.configure(fg_color="#d75a4a", hover_color="#efbdb7")
        self.imgWin = ImgWindow(self, bg='gray14')
        picsDone = False
        self.update.setProgress(0.1, "starting Thread")
        time.sleep(1)
        if not self.running:
            self.t = threading.Thread(target=self.continueProgress, args=(b, s, folder))
            self.t.setDaemon(True)
            self.t.start()

    def continueProgress(self, b, s, folder):
        self.update.setProgress(0.2, "Please align your Camera")
        self.update.refCameraButton(b, s, folder, self)

    def openWin(self, b, s, folder):
        global picsDone, collecting
        self.running = True
        self.update.setProgress(0.3, "getting Starting Folder")
        time.sleep(1)
        if self.running:
            self.update.setProgress(0.4, "collecting Images from Folder")
            time.sleep(1)
        if self.running:
            collecting = True
            pc.getPics(folder, self.update)
            collecting = False
        if self.running:
            self.update.setProgress(0.6, "creating Fakes of Images")
            time.sleep(1)
            picsDone = True
            self.imgWin.startPic(folder, self.update)
        if self.running:
            self.update.setProgress(1.0, "____Done____")
            time.sleep(1)
            self.finishProgress(b, s, folder)

    def stopProgress(self, b, s, folder):
        global picsDone, collecting
        self.running = False
        self.update.stopCam()
        statusImg = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Error.png").resize((23, 23)))
        s.configure(image=statusImg)
        s.image = statusImg
        b.configure(command=lambda: self.startProgress(b, s, folder))
        b.configure(text=folder)
        b.configure(fg_color="#4b5f9c", hover_color="#b7bfd7")
        b.configure(state=DISABLED)
        if collecting:
            pc.stopPics()
        if not picsDone:
            self.imgWin.loopStatus = False
        self.imgWin.destroy()
        self.update.resetProgress()
        self.after(3000, self.activateButtons)

    def activateButtons(self):
        for button in self.buttons:
                button.configure(state=ACTIVE)
    def finishProgress(self, b, s, folder):
        self.running = False
        statusImg = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Success.png").resize((23, 23)))
        s.configure(image=statusImg)
        s.image = statusImg
        b.configure(command=lambda: self.startProgress(b, s, folder))
        b.configure(text=folder)
        b.configure(fg_color="#4b5f9c", hover_color="#b7bfd7")
        self.after(3000, self.activateButtons)
        self.imgWin.loopStatus = False
        self.imgWin.destroy()
        self.update.setProgress(1.0, "")



