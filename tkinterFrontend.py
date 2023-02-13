import tkinter
from tkinter import *
from PIL import Image, ImageTk

root = Tk()

Label(root, text = 'Position iamge on button').pack(side = TOP, padx = 0, 
                                                    pady = 0)

photo = PhotoImage(file = "/home/maeve/wallpapers/lofi/samurai.png")
photoimage = photo.subsample(1, 2)

Button(root, image = photoimage,).pack(side = BOTTOM, pady=0)
mainloop()
