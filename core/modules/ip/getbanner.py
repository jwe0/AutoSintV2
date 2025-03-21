import socket

def get_banner(self, session, ip, port):
    s = socket.socket()
    try:
        s.settimeout(5)
        s.connect((ip, int(port)))
        banner = s.recv(1024).decode("utf-8").strip()
        s.close()
    except:
        banner = "Unknown"

    return banner