from FakeProcessor.BioID_HelpMethods.SettingParameter import getCords, setCords
import tkinter as tk

class FloatingWindow(tk.Toplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.saveX, self.saveY = getCords()

        self.overrideredirect(True)
        self.fullScreen = False
        self._offsetx = 0
        self._offsety = 0
        self._window_x = 500
        self._window_y = 100
        self._window_w = 750
        self._window_h = 1000
        if self.saveY == 0 and self.saveX == 0:
            self.geometry('{w}x{h}+{x}+{y}'.format(w=self._window_w, h=self._window_h, x=self._window_x, y=self._window_y))
        else:
            self.geometry('{w}x{h}+{x}+{y}'.format(w=self._window_w, h=self._window_h, x=self.saveX, y=self.saveY))
        self.bind('<Button-1>', self.clickwin)
        self.bind('<B1-Motion>', self.dragwin)
        self.bind("<F11>", self.toggleFullScreen)

    def dragwin(self, event):
        global savedY, savedX
        delta_x = self.winfo_pointerx() - self._offsetx
        delta_y = self.winfo_pointery() - self._offsety
        x = self._window_x + delta_x
        y = self._window_y + delta_y
        geometryLoc = "+{x}+{y}".format(x=x, y=y)
        self.geometry(str(geometryLoc))
        self._offsetx = self.winfo_pointerx()
        self._offsety = self.winfo_pointery()
        self._window_x = x
        self._window_y = y
        setCords(x, y)

    def clickwin(self, event):
        self._offsetx = self.winfo_pointerx()
        self._offsety = self.winfo_pointery()

    def toggleFullScreen(self, event):
        if self.fullScreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullScreen = True

        # Maximize window (Windows only). Optionally set screen geometry if you have it
        self.state("zoomed")

    def deactivateFullscreen(self):
        self.fullScreen = False
        self.state("normal")