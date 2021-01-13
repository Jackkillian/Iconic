###################
# File Icon Maker #
###################

### TODO: MAKE ICON PREVIEW

import tkinter as tk
from tkinter import ttk, font, filedialog
from PIL import Image, ImageFont, ImageDraw 
import json
import pathlib
from concurrent import futures
import os

threadPoolExec = futures.ThreadPoolExecutor(max_workers=1)

def runFunc(func, args):
    return lambda:func(args)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.availableFonts = list(font.families());
        self.preferedFonts = ["Quicksand", "Calibri"]
        self.makeRunning = False

        self.defaultTheme = ttk.Style(parent)
        root.tk.call('lappend', 'auto_path', './awthemes-10.2.0')
        root.tk.call('package', 'require', 'awdark')
        self.defaultTheme.theme_use('awdark')
        self.configure(bg=self.defaultTheme.lookup('TFrame', 'background'))
        
        titleLbl = ttk.Label(self, text="Iconic", font=self.chooseFont(self.preferedFonts) + " 30")
        authorLbl = ttk.Label(self, text="File icon generator made by Jackkillian", font=self.chooseFont(self.preferedFonts) + " 12")
        titleLbl.config(anchor=tk.CENTER)
        authorLbl.config(anchor=tk.CENTER)
        titleLbl.pack(side="top", fill="both", expand=True)
        authorLbl.pack(side="top", fill="both", expand=True)
        
        # JSON file
        jsonPathFrm = ttk.Frame(self)
        jsonPathLbl = ttk.Label(jsonPathFrm, text="JSON file:      ");
        jsonPathLbl.config(anchor=tk.NW)
        self.jsonPathEty = ttk.Entry(jsonPathFrm, width=50)
        chooseJsonBtn = ttk.Button(self.jsonPathEty, text="...", command=lambda: threadPoolExec.submit(lambda: self.openJson()))

        jsonPathLbl.pack(side="left")
        self.jsonPathEty.pack(side="left", fill="both", expand=True)
        chooseJsonBtn.pack(side="right")
        
        jsonPathFrm.pack(side="top", fill="both", expand=True, pady=4)

        # Read folder
        readPathFrm = ttk.Frame(self)
        readPathLbl = ttk.Label(readPathFrm, text="Read folder:  ");
        readPathLbl.config(anchor=tk.NW)
        self.readPathEty = ttk.Entry(readPathFrm, width=50)
        chooseReadFolderBtn = ttk.Button(self.readPathEty, text="...", command=lambda: threadPoolExec.submit(lambda: self.openReadFolder()))

        readPathLbl.pack(side="left")
        self.readPathEty.pack(side="left", fill="both", expand=True)
        chooseReadFolderBtn.pack(side="right")
        
        readPathFrm.pack(side="top", fill="both", expand=True, pady=4)

        # Write folder
        writePathFrm = ttk.Frame(self)
        writePathLbl = ttk.Label(writePathFrm, text="Write folder: ");
        writePathLbl.config(anchor=tk.NW)
        self.writePathEty = ttk.Entry(writePathFrm, width=50)
        chooseWriteFolderBtn = ttk.Button(self.writePathEty, text="...", command=lambda: threadPoolExec.submit(lambda: self.openWriteFolder()))

        writePathLbl.pack(side="left")
        self.writePathEty.pack(side="right", fill="both", expand=True)
        chooseWriteFolderBtn.pack(side="right")
        
        writePathFrm.pack(side="top", fill="both", expand=True, pady=4)

        # File Type
        fileTypeFrm = ttk.Frame(self)
        fileTypeLbl = ttk.Label(fileTypeFrm, text="File type:       ");
        fileTypeLbl.config(anchor=tk.NW)
        self.fileTypeCmb = ttk.Combobox(fileTypeFrm, width=45, values=["PNG", "ICO", "JPG", "JPEG", "GIF"])

        fileTypeLbl.pack(side="left")
        self.fileTypeCmb.pack(side="left", fill="both", expand=True)
        
        fileTypeFrm.pack(side="top", fill="both", expand=True, pady=4)

        # Font options
        self.fontFrm = ttk.Labelframe(self, text='Font Options')
        fontPathFrm = ttk.Frame(self.fontFrm)
        fontPathLbl = ttk.Label(fontPathFrm, text="Font file:           ");
        fontPathLbl.config(anchor=tk.NW)
        self.fontPathEty = ttk.Entry(fontPathFrm, width=50)
        chooseFontBtn = ttk.Button(self.fontPathEty, text="...", command=lambda: threadPoolExec.submit(lambda: self.openFont()))

        fontSizeFrm = ttk.Frame(self.fontFrm)
        fontSizeLbl = ttk.Label(fontSizeFrm, text="Base font size:  ");
        fontSizeLbl.config(anchor=tk.NW)
        self.fontSizeSpn = ttk.Spinbox(fontSizeFrm, from_=0, to=64 ** 64, increment=1)
        self.fontSizeSpn.set(25)

        fontPathLbl.pack(side="left")
        self.fontPathEty.pack(side="right", fill="both", expand=True)
        chooseFontBtn.pack(side="right")
        
        fontSizeLbl.pack(side="left")
        self.fontSizeSpn.pack(side="left", fill="both", expand=True)

        fontPathFrm.pack(side="top", fill="both", expand=True, pady=4)
        fontSizeFrm.pack(side="top", fill="both", expand=True, pady=4)
        self.fontFrm.pack(side="top", fill="both", expand=True, pady=8, padx=10)

        # Resizing
        self.resizeFrm = ttk.LabelFrame(self, text="Resize Options")

        widthResizeFrm = ttk.Frame(self.resizeFrm)
        widthResizeLbl = ttk.Label(widthResizeFrm, text="Width:   ");
        self.widthResizeSpn = ttk.Spinbox(widthResizeFrm, from_=0, to=64 ** 64, increment=64)

        heightResizeFrm = ttk.Frame(self.resizeFrm)
        heightResizeLbl = ttk.Label(heightResizeFrm, text="Height:  ");
        self.heightResizeSpn = ttk.Spinbox(heightResizeFrm, from_=0, to=64 ** 64, increment=64)
        
        self.doResize = tk.IntVar()
        
        def toggleFrame():
            for frame in self.resizeFrm.children:
                frame = self.resizeFrm.children[frame]
                for widget in frame.children:
                    frame.children[widget].config(state=tk.DISABLED if not self.doResize.get() else tk.NORMAL)
        toggleFrame()

        resizeChk = ttk.Checkbutton(self, text="Resize Images", variable=self.doResize, command=toggleFrame)
        resizeChk.pack(side="top", fill="both", expand=True, pady=2)

        widthResizeLbl.pack(side="left")
        self.widthResizeSpn.pack(side="left", fill="both", expand=True)
        heightResizeLbl.pack(side="left")
        self.heightResizeSpn.pack(side="left", fill="both", expand=True)

        widthResizeFrm.pack(side="top", fill="both", expand=True, pady=4)
        heightResizeFrm.pack(side="top", fill="both", expand=True, pady=4)

        self.resizeFrm.pack(side="top", fill="both", expand=True, pady=8, padx=10)

        # Progress
        makeBtn = ttk.Button(self, text="Make", command=self.make)
        self.progressBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, value=0, mode='determinate')
        self.descriptionLbl = ttk.Label(self, text="Press \"Make\" to make the file icons.")
        self.descriptionLbl.config(anchor=tk.CENTER)

        makeBtn.pack(fill="both", expand=True, pady=4)
        self.progressBar.pack(fill="both", expand=True, pady=4)
        self.descriptionLbl.pack(fill="both", expand=True, pady=4)

    def openJson(self):
        path = filedialog.askopenfilename(title="Select JSON", parent=self, filetypes=(('JSON', '.json'), ('All Files', '.*')))
        if (path):
            self.jsonPathEty.delete(0, tk.END)
            self.jsonPathEty.insert(0, path)

    def openFont(self):
        path = filedialog.askopenfilename(title="Select Font", parent=self, filetypes=(('True Type Font', '.ttf'), ('All Files', '.*')))
        if (path):
            self.fontPathEty.delete(0, tk.END)
            self.fontPathEty.insert(0, path)            

    def openReadFolder(self):
        path = filedialog.askdirectory(title="Select Read Folder", parent=self)
        if (path):
            self.readPathEty.delete(0, tk.END)
            self.readPathEty.insert(0, path)

    def openWriteFolder(self):
        path = filedialog.askdirectory(title="Select Write Folder", parent=self)
        if (path):
            self.writePathEty.delete(0, tk.END)
            self.writePathEty.insert(0, path)

    def chooseFont(self, preferedFonts):
        for font in preferedFonts:
            if font in self.availableFonts:
                break;
        return font

    def make(self):
        if not self.makeRunning:
            self.makeRunning = True
            #self._make()
            threadPoolExec.submit(lambda: self._make())

    def _make(self):
        # Save variables so that they don't get changed accidently by user during operation.
        jsonPath = self.jsonPathEty.get()
        readPath = self.readPathEty.get()
        writePath = self.writePathEty.get()
        fileExportType = self.fileTypeCmb.get()
        fontPath = self.fontPathEty.get()
        fontSize = self.fontSizeSpn.get()
        doResize = self.doResize.get()
        if (doResize):
            resizeWidth = self.widthResizeSpn.get()
            resizeHeight = self.heightResizeSpn.get()

        fileTypes = []
        fileJson = json.load(open(jsonPath))

        length = 0
        for catagory in fileJson.keys():
            for fileType in fileJson[catagory]:
                if (self.doResize.get()):
                    length += 2
                else:
                    length += 1

        progress = 0
        for catagory in fileJson.keys():
            for fileType in fileJson[catagory]:
                self.descriptionLbl["text"] = "Making", fileType + "..."
                img = Image.open(os.path.join(readPath, catagory + "." + fileExportType.lower()))
                if len(fileType) <= 3:
                    font = ImageFont.truetype(fontPath, fontSize)
                else:
                    #if len(fileType) > 5:
                        #split string at 5 with a newline 
                    size = fontSize - ((len(fileType) - 3) * 2)
                    if (size < 1):
                        font = ImageFont.truetype(fontPath, fontSize - ((len(fileType) - 3)))
                    else:
                        font = ImageFont.truetype(fontPath, size)
                imgEdit = ImageDraw.Draw(img)
                w, h = imgEdit.textsize(fileType, font=font)
                imgEdit.text(((64-w)/2,(64-h)/2), fileType, font=font, fill="black")
                if (doResize):
                    self.descriptionLbl["text"] = "Resizing", fileType + "..."
                    img = img.resize((int(resizeWidth), int(resizeHeight)), Image.ANTIALIAS)
                    progress += 1
                img.save(os.path.join(writePath, fileType + "." + fileExportType.lower()), fileExportType.upper())
                progress += 1
                percentage = round(progress/length*100)
                self.progressBar["value"] = percentage
        self.descriptionLbl["text"] = "Done."
        self.makeRunning = False

#E:/File Icons/extensions.json
#C:/Users/jkafr/AppData/Local/Microsoft/Windows/Fonts/Kiona-Regular.ttf
#E:/File Icons/Standard+/png

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Iconic by Jackkillian")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
