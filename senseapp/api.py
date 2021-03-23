import threading
import socket,os
import json

DEAULT_SOCKET_PATH="/tmp/senseapp.sock"

class API:

    socket = None
    thread = None
    context = None
    clients = []

    def __init__(self, context, socket_file_path = DEAULT_SOCKET_PATH):
        self.context = context
        self.thread = threading.Thread( target=self.wait_for_message, args=())
        self.thread.daemon = True

    def connect(self, socket_file_path = DEAULT_SOCKET_PATH):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove(socket_file_path)
        except OSError:
            pass
        self.socket.bind(socket_file_path)
        os.chmod(socket_file_path, 0o777)
        self.socket.listen(1)
        self.run()

    def run(self):
        # TODO only run when connected
        self.thread.start()

    def wait_for_message(self):
        while True:
            conn, addr = self.socket.accept()
            self.clients.append(conn)
            print("Socket connected", conn, addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                data = data.decode("utf-8")

                decoder = json.JSONDecoder()
                data = data.lstrip() # decode hates leading whitespace
                while data:
                    message, index = decoder.raw_decode(data)
                    data = data[index:].lstrip()

                    if "get" in message.keys():
                        for key in message["get"]:
                            if key == "settings":
                                self.get_all_settings(conn)

                    if "post" in message.keys():
                        for key in message["post"]:
                            if key == "settings":
                                self.update_settings(message["post"]["settings"])


    def get_all_settings(self, conn):
        self.send("settings", self.context.settings_manager.get_all(), conn)
        
    def update_settings(self, settings):
        self.context.settings_manager.set_all(settings)
        print(self.context.settings_manager.get_all())
        for client in self.clients:
            self.get_all_settings(client)

    def update_sensor_values(self, sensor_values):
        for client in self.clients:
            self.send("sensor_values", sensor_values, client)


    def send(self, type, data, conn):
        payload = {
            type: data
        }
        try:
            conn.send(str.encode(json.dumps(payload) + ""))
        except BrokenPipeError:
            print("[ERROR] Websocket pipe broken, removing client")
            self.clients.remove(conn)
