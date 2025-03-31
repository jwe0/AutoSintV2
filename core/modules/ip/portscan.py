import json, threading, socket
from concurrent.futures import ThreadPoolExecutor, as_completed


class Portscan:
    def __init__(self):
        self.progress = 0
        self.result = {}
        self.lock = threading.Lock()

    def lookup(self, port):
        ports = json.loads(open("ports.json").read())
        return ports[str(port)] if str(port) in ports else {"service": "Unknown", "protocols": "Unknown"}

    def banner(self, host, port):
        try:
            s = socket.socket()
            s.settimeout(5)
            s.connect((host, int(port)))
            banner = s.recv(1024).decode("utf-8").strip()
            s.close()
            return banner
        except:
            return "Unknown"

    def scan(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            con = s.connect_ex((host, int(port)))
            if con == 0:
                info = self.lookup(port)
                banner_ = self.banner(host, port)
                self.result[port] = {"service": info["service"], "protocol": info["protocols"], "banner": banner_}
                self.progress += 1
            else:
                self.progress += 1
        except:
            self.progress += 1

    def start(self, ip):
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(self.scan, ip, port) for port in range(1, 65535)]
            for future in as_completed(futures):
                with self.lock:
                    completed = (self.progress / 65535) * 100
                if completed % 10 == 0:
                    print(f"Scanning: {int(completed)}%")

        return self.result


def portscan(self, session, ip):
    scan = Portscan()
    return scan.start(ip)