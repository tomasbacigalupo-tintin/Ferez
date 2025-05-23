import socket
import subprocess
from dataclasses import dataclass
from typing import List

import psutil


@dataclass
class PingResult:
    host: str
    reachable: bool
    output: str


def ping(host: str, count: int = 1) -> PingResult:
    """Ping a host using the system ping command."""
    cmd = ["ping", "-n" if psutil.WINDOWS else "-c", str(count), host]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        reachable = proc.returncode == 0
        output = proc.stdout + proc.stderr
    except Exception as e:
        reachable = False
        output = str(e)
    return PingResult(host, reachable, output)


def get_default_gateway() -> str:
    """Return the default gateway IP or empty string."""
    if psutil.WINDOWS:
        cmd = ["ipconfig"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                if "Default Gateway" in line:
                    parts = line.split(":")
                    if len(parts) > 1 and parts[1].strip():
                        return parts[1].strip()
    elif psutil.MACOS:
        cmd = ["route", "-n", "get", "default"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                if "gateway:" in line:
                    return line.split()[1]
    else:
        cmd = ["ip", "route", "show", "default"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            parts = proc.stdout.split()
            if "via" in parts:
                return parts[parts.index("via") + 1]
    return ""


def check_gateway() -> bool:
    gw = get_default_gateway()
    if not gw:
        return False
    return ping(gw).reachable


def detect_ip_conflict() -> bool:
    """Return True if an IP conflict is detected."""
    ips = [addr.address for addrs in psutil.net_if_addrs().values() for addr in addrs if addr.family == socket.AF_INET]
    try:
        proc = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        if proc.returncode == 0:
            for ip in ips:
                if proc.stdout.count(ip) > 1:
                    return True
    except FileNotFoundError:
        pass
    return False


def scan_open_ports(host: str, ports: List[int]) -> List[int]:
    """Scan a list of ports on the given host and return those that are open."""
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                open_ports.append(port)
            except Exception:
                pass
    return open_ports


def resolve_hostname(hostname: str) -> bool:
    """Return True if the hostname can be resolved via DNS."""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False
