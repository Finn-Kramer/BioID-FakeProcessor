from PIL import Image, ImageTk

class resizer():
    def __init__(self):
        super().__init__()
        # this is a placeholder

    def returnPPWH(self):
        global pW, pH
        return pW, pH

    def checkRootH(self, c):
        RHeight = c.winfo_height()
        return RHeight

    def checkRootW(self, c):
        RWidth = c.winfo_width()
        return RWidth

    def resizer(self, c, e, img, content, size):
        global pW, pH
        bg1 = img

        w, h = bg1.size
        if pH >= self.checkRootH(c) and pW <= self.checkRootW(c):
            ratio = w / h
            if (size != (1, 1)):
                pW, pH = size
            new_height = pH
            new_width = round(ratio * pH)
            resized_bg = bg1.resize((new_width, new_height))
            new_bg = ImageTk.PhotoImage(resized_bg)
            content.configure(image=new_bg)
            content.image = new_bg
            pW, pH = resized_bg.size
        else:
            ratio = h / w
            if (size != (1, 1)):
                pW, pH = size
            new_height = round(ratio * e.width)
            new_width = e.width
            resized_bg = bg1.resize((new_width, new_height))
            new_bg = ImageTk.PhotoImage(resized_bg)
            content.configure(image=new_bg)
            content.image = new_bg
            pW, pH = resized_bg.size
