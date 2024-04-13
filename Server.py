import socket
from Airport import Airport

class Server:
    def __init__(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        port = 12345
        self.__server_socket.bind((hostname, port))
        self.__server_socket.listen(5)

        print(f"Running server on host {hostname} port {port}")

        url = "localhost"
        user = "root"
        password = "Password123"
        self.__airport = Airport(url, user, password)
        print("Connection to DB established")

        print('Waiting for a connection...')

    def run_server(self):
        client, address = self.__server_socket.accept()
        print(f'Accepted connection from {address}')
        while True:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            method, *params = data.split(';')
            response = self.handle_request(method, params)
            client.sendall(response.encode('utf-8'))

    def handle_request(self, method, params):
        result = None
        if method == 'SHOW_AIRLINES':
            result = self.__airport.show_airlines_str()
        elif method == 'SHOW_FLIGHTS':
            result = self.__airport.show_flights_str()
        elif method == 'SHOW_FLIGHTS_FOR_AIRLINE':
            id = int(params[0])
            result = self.__airport.show_flights_for_airline_str(id)
        elif method == 'ADD_AIRLINE':
            id = int(params[0])
            name = params[1]
            self.__airport.add_airline(id, name)
            result = "ADDED AIRLINE"
        elif method == 'ADD_FLIGHT':
            id = int(params[0])
            airline_id = int(params[1])
            destination = params[2]
            departure_time = params[3]
            arrival_time = params[4]
            self.__airport.add_flight(id, airline_id, destination, departure_time, arrival_time)
            result = "ADDED FLIGHT"
        elif method == 'CHANGE_AIRLINE':
            id = int(params[0])
            name = params[1]
            self.__airport.change_airline(id, name)
            result = "CHANGED AIRLINE"
        elif method == 'CHANGE_FLIGHT':
            id = int(params[0])
            airline_id = int(params[1])
            destination = params[2]
            departure_time = params[3]
            arrival_time = params[4]
            self.__airport.change_flight(id, airline_id, destination, departure_time, arrival_time)
            result = "CHANGED FLIGHT"
        elif method == 'DELETE_AIRLINE':
            id = int(params[0])
            self.__airport.delete_airline(id)
            result = "DELETED AIRLINE"
        elif method == 'DELETE_FLIGHT':
            id = int(params[0])
            self.__airport.delete_flight(id)
            result = "DELETED FLIGHT"
        elif method == 'SEARCH_AIRLINE':
            id = int(params[0])
            result = self.__airport.search_airline_str(id)
        elif method == 'SEARCH_FLIGHT':
            id = int(params[0])
            result = self.__airport.search_flight_str(id)
        else:
            pass
        if result is not None:
            return result
        else:
            return "Something went wrong in executed command\n"


if __name__ == '__main__':
    server = Server()
    server.run_server()