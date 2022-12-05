import tkinter as tk
from customtkinter import *
from tkinter import Pack, Grid, Place

class Page(CTkFrame):
    def __init__(self, c, **kwargs):
        super().__init__(c, **kwargs)
    def show(self):
        self.lift()

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    function by crxguy52 (https://stackoverflow.com/a/36221216)
    """
    def __init__(self, widget, pos=(25, 35), bg="gray22", text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 200   #pixels
        self.addx, self.addy = pos
        self.widget = widget
        self.text = text
        self.color = bg
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.addx
        y += self.widget.winfo_rooty() + self.addy
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget, bg=self.color, bd=0)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, bd=0, fg="gray90",justify='left', bg=self.color, relief='solid',
                       wraplength = self.wraplength)
        label.pack(ipadx=5, ipady=5)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class ScrolledText(CTkTextbox):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.frame = CTkFrame(master)
        self.vbar = CTkScrollbar(self.frame, fg_color="gray16")
        self.vbar.pack(side=RIGHT, fill=Y)

        kw.update({'yscrollcommand': self.vbar.set})
        CTkTextbox.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(CTkTextbox).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)