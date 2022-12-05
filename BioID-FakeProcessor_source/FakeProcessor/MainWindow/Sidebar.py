from customtkinter import *
from PIL import Image, ImageTk

class ID_Sidebar(CTkFrame):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)

        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        start = CTkFrame(self)
        folder = CTkFrame(self)
        setting = CTkFrame(self)

        startCan = CTkCanvas(start, bg='gray18', width=50, height=50, highlightthickness=0)
        folderCan = CTkCanvas(folder, bg='gray18', width=50, height=50, highlightthickness=0)
        settingCan = CTkCanvas(setting, bg_='gray18', width=50, height=50, highlightthickness=0)

        startCan.pack(fill=BOTH, expand=True)
        folderCan.pack(fill=BOTH, expand=True)
        settingCan.pack(fill=BOTH, expand=True)

        start.grid(row=0, column=0, sticky=N, pady=10, padx=10)
        folder.grid(row=1, column=0, sticky=N, pady=10, padx=10)
        setting.grid(row=3, column=0, sticky=S, pady=10, padx=10)

        imgStart = ImageTk.PhotoImage(Image.open('FakeProcessor/Icons/Home.png').resize((40, 40)))
        self.imgStart = imgStart
        imgSettings = ImageTk.PhotoImage(Image.open('FakeProcessor/Icons/Settings.png').resize((40, 40)))
        self.imgSettings = imgSettings
        imgFolder = ImageTk.PhotoImage(Image.open('FakeProcessor/Icons/Folder.png').resize((40, 40)))
        self.imgFolder = imgFolder
        imgCamera = ImageTk.PhotoImage(Image.open('FakeProcessor/Icons/Camera.png').resize((40, 40)))
        self.imgCamera = imgCamera

        parent_name = self.winfo_parent()
        parent = self._nametowidget(parent_name)

        startButton = startCan.create_image(5, 5, image=imgStart, anchor='nw')
        startCan.tag_bind(startButton, "<Button-1>", parent.pageStart)
        folderButton = folderCan.create_image(5, 5, image=imgFolder, anchor='nw')
        folderCan.tag_bind(folderButton, "<Button-1>", parent.pageFolder)
        settingButton = settingCan.create_image(5, 5, image=imgSettings, anchor='nw')
        settingCan.tag_bind(settingButton, "<Button-1>", parent.pageSettings)

