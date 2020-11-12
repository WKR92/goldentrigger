# Read PDF fast by displayin words one by one 
# You have to use Global.py and my.kv form main branch to run this program
# You can't save progress yet in this app, but i will add this feature later

from os import pathsep
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from typing import Text
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from kivy.properties import StringProperty
import time
import Global
from kivy.clock import Clock
from functools import partial
import threading
from queue import Empty, Queue
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    textSpeed = NumericProperty(0.200)


class ThirdWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


def show_popup():
    content = Label(text="Lol")

    popupWindow = Popup(title="The speed of reading", content=content, size=(400, 400))

    popupWindow.open()


def convert_pdf_to_txt(path, label):

    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        label.text = "Press start to begin fast reading"
        Global.raw_text.append(text)

    except FileNotFoundError:
        label.text = "No such file or directory. Please go back and insert correct path"

    except OSError:
        label.text = "No such file or directory. Please go back and insert correct path"


q = Queue()


def get_path(text_inpt, label):
    path = text_inpt.text
    change_slahses = path.replace("\\", "/")
    readyPath = change_slahses
    return readyPath


def tittle_of_book(text_inpt, label):
    parts = []
    path = text_inpt.text
    cut = path.split("/")
    parts.append(cut)
    tittle = parts[0][-1]
    ready_tittle = tittle[:-4]
    label.text = "You are reading: " + ready_tittle + "  |Remember that if you will stop text and go between words, after resume text will always start from a place you stopped it."
    if not path:
        label.text = "You are reading: File not chosen."


def split(lista):
    for i in lista:
        split = i.split(" ")
        Global.split_text.append(split)


def first_text_clean(lista):
    for i in lista[0]:
        if "\n" in i:
            cut = i.strip('\n')
            Global.firstCut.append(cut)
        elif i == "":
            continue
        elif i == "\n":
            continue
        else:
            Global.firstCut.append(i)


def second_text_clean(lista):
    for i in lista:
        if "\n" in i:
            cut = i.strip('\n')
            Global.secondCut.append(cut)
        elif i == "":
            continue
        elif i == "\n":
            continue
        else:
            Global.secondCut.append(i)


storedText = []
global queue_data


def get_from_queue(label, *args):
    global queue_data
    try:
        queue_data = q.get(timeout = 5)
        storedText.append(queue_data)
        label.text = queue_data
    except ValueError:
        pass
    except Empty:
        label.text = "Text not chosen"
        event.cancel()


def do_the_loop(time, label):
    global event
    event = Clock.schedule_interval(partial(get_from_queue, label), time)


def cancel_event():
    event.cancel()


def stop_loop(label):
    try:
        event.cancel()
    except NameError:
        label.text = "You can't stop something you didn't start"


def get_first(label):
    label.text = storedText[0]


def get_previous(label):
    try:
        label.text = storedText[Global.n - 1]
        Global.n -= 1
    except IndexError:
        label.text = "No more previous words"


def get_next(label):
    try:
        label.text = storedText[Global.n + 1]
        Global.n += 1
    except IndexError:
        label.text = "You can't see words you didn't read yet"


def get_last(label):
    try:
        label.text = storedText[-1]
        Global.n = -1
    except IndexError:
        label.text = "You can't see words you didn't read yet"


def put_in_q(list):
    length = len(list)
    for i in range(length):
        if list[i-1][-1] == '.':
            q.put(list[i])
        else:
            q.put(list[i])


kv = Builder.load_file("my.kv")


class FastPDFreader(App):
    def build(self):
        return kv


if __name__ == "__main__":
    FastPDFreader().run() 
