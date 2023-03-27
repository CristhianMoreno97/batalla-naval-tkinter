import socket
import logging
from typing import List, Tuple
from threading import Thread

from networking.network import Network
from networking.constants import CONN_LIMIT, BUFFER_SIZE

class Server(Network):
    """ This class represents server instance. """
    def __init__(self, host_address: str, host_port: int) -> None:
        self.is_first_player = True
        self.server_socket = None
        self.host_address = host_address
        self.host_port = host_port
        self.game_data = {
            'winner': None,
            'game_status': 'lobby',
            'game_grid': {},
            'clients': {},
            'sockets': {}
        }

    def start_server(self) -> None:
        """ This function creates a server socket and start a thread for listening. """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_address, self.host_port))
        self.server_socket.listen(CONN_LIMIT)

        server_thread = Thread(target=self.server_lobby)
        server_thread.start()

    def server_lobby(self) -> None:
        """ This function handles server lobby, waiting for every player is connected. """

        logging.info('Server started!')
        try:
            while True:
                if len(self.game_data['clients']) < CONN_LIMIT:
                    client, address = self.server_socket.accept()

                    client_thread = Thread(
                        target=self.client_listener, args=(client, address))
                    client_thread.start()
        except socket.error:
            logging.info('Server stopped.')
            

    def client_listener(self, client_socket: socket.socket, client_ip: str):
        """ This function listens to clients messages and processes them. """

        socket_disconnected = False

        data = client_socket.recv(BUFFER_SIZE)
        client_name = self.decode_data(data)

        self.__add_client_to_server(client_name, client_socket)
        self.send_data_to_client('Connected', client_name)

        logging.info(
            f'Client "{client_name}" connected from IP: "{client_ip}"')

        # cambia automaticamente a modo batalla cuando hay dos jugadores
        if len(self.game_data['clients']) == CONN_LIMIT:
            self.game_data['game_status'] = 'battle'

        self.set_ships_location(client_name)

        try:
            while True:
                # BUCLE PRINCIPAL
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                decoded_data = self.decode_data(data)
                logging.info(f'Received data: {decoded_data}')

                if 'request' in decoded_data:
                    if decoded_data['request'] == 'game_status':
                        # con estos los clientes saben cuando pasar a la pantalla de batalla
                        self.send_data_to_client(
                            {'game_status': self.game_data['game_status']}, client_name)
                        # datos del tablero
                        if decoded_data['request'] == 'game_data':
                            self.send_data_to_client(
                                {'game_data': self.game_data['clients']}, client_name)
                else:
                    self.send_data_to_client({'message': 'ok'}, client_name)

        except socket.error:
            socket_disconnected = True
            logging.info(f'Client disconnected by server: {client_name}')

        self.__remove_client_from_server(client_name)
        if not socket_disconnected:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

            logging.info(f'Closing game')
            self.end_game() ######### PENDIENTE DE REVISAR

    def set_ships_location(self, client_name: str) -> None:
        # coordenadas de los barcos
        if len(self.game_data['clients'][client_name]) == 1:
            self.game_data['clients'][client_name]['ships_location'] = [[0,2],[2,4],[9,9]]
            self.game_data['clients'][client_name]['ships_sinked_location'] = []
        elif len(self.game_data['clients'][client_name]) == 2:
            self.game_data['clients'][client_name]['ships_location'] = [[0,1],[2,3],[9,8]]
            self.game_data['clients'][client_name]['ships_sinked_location'] = []

    def send_data_to_client(self, data: object, client_name: str) -> None:
        """ This function sends data to a specific client. """

        message = self.create_datagram(BUFFER_SIZE, data)
        self.game_data['sockets'][client_name].sendall(message)

    def __add_client_to_server(
            self,
            client_name: str,
            client_socket: socket.socket) -> None:
        """ This function adds a client to game_data. """

        self.game_data['clients'][client_name] = {
            'attacked_tile': {
                'ship_name': None,
                'position': None
            },
            'sinked_ships': 0,
            'ship_locked': False,
            'my_turn': self.is_first_player
        }
        self.game_data['game_grid'][client_name] = None
        self.game_data['sockets'][client_name] = client_socket
        self.is_first_player = False

    def stop_server(self) -> None:
        """ This function stops current server. """

        self.end_game()
        self.server_socket.close()

    def get_connected_clients(self) -> List[str]:
        """ This function returns connected clients. """
        return self.game_data['clients'].keys()
    
    def __remove_client_from_server(self, client_name: str) -> None:
        """ This function removes client from game_data. """
        self.game_data['clients'].pop(client_name, None)
        self.game_data['sockets'].pop(client_name, None)
        self.game_data['game_grid'].pop(client_name, None)

    def end_game(self) -> None:
        """ This function ends game by cleaning server connections. """

        for client_name in self.game_data['sockets']:
            self.game_data['sockets'][client_name].shutdown(socket.SHUT_RDWR)
            self.game_data['sockets'][client_name].close()