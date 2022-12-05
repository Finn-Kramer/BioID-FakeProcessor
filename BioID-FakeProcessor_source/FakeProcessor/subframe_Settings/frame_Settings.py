from customtkinter import *
from FakeProcessor.BioID_HelpMethods.getApp import Page, CreateToolTip
from PIL import Image, ImageTk
from FakeProcessor.BioID_HelpMethods.SettingParameter import *
from tkinter import filedialog as fd
from tkinter import Label
from threading import Thread
import cv2

class ID_Settings(Page):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)
        self.ports = None

        self.top = CTkFrame(self, fg_color="gray16")
        self.left = CTkFrame(self, fg_color="gray16")
        self.right = CTkFrame(self, fg_color="gray16")

        self.grid_rowconfigure((0,1), weight=0)
        self.grid_columnconfigure((0,1), weight=1)

        self.top.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        self.left.grid(row=1, column=0, sticky=NSEW)
        self.right.grid(row=1, column=1, sticky=NSEW)

        self.top.grid_rowconfigure((0,1,2), weight=0)
        self.top.grid_columnconfigure((0), weight=1)

        self.left.grid_rowconfigure((0, 1), weight=0)
        self.left.grid_columnconfigure(0, weight=1)
        self.right.grid_rowconfigure((0,1), weight=0)
        self.right.grid_columnconfigure(0, weight=1)

        titleLabel = CTkLabel(self.top, text="Settings", height=80, text_font=("Arial", 16))
        titleLabel.grid(row=0, column=0, sticky=NSEW)

        t3 = Thread(target=self.list_ports)
        t3.setDaemon(True)
        t3.start()

    def callButtons(self):
        # Save Buttons
        buttonFrame = CTkFrame(self.top, width=400)
        saveButton = CTkButton(buttonFrame, text="Save Settings", command=lambda: saveSettings())
        defaultButton = CTkButton(buttonFrame, text="Save Default Settings", command=lambda: saveDefaultSettings())
        resetButton = CTkButton(buttonFrame, text="Reset Settings", command=lambda: resetSettings())

        buttonFrame.grid(row=1, column=0)
        saveButton.grid(row=1, column=0, sticky=E)
        defaultButton.grid(row=1, column=1, padx=10)
        resetButton.grid(row=1, column=2, sticky=W)

        self.top.grid_rowconfigure(2, minsize=50)

        # startPath
        startPathFrame = CTkFrame(self.top, fg_color="gray16")
        startPathFrame.grid(row=3, column=0)
        folderImg = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Folder.png").resize((25, 25)))
        self.startPathButton = CTkButton(startPathFrame, width=30, height=30, image=folderImg, text="", command=self.getDirectory, fg_color="gray16")
        startPathFrame_ttp = CreateToolTip(startPathFrame, pos=(445, 1), bg="gray10", text="set the Folder Path!")
        self.startPathInput = CTkEntry(startPathFrame, height=30, width=400, placeholder_text=getStartPath())
        self.startPathInput.bind('<Return>', self.changeStartPath)
        self.startPathButton.grid(row=0, column=0, sticky=E)
        self.startPathInput.grid(row=0, column=1, sticky=EW, padx=5)
        self.top.grid_rowconfigure(4, minsize=30)
        # webcam
        webcamFrame = CTkFrame(self.right, fg_color="gray16")
        webcamFrame.grid(row=0, column=0, sticky=W, padx=30)
        webcamFrame_ttp = CreateToolTip(webcamFrame, pos=(210, 23), bg="gray10", text="Choose a camera you want to use! \nBy default it is always the first Camera")
        self.webcamLabel = Label(webcamFrame, text="Webcam: ", bg="gray16", justify=LEFT, fg="gray90", font=("Arial", 10))
        self.webcamLabel.pack(side=TOP, anchor=W, pady=5)
        self.webcamBox = CTkComboBox(webcamFrame, values=["Default"], command=self.chooseWebcam, corner_radius=5, border_width=0,
                                       dropdown_color="gray90",
                                       dropdown_text_color="black",
                                       dropdown_hover_color="gray41",
                                       hover=False)
        self.refreshCam()
        self.webcamBox.pack(side=TOP, fill=X, anchor=E)

        # prevWin
        prevFrame = CTkFrame(self.right, fg_color="gray16")
        prevFrame.grid(row=1, column=0, sticky=W, padx=25, pady=15)
        if getPrevWin():
            value = "on"
        else:
            value = "off"
        switchVar = StringVar(value=value)
        prevFrame_ttp = CreateToolTip(prevFrame, pos=(190, -10), bg="gray10",
                                        text="Choose weather to display a popout when you get the camera preview")
        self.prevLabel = Label(prevFrame, text="Preview Window:", bg="gray16", justify=LEFT, fg="gray90", font=("Arial", 10))
        self.prevSwitch = CTkSwitch(prevFrame, text="", variable=switchVar, offvalue="off", onvalue="on", command=self.switchToplevel)
        self.prevLabel.pack(side=LEFT, fill=X)
        self.prevSwitch.pack(side=RIGHT, fill=X, padx=15, anchor=E)

        # Image Folder
        imageFrame = CTkFrame(self.left, fg_color="gray16")
        imageFrame.grid(row=1, column=0, pady=30, sticky=NSEW, padx=25)
        imageFrame_ttp = CreateToolTip(imageFrame, pos=(-120, 23), bg="gray10",
                                        text="Choose a Name for the Fake images! You can chose where to put the number by adding \"{}\" somewhere in the Name")
        self.imageLabel = Label(imageFrame, text="Fake Image Label", bg="gray16", justify=RIGHT, fg="gray90",
                                 font=("Arial", 10))
        self.imageLabel.pack(side=TOP, anchor=E, pady=5)
        self.imageInput = CTkEntry(imageFrame, height=30, width=190, placeholder_text=getFakeImageName())
        self.imageInput.bind('<Return>', self.changeImage)
        self.imageInput.pack(side=TOP, anchor=E)

        # Fake Folder
        folderFrame = CTkFrame(self.left, fg_color="gray16")
        folderFrame.grid(row=0, column=0, pady=10, sticky=NSEW, padx=25)
        folderFrame_ttp = CreateToolTip(folderFrame, pos=(-120, 23), bg="gray10",
                                        text="Create a prefix for the folder you want to save the Fake pictures to! The folder will look like this: \n\"{Your Name} digi123-45_FAKE\"")
        self.folderLabel = Label(folderFrame, text="Fake Folder Prefix", bg="gray16", justify=RIGHT, fg="gray90",
                                 font=("Arial", 10))
        self.folderLabel.pack(side=TOP, anchor=E, pady=5)
        self.folderInput = CTkEntry(folderFrame, height=30, width=190, placeholder_text=getFakeFolderName())
        self.folderInput.bind('<Return>', self.changeFolder)
        self.folderInput.pack(side=TOP, anchor=E)

        '''# Width
        widthFrame = CTkFrame(self.right, fg_color="gray16")
        widthFrame.grid(row=2, column=0, pady=30, sticky=W, padx=25)
        widthFrame_ttp = CreateToolTip(widthFrame, pos=(210, 7), bg="gray10",
                                        text="Choose a camera you want to use! \nBy default it is always the first Camera")
        self.widthLabel = Label(widthFrame, text="Image Width: {}".format(getPicWidth()), bg="gray16", justify=LEFT, fg="gray90",
                                 font=("Arial", 10))
        self.widthLabel.pack(side=TOP, anchor=W, pady=5)
        slideVar = IntVar(value=getPicWidth())
        self.widthSlider = CTkSlider(widthFrame, variable=slideVar, from_=0, to=1000, number_of_steps=10, command=self.changeWidth)
        self.widthSlider.pack(side=TOP, anchor=W)'''

    '''def changeWidth(self, value):
        setPicWidth(int(value))
        self.widthLabel.configure(text="Image Width: {}".format(int(getPicWidth())))'''

    def changeImage(self, e):
        text = self.imageInput.get()
        setFakeImageName(text)
        self.imageInput.configure(placeholder_text=text)
        self.imageInput.delete(0, 'end')
        self.imageLabel.focus_set()

    def changeFolder(self, e):
        text = self.folderInput.get()
        setFakeFolderName(text)
        self.folderInput.configure(placeholder_text=text)
        self.folderInput.delete(0, 'end')
        self.folderLabel.focus_set()

    def switchToplevel(self):
        value = self.prevSwitch.get()
        if value == "on":
            setPrevWin(True)
        else:
            setPrevWin(False)

    def refreshCam(self):
        self.webcams = []
        webnames = []
        for w in range(0, len(self.ports)):
            self.webcams.append(["Camera " + str(w + 1), self.ports[w]])
            webnames.append("Camera " + str(w + 1))
        self.webcamBox.configure(values=webnames)

    def changeStartPath(self, e):
        text = self.startPathInput.get()
        text = text.replace('/', '\\')
        setStartPath(text)
        self.startPathInput.configure(placeholder_text=text)
        self.startPathInput.delete(0, 'end')
        self.startPathButton.focus_set()

    def chooseWebcam(self, webcam):
        for list in self.webcams:
            if webcam == list[0]:
                setCamera(list[1])

    def getDirectory(self):
        foldername = fd.askdirectory(
            title='Open a directory',
            initialdir=getStartPath())
        foldername = foldername.replace('/', '\\')
        setStartPath(foldername)
        self.startPathInput.configure(placeholder_text=foldername)
        self.startPathInput.update()

    def list_ports(self):
        """
        Test the ports and returns a tuple with the available ports and the ones that are working.
        """
        non_working_ports = []
        dev_port = 0
        working_ports = []
        while len(non_working_ports) < 4:  # if there are more than 5 non working ports stop the testing.
            camera = cv2.VideoCapture(dev_port)
            if not camera.isOpened():
                non_working_ports.append(dev_port)
            else:
                is_reading, img = camera.read()
                w = camera.get(3)
                h = camera.get(4)
                if is_reading:
                    working_ports.append(dev_port)
            dev_port += 1
        self.ports = working_ports

