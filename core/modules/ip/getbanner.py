import socket

def get_banner(self, session, ip):
    result = {}
    ports = [21, 22]
    for port in ports:
        s = socket.socket()
        try:
            s.settimeout(5)
            s.connect((ip, port))
            banner = s.recv(1024).decode("utf-8").strip()
            result[str(port)] = banner
            s.close()
        except Exception as e:
            print(e)
            banner = "Unknown"

    return result if result else {"banner" : "unknown"}