# This calculator makes only one type of operation at once 

from tkinter import *
import numpy
from functools import reduce


root = Tk()
root.title("Calculator")


e = Entry(root, width = 35, borderwidth = 5, bg="white")
e.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)
e.insert(0, "0")


def button_click(number):
    current = e.get()
    if current == "0":
        e.delete(0, END)
        e.insert(0, str(number))

    elif current == "Error":
        e.delete(0, END)
        e.insert(0, str(number))

    else:
        e.delete(0, END)
        e.insert(0, str(current) + str(number))


def button_clear():
    e.delete(0, END)


def button_back():
    txt= e.get()[:-1] 
    e.delete(0, END) 
    e.insert(0, txt)


def button_add():
    global math
    math = "add"
    e.insert(END, "+")


def button_min():
    global math
    math = "min"
    e.insert(END, "-")


def button_multi():
    global math
    math = "multi"
    e.insert(END, "*")


def button_div():
    global math
    math = "divide"
    e.insert(END, "/")

    
def button_dot():
    first_number = e.get()
    e.insert (END, ".")


def split_list(symbol):
    x = symbol
    if symbol == "-":
        numbers = e.get()
        e.delete(0, END)
        e.insert(0, "0" + numbers)
        numbers = e.get()
        listOfNumbers = numbers.split(x)
        listOfNumbers = [float(i) for i in listOfNumbers]
        return listOfNumbers
    else:
        x = symbol
        numbers = e.get()
        listOfNumbers = numbers.split(x)
        listOfNumbers = [float(i) for i in listOfNumbers]
        return listOfNumbers


def button_equal():

    try:
        if math == "add":
            calculatedNumbers = split_list("+")
            e.delete(0, END)
            e.insert(0, sum(calculatedNumbers))

        if math == "min":
            listOfNumbers = split_list("-")
            calculatedNumbers = reduce(lambda x, y: x-y, listOfNumbers)
            # reduce - subtraction numbers within a list
            e.delete(0, END)
            e.insert(0, calculatedNumbers)
    
        if math == "multi":
            listOfNumbers = split_list("*")
            # numpy.prod - function to multiply numbers inside a list
            calculatedNumbers = numpy.prod(listOfNumbers)
            e.delete(0, END)
            e.insert(0, calculatedNumbers)

        if math == "divide":
            listOfNumbers = split_list("/")
            calculatedNumbers = reduce(lambda x, y: x/y, listOfNumbers)
            e.delete(0, END)
            e.insert(0, calculatedNumbers)
    
    except ValueError:
            e.delete(0, END)
            e.insert(0, "Error. One type of operation only")
    
    except ZeroDivisionError:
            e.delete(0, END)
            e.insert(0, "You can't divide by 0")


# define buttons
button_1 = Button(root, text="1", padx = 40, pady = 20, command=lambda: button_click(1))
button_2 = Button(root, text="2", padx = 40, pady = 20, command=lambda: button_click(2))
button_3 = Button(root, text="3", padx = 40, pady = 20, command=lambda: button_click(3))
button_4 = Button(root, text="4", padx = 40, pady = 20, command=lambda: button_click(4))
button_5 = Button(root, text="5", padx = 40, pady = 20, command=lambda: button_click(5))
button_6 = Button(root, text="6", padx = 40, pady = 20, command=lambda: button_click(6))
button_7 = Button(root, text="7", padx = 40, pady = 20, command=lambda: button_click(7))
button_8 = Button(root, text="8", padx = 40, pady = 20, command=lambda: button_click(8))
button_9 = Button(root, text="9", padx = 40, pady = 20, command=lambda: button_click(9))
button_0 = Button(root, text="0", padx = 40, pady = 20, command=lambda: button_click(0))

button_plus = Button(root, text="+", padx = 43, pady = 20, command=button_add)
button_minus = Button(root, text=" -", padx = 43, pady = 20, command=button_min)
button_multiply = Button(root, text=" *", padx = 43, pady = 20, command=button_multi)
button_divide = Button(root, text=" /", padx = 43, pady = 20, command=button_div)
button_equals = Button(root, text="=", padx = 40, pady = 20, command=button_equal)
button_dot = Button(root, text=" .", padx = 40, pady = 20, command=button_dot)
button_clear = Button(root, text="AC", padx = 39, pady = 20, command=button_clear)
button_backspace = Button(root, text="Backspace", padx = 38, pady = 20, command=button_back)

# put buttons on the screen
button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_0.grid(row=4, column=1)

button_plus.grid(row=1, column=3)
button_minus.grid(row=2, column=3)
button_multiply.grid(row=3, column=3)
button_divide.grid(row=4, column=3)
button_equals.grid(row=4, column=2)
button_dot.grid(row=4, column=0)
button_clear.grid(row=0, column=3)
button_backspace.grid(row=0, column=4)


root.mainloop()
