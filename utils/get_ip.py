import socket

from fastapi import HTTPException


def get_ip_address():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
        sock.close()
        return ip_address
    except socket.error:
        raise HTTPException(status_code=500, detail="Error getting IP address")