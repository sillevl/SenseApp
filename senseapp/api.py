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
                message = json.loads(data.decode("utf-8"))
                print(f"New message: {message}")

                if "get" in message.keys():
                    for key in message["get"]:
                        if key == "system_info":
                            self.get_system_info(conn)
                        if key == "settings":
                            self.get_all_settings(conn)

                if "post" in message.keys():
                    for key in message["post"]:
                        if key == "settings":
                            self.update_settings(message["post"]["settings"])


    def get_all_settings(self, conn):
        conn.send(str.encode(json.dumps(self.context.settings_manager.get_all())))

    def get_system_info(self, conn):
        conn.send(str.encode(json.dumps(self.context.system_manager.info())))
        
    def update_settings(self, settings):
        self.context.settings_manager.set_all(settings)
        print(self.context.settings_manager.get_all())

    def update_sensor_values(self, sensor_values):
        for client in self.clients:
            try:
                client.send(str.encode(json.dumps(sensor_values)))
            except BrokenPipeError:
                self.clients.remove(client)

