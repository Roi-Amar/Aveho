"""
Aveho (by Roi) was built as a small fast side project in order to give a virtual greenscreen with no real greenscreen to the masses.
Feel free to share and use the code.

Aveho provides you with a virtual green screen you can use in a 3rd party applications like OBS or ZOOM
(hint: look for the chroma key filters and set it to filter green)
"""

import time
from tkinter import *

fen = Tk()
fen.title("Aveho")

canv = Canvas(fen, height=300, width=400, bg="white")
canv.grid(row=0, column=0, rowspan=5, padx=5, pady=5)


def start(t=5):
    Countdown.config(state=DISABLED)
    lab.config(text=str(t), bg="white", font=("Impact", 18))
    if t > 0:
        fen.after(1000, start, t - 1)
    else:
        lab.config(text="Snap!", bg="white", font=("Impact", 18))
        time.sleep(0.1)
        fen.destroy()
        exec(open('production.py').read())


aveholbl = Label(fen, text="Aveho", fg="black", bg="white", font=("Impact", 22))
aveholbl.grid(row=0, column=0)

aveholbl2 = Label(fen, text="by Roi", fg="black", bg="white", font=("David", 10))
aveholbl2.grid(row=1, column=0)

aveholbl2 = Label(fen, text="for best performance Aveho need to take a photo\nof the background without you in it,"
                            "\nafter pressing im ready you will \nhave 5 seconds to clear the way.\n\n\nPro tip: leave "
                            "the camera staionary", fg="black", bg="white", font=("David", 14))
aveholbl2.grid(row=2, column=0)

lab = Label(fen, text="", fg="black", bg="white", font=("Impact", 18))
lab.grid(row=4, column=0)

Countdown = Button(fen, text="Im Ready!", command=start, fg="black", bg="white", font=("Impact", 18))
Countdown.grid(row=5, column=0)

fen.mainloop()
