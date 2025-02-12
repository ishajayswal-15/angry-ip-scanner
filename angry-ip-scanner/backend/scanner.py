import socket
import nmap
import requests
import concurrent.futures

def ping(ip):
    """Check if an IP is reachable."""
    try:
        socket.create_connection((ip, 80), timeout=1)
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def scan_ports(ip, start_port=1, end_port=1024):
    """Scan for open ports on a given IP using multithreading."""
    open_ports = []

    def scan(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return port if result == 0 else None

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(scan, range(start_port, end_port + 1))

    open_ports = [port for port in results if port]
    return open_ports


def get_ip_location(ip):
    """Get geolocation information for an IP."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return {
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "isp": data.get("isp"),
        }
    except Exception as e:
        return {"error": str(e)}