from ._version import __version__

class System:

    def info(self):
        return {
            "version": __version__,
            "os": "Raspberry Pi OS v2.3",
            "hostname": "foobar",
            "network": {
                "eth": {
                    "mac": "qsdfsdfm",
                    "ip": "sdfousdf",
                    "status": "online"
                },
                "eth": {
                    "mac": "qsdfsdfm",
                    "ip": "sdfousdf",
                    "status": "offline"
                }
            },
            "python": {
                "version": "1.2.3"
            },
            "node": {
                "version": "1.2.3"
            },
            "uptime": 12345
        }