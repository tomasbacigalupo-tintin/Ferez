import platform
import socket

from . import system
from .logger import Logger


class WiFiFixCore:
    def __init__(self, logger=None):
        self.logger = logger or Logger()

    def restart_adapter(self):
        os_name = platform.system()
        iface = system.get_interface()
        if os_name == "Windows":
            commands = [["netsh", "interface", "set", "interface", iface, "DISABLED"],
                        ["netsh", "interface", "set", "interface", iface, "ENABLED"]]
        elif os_name == "Darwin":
            commands = [["sudo", "ifconfig", iface, "down"], ["sudo", "ifconfig", iface, "up"]]
        else:
            commands = [["sudo", "ip", "link", "set", iface, "down"], ["sudo", "ip", "link", "set", iface, "up"]]
        success, output = system.run_commands(commands)
        self.logger.log("Reiniciar adaptador", success, output)
        self.logger.flush()
        return success

    def renew_ip(self):
        os_name = platform.system()
        if os_name == "Windows":
            commands = [["ipconfig", "/release"], ["ipconfig", "/renew"]]
        elif os_name == "Darwin":
            iface = system.get_interface()
            commands = [["sudo", "ipconfig", "set", iface, "DHCP"]]
        else:
            commands = [["sudo", "dhclient", "-r"], ["sudo", "dhclient"]]
        success, output = system.run_commands(commands)
        self.logger.log("Renovar IP", success, output)
        self.logger.flush()
        return success

    def flush_dns(self):
        os_name = platform.system()
        if os_name == "Windows":
            commands = [["ipconfig", "/flushdns"]]
        elif os_name == "Darwin":
            commands = [["sudo", "dscacheutil", "-flushcache"], ["sudo", "killall", "-HUP", "mDNSResponder"]]
        else:
            commands = [["sudo", "systemd-resolve", "--flush-caches"]]
        success, output = system.run_commands(commands)
        self.logger.log("Limpiar DNS", success, output)
        self.logger.flush()
        return success

    def change_dns(self):
        os_name = platform.system()
        iface = system.get_interface()
        if os_name == "Windows":
            commands = [["netsh", "interface", "ip", "set", "dns", f"name={iface}", "static", "8.8.8.8"],
                        ["netsh", "interface", "ip", "add", "dns", f"name={iface}", "8.8.4.4", "index=2"]]
        elif os_name == "Darwin":
            commands = [["sudo", "networksetup", "-setdnsservers", "Wi-Fi", "8.8.8.8", "8.8.4.4"]]
        else:
            commands = [["sudo", "nmcli", "device", "modify", iface, "ipv4.dns", "8.8.8.8 8.8.4.4"],
                        ["sudo", "systemctl", "restart", "NetworkManager"]]
        success, output = system.run_commands(commands)
        self.logger.log("Cambiar DNS", success, output)
        self.logger.flush()
        return success

    def check_connection(self):
        os_name = platform.system()
        cmd = ["ping", "-c", "1", "8.8.8.8"] if os_name != "Windows" else ["ping", "-n", "1", "8.8.8.8"]
        success, output = system.run_command(cmd)
        self.logger.log("Verificar conexión", success, output)
        self.logger.flush()
        return success

    def get_current_ip(self):
        os_name = platform.system()
        iface = system.get_interface()
        if os_name == "Windows":
            success, output = system.run_command(["ipconfig"])
            if success:
                for line in output.splitlines():
                    if "IPv4" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            return parts[1].strip()
        elif os_name == "Darwin":
            success, output = system.run_command(["ipconfig", "getifaddr", iface])
            if success:
                return output.strip()
        else:
            success, output = system.run_command(["ip", "-4", "addr", "show", iface])
            if success:
                for line in output.splitlines():
                    line = line.strip()
                    if line.startswith("inet "):
                        return line.split()[1].split("/")[0]
        return ""

    def get_default_gateway(self):
        os_name = platform.system()
        if os_name == "Windows":
            success, output = system.run_command(["ipconfig"])
            if success:
                for line in output.splitlines():
                    if "Default Gateway" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            gw = parts[1].strip()
                            if gw:
                                return gw
        elif os_name == "Darwin":
            success, output = system.run_command(["route", "-n", "get", "default"])
            if success:
                for line in output.splitlines():
                    if "gateway:" in line:
                        return line.split()[1]
        else:
            success, output = system.run_command(["ip", "route", "show", "default"])
            if success:
                parts = output.strip().split()
                if "via" in parts:
                    idx = parts.index("via")
                    return parts[idx + 1]
        return ""

    def check_gateway(self):
        gateway = self.get_default_gateway()
        if not gateway:
            self.logger.log("Verificar gateway", False, "No se detectó la puerta de enlace")
            self.logger.flush()
            return False
        os_name = platform.system()
        cmd = ["ping", "-c", "1", gateway] if os_name != "Windows" else ["ping", "-n", "1", gateway]
        success, output = system.run_command(cmd)
        self.logger.log("Verificar gateway", success, output)
        self.logger.flush()
        return success

    def detect_ip_conflict(self):
        ip = self.get_current_ip()
        if not ip:
            self.logger.log("Detectar conflicto IP", False, "No se obtuvo IP actual")
            self.logger.flush()
            return False
        os_name = platform.system()
        cmd = ["arp", "-a"] if os_name == "Windows" else ["arp", "-n"]
        success, output = system.run_command(cmd)
        conflict = False
        if success:
            if output.count(ip) > 1:
                conflict = True
        self.logger.log("Detectar conflicto IP", not conflict, output)
        self.logger.flush()
        return not conflict

    def check_dhcp(self):
        ip = self.get_current_ip()
        problem = ip.startswith("169.254.") or ip == ""
        self.logger.log("Verificar DHCP", not problem, f"IP actual: {ip}")
        self.logger.flush()
        return not problem

    def check_port(self, host="8.8.8.8", port=53):
        try:
            with socket.create_connection((host, port), timeout=3):
                success = True
                output = "Conexión exitosa"
        except Exception as e:
            success = False
            output = str(e)
        self.logger.log(f"Verificar puerto {port}", success, output)
        self.logger.flush()
        return success

    def diagnose_network(self):
        results = {
            "connection": self.check_connection(),
            "gateway": self.check_gateway(),
            "dhcp": self.check_dhcp(),
            "ip_conflict": self.detect_ip_conflict(),
            "port_53": self.check_port(),
        }
        return results

    def fix_all(self):
        self.restart_adapter()
        self.renew_ip()
        self.flush_dns()
        self.change_dns()
        success = self.check_connection()
        return success
