import re
import time
from datetime import datetime, timedelta
from FakeProcessor.BioID_HelpMethods.SettingParameter import getStartPath, getFakeFolderName, getFakeImageName, getCamera
from customtkinter import *
from threading import Thread
from PIL import Image, ImageTk
from FakeProcessor.BioID_HelpMethods.getFiles import getDir, getDict, getLiveFake
from FakeProcessor.subframe_Folder.Toplevel import FloatingWindow
import cv2



class ImgWindow(FloatingWindow):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.loopStatus = False
        self.timeTaken=0

        self.picCanvas = CTkCanvas(self, bg="gray14", highlightthickness=0)
        self.picCanvas.pack(fill=BOTH, expand=True)
        height = 1000/2
        width = 750/2

        placeholder = ImageTk.PhotoImage(Image.open("FakeProcessor/Icons/Image.png"))
        self.placeholder = placeholder
        self.image = self.picCanvas.create_image(width, height, anchor=CENTER, image=placeholder, tags="bg_img")

    def startPic(self, folder, update):
        global loopStatus
        if self.parent.running:
            self.loopStatus = True
            time.sleep(1)
            t2 = Thread(target=self.goThroughPics, args=(folder, update))
            t2.setDaemon(True)
            t2.start()
            t2.join()

    def goThroughPics(self, folder, update):
        if self.parent.running:
            if getFakeFolderName() != "":
                fakeFolder = getFakeFolderName() + " " + folder + "_FAKE"
            else:
                fakeFolder = folder + "_FAKE"
            if not fakeFolder in getDir(True):
                update.setProgress(0.7, "create new Fake Folder")
                time.sleep(1)
                dir = os.path.join(getLiveFake(True), fakeFolder)
                print(dir)
                os.mkdir(dir)
            else:
                update.setProgress(0.7, "getting existing Folder")
        time.sleep(1)
        self.count = 1
        picList = getDict()[folder]
        if self.parent.running:
            update.setProgress(0.8, "shooting Fakes from Live Images")
        camera = cv2.VideoCapture(getCamera())
        for pic in picList:
            if self.loopStatus and self.winfo_exists():
                startTime = time.time()
                if self.parent.running:
                    update.setDoubleProgress(0.8, f"shooting Fakes from Live Images ({self.count}/{len(picList)})")
                file, name = pic
                if self.loopStatus and self.winfo_exists():
                    newImg = ImageTk.PhotoImage(file)
                    self.newImg = newImg
                    self.picCanvas.itemconfig(self.image, image=newImg)
                else:
                    return
                s, img = camera.read()
                if s:  # frame captured without any errors
                    if getFakeImageName() != "":
                        if "{}" in getFakeImageName():
                            img_name = "{dir}\\{name}.png".format(dir=getLiveFake(True) + "\\" + fakeFolder, name=getFakeImageName().format(self.count))
                        else:
                            img_name = "{dir}\\{name}.png".format(dir=getLiveFake(True) + "\\" + fakeFolder, name=getFakeImageName() + " {}".format(self.count))
                    else:
                        nameRe = re.search(r"\\([\w\d\-.,_]+)\.png", name)
                        img_name = "{dir}\\{name}.png".format(dir=getLiveFake(True) + "\\" + fakeFolder, name=str(nameRe.group(1)))
                    cv2.imwrite(img_name, img)
                    print(img_name + " written!...")
                    time.sleep(.3)
                if self.parent.running:
                    finishTime = self.calcAverageTime(time.time()-startTime, self.count, len(picList))
                    update.setFinishTime(f'{finishTime:%I:%M %p}')
                self.count += 1
            else:
                return
        camera.release()
        update.setProgress(0.9, "concluding Process")
        time.sleep(1)

    def calcAverageTime(self, time, count, all):
        self.timeTaken += time
        averTime = self.timeTaken/count
        remainsec = (averTime*all)-self.timeTaken
        now = datetime.now()
        now_plus = now + timedelta(minutes=round(remainsec / 60))
        return now_plus

