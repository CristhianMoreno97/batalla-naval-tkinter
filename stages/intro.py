import tkinter as tk
import threading

from networking.client import Client

class Intro:
    """ This class manages Intro stage. """
    def __init__(self) -> None:
        self.states = {
            'client': None,
            #'players_connected': False
        }
        self.all_players_connected = False
        self.window_battle = None
        #self.window_thread = threading.Thread(target=self.show_window)
        #self.window_thread.start()

    def show_window(self) -> None:
        self.window_parent = tk.Tk(className='Batalla naval - cliente - grupo 1')
        self.window_parent.geometry('300x300')
        self.window_parent.resizable(width=False, height=False)
        self.window_parent.eval('tk::PlaceWindow . center')

        self.polling_interval = 1000

        self.label_host = tk.Label(
            self.window_parent, text="Host:")
        self.label_host.place(x=20, y=20)
        self.input_host = tk.Entry(self.window_parent)
        self.input_host.place(x=140, y=20, width=100)
        
        self.label_port = tk.Label(
            self.window_parent, text="port:")
        self.label_port.place(x=20, y=60)
        self.input_port = tk.Entry(self.window_parent)
        self.input_port.place(x=140, y=60, width=100)
        
        self.label_username = tk.Label(
            self.window_parent, text="username:")
        self.label_username.place(x=20, y=100)
        self.input_username = tk.Entry(self.window_parent)
        self.input_username.place(x=140, y=100, width=100)

        self.button_connect = tk.Button(
            self.window_parent, text="Conectarse", command=self.connect_to_server)
        self.button_connect.place(x=20, y=140)


        self.label_state_conn = tk.Label(
            self.window_parent, text="Bienvenido")
        self.label_state_conn.place(x=20, y=220)

        self.label_state_conn.after(
            self.polling_interval,
            self.refresh_clients_display)

        self.window_parent.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window_parent.mainloop()

    def refresh_clients_display(self) -> None:
        if self.all_players_connected:
            self.label_state_conn.config(text=f"jugadores conectados")

            self.window_parent.destroy()
            self.window_parent =  None
            if not self.window_battle:
                self.show_window_battle()
        if self.window_parent:
            self.label_state_conn.after(self.polling_interval,
                                    self.refresh_clients_display)
        

    def show_window_battle(self):
        self.window_battle = tk.Tk(className='Batalla naval - cliente - grupo 1')
        frame = tk.Frame(self.window_battle)
        frame.pack(side=tk.LEFT)
        self.canvas_battle = tk.Canvas(frame, bg="black", width=750, height=420)
        self.canvas_battle.pack()
        bg = tk.PhotoImage(file="public/board.png").subsample(2)
        self.canvas_battle.create_image(bg.width()/2, bg.height()/2, image=bg)
        
        hilo2 = threading.Thread(target=self.tarea_ciclica2)
            # Iniciar el hilo
        hilo2.start()

        self.window_battle.mainloop()

    def tarea_ciclica2(self):
        # pedir datos de la partida
        while True:
            #game_data = self.states['client'].get_game_data() ### aqui deben llegar las coordenadas de los barcos vivos y los barcos hundidos. get_game_data no esta funcionando
            game_data = self.states['client'].get_game_status()
            print(game_data)
            print('---')

    def connect_to_server(self) -> None:
        # obtener los datos de los campos
        host_address = self.input_host.get()
        host_port = self.input_port.get()
        username = self.input_username.get()
        # crear instancia de clientes
        client = Client(username, host_address, host_port)

        if client.connect_to_server():
            self.states['client'] = client
            self.label_state_conn.config(
                text=f"conexion establecida.\nEsperando conexion de otro jugador...")
            self.button_connect.config(state=tk.DISABLED)
            # Crear un hilo para ejecutar la tarea cíclica
            hilo = threading.Thread(target=self.tarea_ciclica)
            # Iniciar el hilo
            hilo.start()
        else:
            self.label_state_conn.config(
                text=f"No fue posible conectarse al sevidor.")
    
    def tarea_ciclica(self) -> None:
        while not self.ask_for_all_players_connected():
            print('esperando jugador')
        
        self.all_players_connected = True

    def ask_for_all_players_connected(self) -> bool:
        """
          This function fetchs game status from server
          and checks if all clients are ready.
        """
        print('all_players_connected?')
        if self.states['client']:
            game_status = self.states['client'].get_game_status()
            return game_status != 'lobby'
        
        return False
    
    def close_window(self):
        self.window_parent.destroy()
        #self.window_thread.join()
        print('close')
