import socket


class Client:
    def __init__(self):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        port = 12345
        self.__client_socket.connect((hostname, port))

    def run_client(self, script):
        script = Client.split_script_to_commands(script)

        for command in script:
            print("Executing command: " + command)
            self.__client_socket.send(command.encode('utf-8'))
            data = self.__client_socket.recv(1024)
            print(data.decode('utf-8'))

    @staticmethod
    def split_script_to_commands(script):
        return script.split("\n")


if __name__ == '__main__':
    client = Client()

    script = (f"SHOW_AIRLINES;\nSHOW_FLIGHTS;\nSHOW_FLIGHTS_FOR_AIRLINE;1;\nADD_AIRLINE;4;BNS;\n"
              f"ADD_FLIGHT;6;3;BERLIN;2024-04-15 15:25:00;2024-04-15 15:25:00;\nSHOW_AIRLINES;\nSHOW_FLIGHTS;\n"
              f"CHANGE_AIRLINE;4;WWW;\nCHANGE_FLIGHT;6;1;MOSCOW;2024-04-15 18:00:00;2024-04-15 18:00:00;\n"
              f"SHOW_AIRLINES;\nSHOW_FLIGHTS;\nDELETE_AIRLINE;4;\nDELETE_FLIGHT;6;\nSHOW_AIRLINES;\nSHOW_FLIGHTS;\n"
              f"SEARCH_AIRLINE;1;\nSEARCH_FLIGHT;1;")
    client.run_client(script)