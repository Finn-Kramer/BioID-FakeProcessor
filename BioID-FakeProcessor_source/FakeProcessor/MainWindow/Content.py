from customtkinter import *
from FakeProcessor.subframe_Folder.frame_Folder import ID_Folder
from FakeProcessor.subframe_Camera.frame_Camera import ID_Camera
from FakeProcessor.subframe_Settings.frame_Settings import ID_Settings
from FakeProcessor.subframe_StartPage.frame_StartPage import ID_StartPage

class ID_Content(CTkFrame):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)

        self.pageStart = ID_StartPage(self, fg_color='gray16')
        self.pageFolder = ID_Folder(self, fg_color='gray16')
        self.pageSettings = ID_Settings(self, fg_color='gray16')

        self.pageStart.place(in_=self, x=0, y=0, relwidth=1, relheight=1)

        self.pageStart.show()