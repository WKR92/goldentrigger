# It may take a while to display first photo 
# Some folders where too big to display and made MemoryError

from tkinter import *
from PIL import ImageTk, Image
import os
from win32api import GetSystemMetrics


global askPathRoot
askPathRoot = Tk()
askPathRoot.title("Ścieżka do folderu ze zdjęciami")

global myLabel

def onReturn(event):
    inp = e.get()
    rawInp = r'%s' % inp
    readyPath = rawInp.replace("\\", "/")
    e.delete(0, END)
    e.insert(0, readyPath)
    askPathRoot.withdraw()
    root = Toplevel(askPathRoot)

    
    root.title("Zdjęcia")


    screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
    root.geometry("{}x{}".format(screen_width//1, screen_height//1))
    minSW = screen_width * 0.20
    minSH = screen_height * 0.20
    width, height = screen_width-minSW, screen_height-minSH

    imageList = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(readyPath):
        for file in f:
            if '.jpg' in file:
                imageList.append(os.path.join(r, file))
            if '.jpeg' in file:
                imageList.append(os.path.join(r, file))
            if '.png' in file:
                imageList.append(os.path.join(r, file))
            if '.gif' in file:
                imageList.append(os.path.join(r, file))
            if '.raw' in file:
                imageList.append(os.path.join(r, file))
            if '.swf' in file:
                imageList.append(os.path.join(r, file))
            if '.svg' in file:
                imageList.append(os.path.join(r, file))
        
    picsList = []


    def open_image_from_list(list):
        for i in list:
            global pic
            pic = Image.open(i, "r")
            picsList.append(pic)

    open_image_from_list(imageList)

    resizedImiges = []


    def resize_image_from_list(lista):
        try:
            for pic in picsList:
                if pic.width >= width and pic.height >= height:
                    pw = pic.width - width
                    proc = (pw/pic.width)*100
                    pr = proc/100
                    ws = float(pic.width)*pr
                    wh = float(pic.height)*pr
                    x = pic.width-int(ws)
                    y = pic.height-int(wh)
                    ph = pic.height - height
                    proc = (ph/pic.height)*100
                    pr = proc/100
                    ws = float(pic.width)*pr
                    wh = float(pic.height)*pr
                    x = pic.width-int(ws)
                    y = pic.height-int(wh)
                    z = pic.resize((x, y), Image.ANTIALIAS)
                    resizedImiges.append(z)

                if pic.width >= width and pic.height <= height:
                    pw = pic.width - width
                    proc = (pw/pic.width)*100
                    pr = proc/100
                    ws = float(pic.width)*pr
                    wh = float(pic.height)*pr
                    x = pic.width-int(ws)
                    y = pic.height-int(wh)
                    z = pic.resize((x, y), Image.ANTIALIAS)
                    resizedImiges.append(z)

                if pic.height >= height and pic.width <= width:
                    ph = pic.height - height
                    proc = (ph/pic.height)*100
                    pr = proc/100
                    ws = float(pic.width)*pr
                    wh = float(pic.height)*pr
                    x = pic.width-int(ws)
                    y = pic.height-int(wh)
                    z = pic.resize((x, y), Image.ANTIALIAS)
                    resizedImiges.append(z)
          
                if pic.height <= height and pic.width <= width:
                    x = pic
                    resizedImiges.append(x)

        except MemoryError:
            errorLabel = Label(root, text="Memorry error. Zdjęcia są za duże, żeby je wyświetlić. Proszę spróbuj z inną ścieżką")
            errorLabel.grid()

    resize_image_from_list(picsList)

    ReadyImages = []

    def open_resized_image_from_list(list):
        for img in list:
            x = ImageTk.PhotoImage((img))
            ReadyImages.append(x)

    open_resized_image_from_list(resizedImiges)

    def close():
        root.destroy()

    global myLabel
    try:
        myLabel = Label(root, image = ReadyImages[0])
    except IndexError:
        indexErrorLabel = Label(root, text="W pliku nie ma żadnych zdjęć, lub podałeś/aś błędną ścieżkę. Sprawdź w oknie podawania adresu.")
        indexErrorLabel.grid()
        askPathRoot.deiconify()
        destroyButton = Button(root, text="Close window", command=close)
        destroyButton.grid()

    
    myLabel.grid(row=1, column=2, columnspan=3)
    status = Label(root, text="Image 1 of " + str(len(ReadyImages)), bd=1, relief=SUNKEN, anchor=E)
    root.bind("<Right>", lambda event: next(2))

    global blankWidth
    blankWidth = (width - ReadyImages[0].width())/14
    global blankHeight
    blankHeight = (height - ReadyImages[0].height())/28

    def next(imageNumber, event=None):
        global myLabel
        global button_next
        global button_back
        global blankWidth
        global blankHeight
        global blankRight
        global blankLeft
        global blankBottom
        global blankTop
        myLabel.grid_forget()
        blankLeft.grid_forget()
        blankRight.grid_forget()
        blankBottom.grid_forget()
        blankTop.grid_forget()
        myLabel = Label(root, image=ReadyImages[imageNumber-1])
        root.bind("<Right>", lambda event: next(imageNumber+1))
        root.bind("<Left>", lambda event: back(imageNumber-1))
        blankWidth = (width - ReadyImages[imageNumber-1].width())/14
        blankHeight = (height - ReadyImages[imageNumber-1].height())/28
        blankLeft = Label(root, text = "", width=int(blankWidth))
        blankRight = Label(root, text = "", width=int(blankWidth))
        blankTop = Label(root, text = "", height = int(blankHeight))
        blankBottom = Label(root, text = "", height = int(blankHeight))
        button_next = Button(root, text=">>", command=lambda: next(imageNumber+1), height=4)
        button_back = Button(root, text="<<", command=lambda: back(imageNumber-1), height=4)
    
        if imageNumber == len(ReadyImages):
            button_next = Button(root, text=">>", state=DISABLED, height=4)
            root.unbind("<Right>")   

        myLabel.grid(row=1, column=2, columnspan=3)
        button_back.grid(row=1, column=0, padx=60, sticky=W)
        button_next.grid(row=1, column=6, padx=60, sticky=E)
        blankLeft.grid(row=1, column = 1)
        blankRight.grid(row=1, column = 5)
        blankTop.grid(row=0, column = 0)
        blankBottom.grid(row=3, column = 0)

        #update status label
        status = Label(root, text="Image " + str(imageNumber) + " of " + str(len(ReadyImages)), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=2, column=2, columnspan=3, sticky=W+E)
    

    def back(imageNumber, event=None):
        global myLabel
        global button_next
        global button_back
        global blankWidth
        global blankHeight
        global blankRight
        global blankLeft
        global blankBottom
        global blankTop
        myLabel.grid_forget()
        blankLeft.grid_forget()
        blankRight.grid_forget()
        blankBottom.grid_forget()
        blankTop.grid_forget()
        myLabel = Label(root, image = ReadyImages[imageNumber-1])
        root.bind("<Right>", lambda event: next(imageNumber+1))
        root.bind("<Left>", lambda event: back(imageNumber-1))
        blankWidth = (width - ReadyImages[imageNumber-1].width())/14
        blankHeight = (height - ReadyImages[imageNumber-1].height())/28
        blankLeft = Label(root, text = "", width=int(blankWidth))
        blankRight = Label(root, text = "", width=int(blankWidth))
        blankTop = Label(root, text = "", height = int(blankHeight))
        blankBottom = Label(root, text = "", height = int(blankHeight))
        button_next = Button(root, text=">>", command=lambda: next(imageNumber+1), height=4)
        button_back = Button(root, text="<<", command=lambda: back(imageNumber-1), height=4)

        if imageNumber == 1:
            button_back = Button(root, text="<<", state=DISABLED, height=4)
            root.unbind("<Left>")

        myLabel.grid(row=1, column=2, columnspan=3)
        button_back.grid(row=1, column=0, padx=60, sticky=W)
        button_next.grid(row=1, column=6, padx=60, sticky=E)
        blankLeft.grid(row=1, column = 1)
        blankRight.grid(row=1, column = 5)
        blankTop.grid(row=0, column = 0)
        blankBottom.grid(row=3, column = 0)


        #update status label
        status = Label(root, text="Image " + str(imageNumber) + " of " + str(len(ReadyImages)), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=2, column=2, columnspan=3, sticky=W+E)
    
        
    button_back = Button(root, text="<<", command=back, state=DISABLED, height=4)
    button_next = Button(root, text=">>", command=lambda: next(2), height=4)
    global blankLeft
    blankLeft = Label(root, text = "", width=int(blankWidth))
    global blankRight
    blankRight = Label(root, text = "", width=int(blankWidth))
    global blankTop
    blankTop = Label(root, text = "", height = int(blankHeight))
    global blankBottom
    blankBottom = Label(root, text = "", height = int(blankHeight))

    button_back.grid(row=1, column=0, padx=60, sticky=W)
    button_next.grid(row=1, column=6, padx=60, sticky=E)
    status.grid(row=2, column=2, columnspan=3, sticky=W+E)
    blankLeft.grid(row=1, column = 1)
    blankRight.grid(row=1, column = 5)
    blankTop.grid(row=0, column = 0)
    blankBottom.grid(row=3, column = 0)
    arrowsLabel = Label(root, text="Możesz uzywać strzałek <- ->, żeby przewijać zdjęcia")
    arrowsLabel.grid(row=4, column=3)
    

    root.mainloop()


askLabel = Label(askPathRoot, text="Podaj ścieżkę do folderu, z którego chiałbyś przeglądać zdjęcia:")
askLabel.grid()
e = Entry(askPathRoot, width = 70, borderwidth = 5, bg="white",)
e.bind("<Return>", onReturn)
e.grid()
infoLabel1 = Label(askPathRoot, text="Slider obsługuje pliki: .jpg, .jpeg, .png, .gif, .raw, .swf, .svg").grid()
infoLabel = Label(askPathRoot, text="Wciśnij enter, żeby kontynuować. To potrwa kilka sekund.").grid()


askPathRoot.mainloop()
