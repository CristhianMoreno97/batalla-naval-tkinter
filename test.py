import tkinter as tk
from tkinter import Label, Canvas, NW, Frame, PhotoImage
from PIL import ImageTk, Image

#window_parent = tk.Tk(className='Batalla naval - cliente - grupo 1')
#window_parent.geometry('1500x840+0+0')
#window_parent.eval('tk::PlaceWindow . center')

grid = [['A', 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['A', 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 'A']]

# 'A': barco, 'X': barco destruido
def eliminar_ultima_imagen():
    if character_images:
        canvas.delete(character_images[-1])
        character_images.pop()

window_parent = tk.Tk(className='Batalla naval - cliente - grupo 1')

frame = tk.Frame(window_parent)
frame.pack(side=tk.LEFT)

canvas = tk.Canvas(frame, bg="black", width=750, height=420)
canvas.pack()

bg = tk.PhotoImage(file="public/board.png").subsample(2)
canvas.create_image(bg.width()/2, bg.height()/2, image=bg)

character_images = []
character_images.append(tk.PhotoImage(file="public/icons8-viking-ship-48.png").subsample(2))
canvas.create_image(45,80,image=character_images[-1])
character_images.append(tk.PhotoImage(file="public/icons8-viking-ship-48.png").subsample(2))
canvas.create_image(45+32.5*9,80,image=character_images[-1])
character_images.append(tk.PhotoImage(file="public/icons8-viking-ship-48.png").subsample(2))
canvas.create_image(45+32.5*8,80+32.5*9,image=character_images[-1])

right_panel = tk.Frame(window_parent)
right_panel.pack(side=tk.RIGHT)

button = tk.Button(right_panel, text="Eliminar img", command=eliminar_ultima_imagen)
button.pack()

label1 = tk.Label(right_panel, text="Campo 1")
label1.pack()
entry1 = tk.Entry(right_panel)
entry1.pack()
label2 = tk.Label(right_panel, text="Campo 2")
label2.pack()
entry2 = tk.Entry(right_panel)
entry2.pack()

window_parent.mainloop()