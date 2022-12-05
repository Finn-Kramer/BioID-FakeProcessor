from customtkinter import *
from FakeProcessor.MainWindow.Sidebar import ID_Sidebar
from FakeProcessor.MainWindow.Content import ID_Content

class ID_App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("[BioID]: Fake Processor")
        self.resizable(False, False)

        self.sidebar = ID_Sidebar(self, width=80, fg_color='gray18')
        self.sidebar.pack(fill=Y, side=LEFT)

        self.content = ID_Content(self, fg_color='gray10')
        self.content.pack(fill=BOTH, expand=True, side=RIGHT)

    def pageStart(self, event):
        try:
            self.content.pageFolder.imgWin.destroy()
        except AttributeError:
            pass
        self.content.pageStart.place(in_=self.content, x=0, y=0, relwidth=1, relheight=1)
        self.content.pageStart.show()
        try:
            self.toplevel.destroy()
        except AttributeError:
            pass
        self.content.pageSettings.place_forget()
        self.content.pageFolder.place_forget()

    def pageFolder(self, event):
        if self.content.pageFolder.buttonCheck:
            try:
                self.content.pageFolder.remonveDirButtons()
            except AttributeError:
                pass
        self.content.pageFolder.place(in_=self.content, x=0, y=0, relwidth=1, relheight=1)
        try:
            self.content.pageFolder.getDirButtons()
        except FileNotFoundError:
            self.content.pageFolder.failedToLoadFolders()
            pass
        self.content.pageFolder.show()
        try:
            self.toplevel.destroy()
        except AttributeError:
            pass
        self.content.pageSettings.place_forget()
        self.content.pageStart.place_forget()

    def pageSettings(self, event):
        try:
            self.content.pageFolder.imgWin.destroy()
        except AttributeError:
            pass
        self.content.pageSettings.place(in_=self.content, x=0, y=0, relwidth=1, relheight=1)
        self.content.pageSettings.callButtons()
        self.content.pageSettings.show()
        try:
            self.toplevel.destroy()
        except AttributeError:
            pass
        self.content.pageFolder.place_forget()
        self.content.pageStart.place_forget()



