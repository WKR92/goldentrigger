# This is kind of meme - motivational text on demotivational background generator
# It takes a moment to run API and display picture

from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO
import credentials
from win32api import GetSystemMetrics
import textwrap


root = Tk()
root.title("Motivational text on demotivational background generator")
global frame
frame = Frame(root)
frame.pack()


screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
root.geometry("{}x{}".format(screen_width//1, screen_height//1))
minSW = screen_width * 0.20
minSH = screen_height * 0.20
width, height = screen_width-minSW, screen_height-minSH


r = requests.get("https://api.unsplash.com/photos/random?query=pain", headers=credentials.headers)

try:
    meme = r.json()
except json.decoder.JSONDecodeError:
    print("Niepoprawny format", r.text)


quoteRequest = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json")

try:
    quote = quoteRequest.json()
except json.decoder.JSONDecodeError:
    print("Niepoprawny format", quoteRequest.text)


def resize_image(pic):
        try:
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
                return z

            if pic.width >= width and pic.height <= height:
                pw = pic.width - width
                proc = (pw/pic.width)*100
                pr = proc/100
                ws = float(pic.width)*pr
                wh = float(pic.height)*pr
                x = pic.width-int(ws)
                y = pic.height-int(wh)
                z = pic.resize((x, y), Image.ANTIALIAS)
                return z

            if pic.height >= height and pic.width <= width:
                ph = pic.height - height
                proc = (ph/pic.height)*100
                pr = proc/100
                ws = float(pic.width)*pr
                wh = float(pic.height)*pr
                x = pic.width-int(ws)
                y = pic.height-int(wh)
                z = pic.resize((x, y), Image.ANTIALIAS)
                return z
          
            if pic.height <= height and pic.width <= width:
                x = pic
                return x

        except MemoryError:
            errorLabel = Label(root, text="Memory error. Pictures are too big to be displayed")
            errorLabel.pack()


img_url = meme["urls"]["full"]
response = requests.get(img_url)
img_data = response.content
img = Image.open(BytesIO(img_data))
PreImage = resize_image(img)
fontType = ImageFont.truetype("arial.ttf", size=PreImage.height//35)
global draw
draw = ImageDraw.Draw(PreImage)
char_width, char_height = fontType.getsize('A')
chars_per_line = PreImage.width // char_width
top_text = quote['quoteText']
top_lines = textwrap.wrap(top_text, width=chars_per_line)


y = PreImage.height - char_height * len(top_lines) - 200
for line in top_lines:
	line_width, line_height = fontType.getsize(line)
	x = (PreImage.width - line_width)/2
	drawnedText = draw.text((x,y), line, fill='white', font=fontType)
	y += line_height


readyImage = ImageTk.PhotoImage(PreImage)
global panel
panel = Label(frame, image=readyImage)
panel.pack()


def button_new():
    global panel
    global frame
    global blankSpot1
    global new_img_button
    global draw
    del draw
    frame.destroy()
    panel.destroy()
    blankSpot1.pack_forget()
    new_img_button.pack_forget()

    frame = Frame(root)
    frame.pack()

    r = requests.get("https://api.unsplash.com/photos/random?query=pain", headers=credentials.headers)

    try:
        meme = r.json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", r.text)


    quoteRequest = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json")

    try:
        quote = quoteRequest.json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", quoteRequest.text)
        

    img_url = meme["urls"]["full"]
    response = requests.get(img_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    PreImage = resize_image(img)
    fontType = ImageFont.truetype("arial.ttf", size=PreImage.height//35)
    draw = ImageDraw.Draw(PreImage)
    
    char_width, char_height = fontType.getsize('A')
    chars_per_line = PreImage.width // char_width
    top_text = quote['quoteText']
    top_lines = textwrap.wrap(top_text, width=chars_per_line)

    y = PreImage.height - char_height * len(top_lines) - 200
    for line in top_lines:
        line_width, line_height = fontType.getsize(line)
        x = (PreImage.width - line_width)/2
        draw.text((x,y), line, fill='white', font=fontType)
        y += line_height

    readyImage = ImageTk.PhotoImage(PreImage)
    panel = Label(frame, image=readyImage)
    panel.pack()

    blankSpot1 = Label(root, text=" ")
    blankSpot1.pack()
    new_img_button = Button(root, text="Another meme", command=button_new)
    new_img_button.pack()

    root.mainloop()


global blankSpot1
blankSpot1 = Label(root, text=" ")
blankSpot1.pack()
global new_img_button
new_img_button = Button(root, text="Another meme", command=button_new)
new_img_button.pack()


root.mainloop()
