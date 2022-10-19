from ast import Num
import tkinter as tk

def initalise() :
    global displayTemp
    displayTemp = 0

r = tk.Tk()
r.title('Green House control')
w=tk.Canvas(r, width=800, height=480)
w.pack()
r.mainloop()