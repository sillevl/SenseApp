from ._version import __version__
import platform
import psutil
import os
import sys
import socket

class System:

    def get_networks(self):
        interfaces = psutil.net_if_addrs()
        results = {}
        for interface in interfaces:
            if interface == 'lo': continue
            results[interface] = { "mac": None, "ip": None}
            for sni in interfaces[interface]:
                if sni.family == socket.AF_PACKET:
                    results[interface]["mac"] = sni.address
                if sni.family == socket.AF_INET:
                    results[interface]["ip"] = sni.address
        return results

    def info(self):
        return {
            "version": __version__,
            "os": platform.platform(),
            "hostname": platform.node(),
            "network": self.get_networks(),
            "python": {
                "version": sys.version.partition("\n")[0]
            },
            "node": {
                "version": os.popen("node --version").read().partition("\n")[0]
            },
            "uptime": os.popen('uptime -p').read()[:-1]
        }