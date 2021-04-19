import time

import gi
import os
import threading
import urllib.request

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk
from gi.repository.GdkPixbuf import Pixbuf
from urllib.request import urlopen

LOCALFILE = 1
URLFILE = 0


class App:
    __urlColorize = None
    __urlSuperResolution = None
    __urlWaifu2x = None
    __urlToonify = None
    __textNeuralTalk = None
    __filePath = None
    __builder = None
    __lblOrig = None
    __lblRes = None
    __lblNeural = None
    __btnConvert = None
    __btnSave = None
    __imgOrig = None
    __imgRes = None
    __window = None
    __saveDialog = None
    __textEntry = None
    __fileSelector = None
    __imgOrigContainer = None
    __imgResContainer = None
    __apiKey = '9d023634-de61-4d54-a293-90bd5ccb78f9'

    def __init__(self, gladefile):
        builder = Gtk.Builder()
        builder.add_from_file(gladefile)
        builder.connect_signals(self)

        self.__saveDialog = builder.get_object("saveDialog")
        self.__lblOrig = builder.get_object("lblOrig")
        self.__lblRes = builder.get_object("lblRes")
        self.__lblNeural = builder.get_object("lblNeural")
        self.__imgOrig = builder.get_object("imgOrig")
        self.__imgRes = builder.get_object("imgRes")
        self.__btnConvert = builder.get_object("btnConvert")
        self.__btnSave = builder.get_object("btnSave")
        self.__fileSelector = builder.get_object("fileSelector")
        self.__window = builder.get_object("window")
        self.__imgResContainer = builder.get_object('imgResContainer')
        self.__imgOrigContainer = builder.get_object('imgOrigContainer')
        self.__textEntry = builder.get_object('textEntry')

        self.__btnConvert.set_sensitive(False)
        self.__btnSave.set_sensitive(False)
        self.__imgRes.clear()
        self.__imgOrig.clear()
        self.__window.set_icon_from_file("icon.png")


    def adjustImage(self, containerWidget, imgWidget, path):
        allocation = containerWidget.get_allocation()
        desired_width = allocation.width
        desired_height = allocation.height
        pixbuf = Pixbuf.new_from_file(path)
        pixbuf = pixbuf.scale_simple(desired_width, desired_height, 2)
        imgWidget.set_from_pixbuf(pixbuf)

    def toonify(self, option, path):
        import requests
        print("Toonification in process...")
        if option == URLFILE:
            r = requests.post(
                "https://api.deepai.org/api/waifu2x",
                data={
                    'image': path,
                },
                headers={'api-key': self.__apiKey}
            )
            print(r.json())
            self.__urlToonify = r.json()['output_url']
        else:
            if option == LOCALFILE:
                r = requests.post(
                    "https://api.deepai.org/api/toonify",
                    files={
                        'image': open(path, 'rb'),
                    },
                    headers={'api-key': self.__apiKey}
                )
                print(r.json())
                self.__urlToonify = r.json()['output_url']
            else:
                print("File mode for Toonification error")

    def waifu2x(self, option, path):
        import requests
        print("Waifu2x in process...")
        if option == URLFILE:
            r = requests.post(
                "https://api.deepai.org/api/waifu2x",
                data={
                    'image': path,
                },
                headers={'api-key': self.__apiKey}
            )
            print(r.json())
            self.__urlWaifu2x = r.json()['output_url']
        else:
            if option == LOCALFILE:
                r = requests.post(
                    "https://api.deepai.org/api/waifu2x",
                    files={
                        'image': open(path, 'rb'),
                    },
                    headers={'api-key': self.__apiKey}
                )
                print(r.json())
                self.__urlWaifu2x = r.json()['output_url']
            else:
                print("File mode for Waifu2x error")


    def colorize(self, option, path):
        import requests
        print("Colorization in process...")
        if option == URLFILE:
            r = requests.post(
                "https://api.deepai.org/api/colorizer",
                data={
                    'image': path,
                },
                headers={'api-key': self.__apiKey}
            )
            print(r.json())
            self.__urlColorize = r.json()['output_url']
        else:
            if option == LOCALFILE:
                r = requests.post(
                    "https://api.deepai.org/api/colorizer",
                    files={
                        'image': open(path, 'rb'),
                    },
                    headers={'api-key': self.__apiKey}
                )
                print(r.json())
                self.__urlColorize = r.json()['output_url']
            else:
                print("File mode for colorization error")

    def superResolution(self, option, path):
        import requests
        print("Super Resolution in process...")

        if option == LOCALFILE:
            r = requests.post(
                "https://api.deepai.org/api/torch-srgan",
                files={
                    'image': open(path, 'rb'),
                },
                headers={'api-key': self.__apiKey}
            )
            print(r.json())
            self.__urlSuperResolution = r.json()['output_url']

        else:
            if option == URLFILE:
                r = requests.post(
                    "https://api.deepai.org/api/torch-srgan",
                    data={
                        'image': path,
                    },
                    headers={'api-key': self.__apiKey}
                )
                print(r.json())
                self.__urlSuperResolution = r.json()['output_url']
            else:
                print("File mode for super resolution error")

    def neuralTalk(self, option, path):
        import requests
        print("Neural Talk in process...")
        if option == LOCALFILE:
            r = requests.post(
                "https://api.deepai.org/api/neuraltalk",
                files={
                    'image': open(path, 'rb'),
                },
                headers={'api-key': self.__apiKey}
            )
            print(r.json())
            self.__textNeuralTalk = r.json()['output'].capitalize()
        else:
            if option == URLFILE:
                r = requests.post(
                    "https://api.deepai.org/api/neuraltalk",
                    data={
                        'image': path,
                    },
                    headers={'api-key': self.__apiKey}
                )
                print(r.json())
                self.__textNeuralTalk = r.json()['output'].capitalize()
            else:
                print("File mode for neural talk error")

    def iaProcessingCnSR(self):
        self.colorize(LOCALFILE, self.__filePath)
        self.superResolution(URLFILE, self.__urlColorize)
        self.waifu2x(URLFILE, self.__urlSuperResolution)
        self.colorize(URLFILE, self.__urlWaifu2x)
        self.neuralTalk(URLFILE, self.__urlColorize)
        GLib.idle_add(self.updateGui)

    def iaProcessingNT(self):
        self.neuralTalk(LOCALFILE, self.__filePath)

    def updateGui(self):
        self.loadURLImage(self.__urlSuperResolution)
        self.__lblNeural.set_text(self.__textNeuralTalk);
        self.__btnConvert.set_sensitive(True)
        self.__btnSave.set_sensitive(True)
        self.__btnConvert.set_label("Convert")

    def clickCloseDialog(self, button):
        self.__btnConvert.set_sensitive(True)
        self.__btnSave.set_sensitive(True)
        self.__saveDialog.hide();

    def clickSaveDialog(self, button):
        self.clickCloseDialog(self);
        thrSave = threading.Thread(target=self.saveFile)
        # This avoid that thread doesn't end when the process ends
        thrSave.daemon = True
        thrSave.start()

    def deleteOutput(self):
        if os.path.exists("output.jpg"):
            os.remove("output.jpg")
        else:
            print("The file does not exist")

    def saveFile(self):
        self.deleteOutput()
        savePath = self.__saveDialog.get_current_folder() + "/" + self.__textEntry.get_text()
        urllib.request.urlretrieve(self.__urlSuperResolution, savePath)

    def loadURLImage(self, result):
        response = urlopen(result)
        fname = result.split("/")[-1]
        f = open(fname, "wb")
        f.write(response.read())
        f.close()
        response.close()
        self.adjustImage(self.__imgResContainer, self.__imgRes, fname)

    def loadLocalImage(self, button):
        self.__btnConvert.set_sensitive(True)
        self.__filePath = self.__fileSelector.get_filename()
        self.adjustImage(self.__imgOrigContainer, self.__imgOrig, self.__filePath)

    def showWindow(self):
        self.__window.show_all()

    def clickConvert(self, button):
        self.__btnConvert.set_label("Please Wait...")
        self.__btnSave.set_label("Save")
        self.__btnSave.set_sensitive(False)
        self.__btnConvert.set_sensitive(False)
        self.__lblNeural.set_text("The enhanced image in a sentence...")
        self.__imgRes.clear()
        thrCnSR = threading.Thread(target=self.iaProcessingCnSR)
        # This avoid that thread doesn't end when the process ends
        thrCnSR.daemon = True
        thrCnSR.start()

    def clickSaveButton(self, button):
        self.__textEntry.set_text("EnhancedImage.jpg")
        self.__saveDialog.show()


if __name__ == "__main__":
    myApp = App('ImageEnhancer.glade')
    myApp.showWindow()
    Gtk.main()
