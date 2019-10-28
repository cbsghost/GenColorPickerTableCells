#!/usr/bin/env python3
#
# GenColorPickerTableCells.py
#
# Generate color picker table cells for Qt5's table widget.
#
# Created by CbS Ghost, 2019.
# Copyright (c) 2019 CbS Ghost. All rights reserved.
# (This special version is licensed under GPL-2.0)
#
# -*- coding: utf-8 -*-

from   __future__ import print_function
import sys        as     sys
if sys.version_info.major < 3 or sys.version_info.minor < 7:
    print("Python version 3.7 or above is quired. Quitting now.")
    sys.exit()

import tkinter as     tk
from   tkinter import ttk          as ttk
from   tkinter import messagebox   as messagebox
from   tkinter import scrolledtext as scrolledtext

colorPickerPhotoFilePath = "colorpicker-mac-preview.gif"

def GenerateSnippet(columns, rows, colorList):
    if (columns == 0 or rows == 0):
        return "<error>invalid properties</error>\n"
    if (len(colorList) < columns * rows):
        return "<error>internal error</error>\n"

    snippetString = ""

    # Define rows
    for i in range(rows):
        snippetString += (
            "<row>\n"
            "  <property name=\"text\">\n"
            "    <string/>\n"
            "  </property>\n"
            "</row>\n"
        )
    # Define columns
    for i in range(columns):
        snippetString += (
            "<column>\n"
            "  <property name=\"text\">\n"
            "    <string/>\n"
            "  </property>\n"
            "</column>\n"
        )
    # Fill properties of each cell
    for i in range(rows):
        for j in range(columns):
            colorHex = colorList[i * columns + j]
            colorValue = tuple(int(colorHex.lstrip('#')[k:k+2], 16) for k in (0, 2, 4))

            snippetString += (
                "<item row=\"{row}\" column=\"{column}\">\n"
                "  <property name=\"text\">\n"
                "    <string/>\n"
                "  </property>\n"
                "  <property name=\"toolTip\">\n"
                "    <string>{colorHex}</string>\n"
                "  </property>\n"
                "  <property name=\"background\">\n"
                "    <brush brushstyle=\"SolidPattern\">\n"
                "      <color alpha=\"255\">\n"
                "        <red>{colorValue[0]}</red>\n"
                "        <green>{colorValue[1]}</green>\n"
                "        <blue>{colorValue[2]}</blue>\n"
                "      </color>\n"
                "    </brush>\n"
                "  </property>\n"
                "</item>\n"
            ).format(row=i, column=j, colorHex=colorHex, colorValue=colorValue)

    return snippetString

