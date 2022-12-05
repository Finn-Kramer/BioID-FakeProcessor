from FakeProcessor.MainWindow.App import ID_App
from FakeProcessor.BioID_HelpMethods.SettingParameter import loadSettings
from multiprocessing import freeze_support

if __name__ == '__main__':
    loadSettings()
    freeze_support()
    root = ID_App()
    root.iconbitmap("FakeProcessor/Icons/Camera.ico")
    root.mainloop()