import tkinter as tk
from tkinter import Label
import threading
from PIL import ImageTk, Image

class Battle:
    """ This class manages Battle stage. """

    def __init__(self, client) -> None:
        self.states = {
            'client': client,
            'winner_name': None,
            'game_finished': False,
            'maps_ships_loaded': False,
            'last_selected_ship': -1
        }
        self.board_props = {
            'w_width': 750,
            'w_height': 420,
            'offset': 45, # valor calculado a prueba y error
        }
        print('ventata battle')
        self.window_thread = threading.Thread(target=self.show_window)
        self.window_thread.start()

    def show_window(self) -> None:
        self.window_parent = tk.Tk(className='Batalla naval - Board')
        self.window_parent.resizable(width=False, height=False)
        
        frame = tk.Frame(self.window_parent)
        frame.pack()
        
        self.canvas = tk.Canvas(
            frame, bg="black",
            width=self.board_props['w_width'],
            height=self.board_props['w_height'])
        self.canvas.pack()

        bg = tk.PhotoImage(file="public/board.png").subsample(2)
        self.canvas.create_image(bg.width()/2,bg.height()/2,image=bg)
        
        # obtener ubicacion de los barcos
        game_data = self.states['client'].get_game_data()
        ships_location = game_data['client'][self.states['client'].client_name]['ships_location']
        ships_sinked_location = game_data['client'][self.states['client'].client_name]['ships_sinked_location']

        self.ship_images = []
        for i in range(len(ships_location)):
            self.ship_images.append(
                tk.PhotoImage(file="public/icons8-viking-ship-48.png").subsample(2))
            pos_x = ships_location[i][0]
            pos_y = ships_location[i][1]
            self.canvas.create_image(45+32.5*pos_x, 80+32.5*pos_y, Image=self.ship_images[-1])
        
        right_panel = tk.Frame(self.window_parent)
        right_panel.pack(side=tk.RIGHT)

        button = tk.Button(right_panel, text="Eliminar img", command=self.eliminar_ultima_imagen)
        button.pack()

        label1 = tk.Label(right_panel, text="Campo 1")
        label1.pack()
        entry1 = tk.Entry(right_panel)
        entry1.pack()
        label2 = tk.Label(right_panel, text="Campo 2")
        label2.pack()
        entry2 = tk.Entry(right_panel)
        entry2.pack()


        self.window_parent.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window_parent.mainloop()

    def close_window(self):
        self.window_parent.destroy()
        self.window_thread.join()

    def eliminar_ultima_imagen(self):
        if self.ship_images:
            self.canvas.delete(self.ship_images[-1])
            self.ship_images.pop()