class Application(ttk.Notebook):
    colorPickerPhoto_  = None
    colorPickerCanvas_ = None;

    colorPickerCanvasMarkerItemList  = []
    colorPickerCanvasMarkerColorList = []

    beginX_  = None
    beginY_  = None
    offsetX_ = None
    offsetY_ = None
    columns_ = None
    rows_    = None

    snippetTextWidget_ = None

    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)

        # Setup color picker photo
        try:
            self.colorPickerPhoto_ = tk.PhotoImage(file=colorPickerPhotoFilePath)
        except:
            messagebox.showerror("Open File Error", "Cannot open color picker image file.")
            sys.exit(1)

        # Setup property variables
        self.beginX_ = tk.IntVar(value=0)
        self.beginX_.trace_add("write", self.reloadProperties)
        self.beginY_ = tk.IntVar(value=0)
        self.beginY_.trace_add("write", self.reloadProperties)
        self.offsetX_ = tk.IntVar(value=0)
        self.offsetX_.trace_add("write", self.reloadProperties)
        self.offsetY_ = tk.IntVar(value=0)
        self.offsetY_.trace_add("write", self.reloadProperties)
        self.columns_ = tk.IntVar(value=0)
        self.columns_.trace_add("write", self.reloadProperties)
        self.rows_ = tk.IntVar(value=0)
        self.rows_.trace_add("write", self.reloadProperties)

        # Setup tab widgets
        self.createConfigTabWidget()
        self.createSnippetTabWidget()
        self.createAboutTabWidget()

        # Setup layout
        self.pack(expand=True, fill="both")

    def onGenerateSnippetButtonClicked(self):
        beginX  = None
        beginY  = None
        offsetX = None
        offsetY = None
        columns = None
        rows    = None

        try:
            beginX  = self.beginX_.get()
            beginY  = self.beginY_.get()
            offsetX = self.offsetX_.get()
            offsetY = self.offsetY_.get()
            columns = self.columns_.get()
            rows    = self.rows_.get()

            if (offsetX <= 0 or offsetY <= 0 or columns <= 0 or rows <=0):
                raise ValueError()
        except:
            messagebox.showerror("Configuration Error", "Invalid properties.")
            return;

        self.snippetTextWidget_.delete(1.0, tk.END)
        self.snippetTextWidget_.insert(1.0, GenerateSnippet(columns, rows, self.colorPickerCanvasMarkerColorList))
        self.select(1)

    def onCopyToClipboardButtonClicked(self):
        self.clipboard_clear()
        self.clipboard_append(self.snippetTextWidget_.get(1.0, tk.END))

    def getColorPickerPixel(self, x, y):
        if (self.colorPickerPhoto_ == None):
            return ""
        if (x >= self.colorPickerPhoto_.width() or y >= self.colorPickerPhoto_.height()):
            return ""

        colorData = self.colorPickerPhoto_.get(x, y)
        if (type(colorData) is not tuple):
            colorData = tuple(map(int, self.colorPickerPhoto_.get(x, y).split()))

        return "#{0[0]:02X}{0[1]:02X}{0[2]:02X}".format(colorData)

    def colorPickerCanvasLoop(self, *args):
        try:
            if (self.index('current') != 0):
                return

            while (True):
                if (self.colorPickerCanvas_ == None):
                    break

                for i in range(len(self.colorPickerCanvasMarkerItemList)):
                    item      = self.colorPickerCanvasMarkerItemList[i]
                    itemColor = self.colorPickerCanvasMarkerColorList[i]
                    isFilled  = False if (self.colorPickerCanvas_.itemcget(item, "fill") == "") else True
                    self.colorPickerCanvas_.itemconfig(item, fill="" if (isFilled) else itemColor)
                    self.colorPickerCanvas_.itemconfig(item, outline="white" if (isFilled) else "black")
                break
        except:
            pass

        self.colorPickerCanvas_.after(480, self.colorPickerCanvasLoop)

        return True

    def reloadProperties(self, *args):
        beginX  = None
        beginY  = None
        offsetX = None
        offsetY = None
        columns = None
        rows    = None

        try:
            beginX  = self.beginX_.get()
            beginY  = self.beginY_.get()
            offsetX = self.offsetX_.get()
            offsetY = self.offsetY_.get()
            columns = self.columns_.get()
            rows    = self.rows_.get()
        except:
            return False;

        colorPickerCanvas = self.colorPickerCanvas_
        if (colorPickerCanvas == None):
            return False

        for item in self.colorPickerCanvasMarkerItemList:
            colorPickerCanvas.delete(item)
        self.colorPickerCanvasMarkerItemList  = []
        self.colorPickerCanvasMarkerColorList = []

        if (offsetX <= 0 or offsetY <= 0 or columns <= 0 or rows <= 0):
            return False

        for i in range(rows):
            for j in range(columns):
                itemPos  = (beginX + j * offsetX, beginY + i * offsetY)
                itemRect = ()
                if (i == 0 and j == 0):
                    itemRect = (itemPos[0] - 6, itemPos[1] - 6, itemPos[0] + 6, itemPos[1] + 6)
                else:
                    itemRect = (itemPos[0] - 4, itemPos[1] - 4, itemPos[0] + 4, itemPos[1] + 4)
                itemColor = self.getColorPickerPixel(itemPos[0], itemPos[1])
                item = colorPickerCanvas.create_oval(itemRect[0], itemRect[1], itemRect[2], itemRect[3])
                colorPickerCanvas.itemconfig(item, fill=itemColor)
                self.colorPickerCanvasMarkerItemList.append(item)
                self.colorPickerCanvasMarkerColorList.append(itemColor)

        return True;

    def createConfigTabWidget(self):
        configTabView = ttk.Frame(self)
        configTabView.bind("<Visibility>", self.colorPickerCanvasLoop)
        self.add(configTabView, text="Configuration")

        configTabView.grid_rowconfigure(0,    weight=0, pad=3)
        configTabView.grid_rowconfigure(1,    weight=0, pad=3)
        configTabView.grid_rowconfigure(2,    weight=0, pad=3)
        configTabView.grid_rowconfigure(3,    weight=1, pad=3)
        configTabView.grid_rowconfigure(4,    weight=0, pad=3)
        configTabView.grid_columnconfigure(0, weight=0, pad=3)
        configTabView.grid_columnconfigure(1, weight=1, pad=3)
        configTabView.grid_columnconfigure(2, weight=0, pad=3)
        configTabView.grid_columnconfigure(3, weight=1, pad=3)

        ttk.Label(configTabView, text="Begin X").grid(row=0, column=0, sticky="e")
        ttk.Spinbox(configTabView, textvariable=self.beginX_, from_=0, to=16383).grid(row=0, column=1, sticky="ew")
        ttk.Label(configTabView, text="Begin Y").grid(row=0, column=2, sticky="e")
        ttk.Spinbox(configTabView, textvariable=self.beginY_, from_=0, to=16383).grid(row=0, column=3, sticky="ew")

        ttk.Label(configTabView, text="Offset X").grid(row=1, column=0, sticky="e")
        ttk.Spinbox(configTabView, textvariable=self.offsetX_, from_=0, to=16383).grid(row=1, column=1, sticky="ew")
        ttk.Label(configTabView, text="Offset Y").grid(row=1, column=2, sticky="e")
        ttk.Spinbox(configTabView, textvariable=self.offsetY_, from_=0, to=16383).grid(row=1, column=3, sticky="ew")

        ttk.Label(configTabView, text="Columns").grid(row=2, column=0, sticky="e")
        ttk.Spinbox(configTabView, textvariable=self.columns_, from_=0, to=16383).grid(row=2, column=1, sticky="ew")
        ttk.Label(configTabView, text="Rows").grid(row=2, column=2, sticky="e")
        ttk.Spinbox(configTabView, textvariable=self.rows_, from_=0, to=16383).grid(row=2, column=3, sticky="ew")

        colorPickerSize = (self.colorPickerPhoto_.width(), self.colorPickerPhoto_.height())
        colorPickerCanvas = tk.Canvas(configTabView, width=colorPickerSize[0], height=colorPickerSize[1])
        colorPickerCanvas.grid(row=3, columnspan=4)
        colorPickerCanvas.create_image(colorPickerSize[0] / 2, colorPickerSize[1] / 2, image=self.colorPickerPhoto_)
        self.colorPickerCanvas_ = colorPickerCanvas

        generateSnippetButton = ttk.Button(configTabView, text="Generate Snippet")
        generateSnippetButton.configure(command=self.onGenerateSnippetButtonClicked)
        generateSnippetButton.grid(row=4, columnspan=4)

    def createSnippetTabWidget(self):
        snippetTabView = ttk.Frame(self)
        self.add(snippetTabView, text="Snippet Output")

        snippetTabView.grid_rowconfigure(0,    weight=1, pad=3)
        snippetTabView.grid_rowconfigure(1,    weight=0, pad=3)
        snippetTabView.grid_columnconfigure(0, weight=1, pad=3)

        self.snippetTextWidget_ = scrolledtext.ScrolledText(snippetTabView)
        self.snippetTextWidget_.grid(row=0, sticky="nsew")

        copyToClipboardButton = ttk.Button(snippetTabView, text="Copy to Clipboard")
        copyToClipboardButton.configure(command=self.onCopyToClipboardButtonClicked)
        copyToClipboardButton.grid(row=1)

    def createAboutTabWidget(self):
        aboutTabView = ttk.Frame(self)
        self.add(aboutTabView, text="About")

        aboutTabView.grid_rowconfigure(0,    weight=1, pad=3)
        aboutTabView.grid_rowconfigure(1,    weight=0, pad=3)
        aboutTabView.grid_rowconfigure(2,    weight=0, pad=3)
        aboutTabView.grid_rowconfigure(3,    weight=0, pad=3)
        aboutTabView.grid_rowconfigure(4,    weight=2, pad=3)
        aboutTabView.grid_columnconfigure(0, weight=1, pad=3)

        softwareTitleLabel = ttk.Label(aboutTabView, text="GenColorPickerTableCells.py")
        softwareTitleLabel.config(anchor="center")
        softwareTitleLabel.config(font=("","24","bold italic"))
        softwareTitleLabel.grid(row=0, sticky="sew")

        ttk.Separator(aboutTabView).grid(row=1, sticky="ew")

        softwareDescLabel = ttk.Label(aboutTabView)
        softwareDescLabel.config(text="Generate color picker table cells for Qt5's table widget.\n\n")
        softwareDescLabel.config(anchor="center")
        softwareDescLabel.grid(row=2, sticky="ew")

        copyrightLabel = ttk.Label(aboutTabView)
        copyrightLabel.config(text="Copyright (c) 2019 CbS Ghost. All rights reserved.")
        copyrightLabel.config(anchor="center")
        copyrightLabel.grid(row=3, sticky="ew")

        copyrightLabel2 = ttk.Label(aboutTabView)
        copyrightLabel2.config(text="(This special version is licensed under GPL-2.0)")
        copyrightLabel2.config(anchor="center")
        copyrightLabel2.grid(row=4, sticky="new")

if __name__ == '__main__':
    # Override default color picker image file path if specify custom image file
    argList = sys.argv
    if (len(argList) > 1):
        colorPickerPhotoFilePath = argList[1]

    # Setup main widget
    root = tk.Tk()
    root.title("Color Picker Table Cell Generator (Qt5)")
    app = Application(root)

    # Update geometry of main widget
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    # Enter application main loop
    root.mainloop()
