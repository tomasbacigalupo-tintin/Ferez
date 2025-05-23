import os
import platform
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import socket


class WiFiFixer:
    """Aplicación para diagnosticar y corregir problemas de conectividad WiFi."""

    def __init__(self, root):
        self.root = root
        root.title("WiFi Fixer")
        root.geometry("420x480")
        self.status_var = tk.StringVar()
        self.status_var.set("Estado de conexión: desconocido")

        home = os.path.expanduser("~")
        self.report_path = os.path.join(home, "wifi_fix_report.txt")

        tk.Label(root, textvariable=self.status_var, font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Verificar conexión", command=self.check_connection).pack(pady=5)
        tk.Button(root, text="Reiniciar adaptador", command=self.restart_adapter).pack(pady=5)
        tk.Button(root, text="Renovar IP", command=self.renew_ip).pack(pady=5)
        tk.Button(root, text="Limpiar DNS", command=self.flush_dns).pack(pady=5)
        tk.Button(root, text="Cambiar DNS", command=self.change_dns).pack(pady=5)
        tk.Button(root, text="Diagnóstico avanzado", command=self.diagnose_network).pack(pady=5)
        tk.Button(root, text="Arreglar todo", command=self.fix_all, bg="lightgreen").pack(pady=10)
        tk.Button(root, text="Abrir reporte", command=self.open_report).pack(pady=5)

        self.report = []

    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            success = result.returncode == 0
            output = result.stdout + result.stderr
        except Exception as e:
            success = False
            output = str(e)
        return success, output

    def run_commands(self, commands):
        """Ejecuta una lista de comandos y devuelve el estado acumulado."""
        success = True
        output_total = ""
        for cmd in commands:
            ok, out = self.run_command(cmd)
            success = success and ok
            output_total += out
        return success, output_total

    def log(self, action, success, output):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{now} - {action}: {'OK' if success else 'ERROR'}\n{output}\n"
        self.report.append(entry)

    def write_report(self):
        with open(self.report_path, "a", encoding='utf-8') as f:
            for line in self.report:
                f.write(line)
            f.write("\n")
        self.report = []

    def open_report(self):
        """Abre el archivo de reporte con el visor de texto por defecto."""
        if os.path.exists(self.report_path):
            if platform.system() == "Windows":
                os.startfile(self.report_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.report_path])
            else:
                subprocess.Popen(["xdg-open", self.report_path])
        else:
            messagebox.showinfo("Abrir reporte", "El archivo de reporte aún no existe")

    def check_connection(self):
        os_name = platform.system()
        cmd = ["ping", "-c", "1", "8.8.8.8"] if os_name != "Windows" else ["ping", "-n", "1", "8.8.8.8"]
        success, output = self.run_command(cmd)
        self.status_var.set("Estado de conexión: Conectado" if success else "Estado de conexión: Sin conexión")
        messagebox.showinfo("Verificar conexión", "Conectado a internet" if success else "Sin conexión a internet")
        self.log("Verificar conexión", success, output)
        self.write_report()

    def get_windows_interface(self):
        success, output = self.run_command(["netsh", "interface", "show", "interface"])
        if success:
            for line in output.splitlines():
                if "Connected" in line:
                    parts = line.split()
                    if parts:
                        return parts[-1]
        return "Wi-Fi"

    def get_linux_interface(self):
        success, output = self.run_command(["nmcli", "-t", "-f", "DEVICE,STATE", "device"])
        if success:
            for line in output.splitlines():
                if line.endswith(":connected"):
                    return line.split(":")[0]
        return "wlan0"

    def get_macos_interface(self):
        return "en0"

    def restart_adapter(self):
        os_name = platform.system()
        if os_name == "Windows":
            iface = self.get_windows_interface()
            commands = [["netsh", "interface", "set", "interface", iface, "DISABLED"],
                        ["netsh", "interface", "set", "interface", iface, "ENABLED"]]
        elif os_name == "Darwin":
            iface = self.get_macos_interface()
            commands = [["sudo", "ifconfig", iface, "down"], ["sudo", "ifconfig", iface, "up"]]
        else:
            iface = self.get_linux_interface()
            commands = [["sudo", "ip", "link", "set", iface, "down"], ["sudo", "ip", "link", "set", iface, "up"]]
        success, output_total = self.run_commands(commands)
        messagebox.showinfo("Reiniciar adaptador", "Completado" if success else "Hubo errores")
        self.log("Reiniciar adaptador", success, output_total)
        self.write_report()

    def renew_ip(self):
        os_name = platform.system()
        if os_name == "Windows":
            commands = [["ipconfig", "/release"], ["ipconfig", "/renew"]]
        elif os_name == "Darwin":
            iface = self.get_macos_interface()
            commands = [["sudo", "ipconfig", "set", iface, "DHCP"]]
        else:
            commands = [["sudo", "dhclient", "-r"], ["sudo", "dhclient"]]
        success, output_total = self.run_commands(commands)
        messagebox.showinfo("Renovar IP", "Completado" if success else "Hubo errores")
        self.log("Renovar IP", success, output_total)
        self.write_report()

    def flush_dns(self):
        os_name = platform.system()
        if os_name == "Windows":
            commands = [["ipconfig", "/flushdns"]]
        elif os_name == "Darwin":
            commands = [["sudo", "dscacheutil", "-flushcache"], ["sudo", "killall", "-HUP", "mDNSResponder"]]
        else:
            commands = [["sudo", "systemd-resolve", "--flush-caches"]]
        success, output_total = self.run_commands(commands)
        messagebox.showinfo("Limpiar DNS", "Completado" if success else "Hubo errores")
        self.log("Limpiar DNS", success, output_total)
        self.write_report()

    def change_dns(self):
        os_name = platform.system()
        if os_name == "Windows":
            iface = self.get_windows_interface()
            commands = [["netsh", "interface", "ip", "set", "dns", f"name={iface}", "static", "8.8.8.8"],
                        ["netsh", "interface", "ip", "add", "dns", f"name={iface}", "8.8.4.4", "index=2"]]
        elif os_name == "Darwin":
            commands = [["sudo", "networksetup", "-setdnsservers", "Wi-Fi", "8.8.8.8", "8.8.4.4"]]
        else:
            iface = self.get_linux_interface()
            commands = [["sudo", "nmcli", "device", "modify", iface, "ipv4.dns", "8.8.8.8 8.8.4.4"],
                        ["sudo", "systemctl", "restart", "NetworkManager"]]
        success, output_total = self.run_commands(commands)
        messagebox.showinfo("Cambiar DNS", "Completado" if success else "Hubo errores")
        self.log("Cambiar DNS", success, output_total)
        self.write_report()

    def get_current_ip(self):
        os_name = platform.system()
        if os_name == "Windows":
            success, output = self.run_command(["ipconfig"])
            if success:
                for line in output.splitlines():
                    if "IPv4" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            return parts[1].strip()
        elif os_name == "Darwin":
            iface = self.get_macos_interface()
            success, output = self.run_command(["ipconfig", "getifaddr", iface])
            if success:
                return output.strip()
        else:
            iface = self.get_linux_interface()
            success, output = self.run_command(["ip", "-4", "addr", "show", iface])
            if success:
                for line in output.splitlines():
                    line = line.strip()
                    if line.startswith("inet "):
                        return line.split()[1].split("/")[0]
        return ""

    def get_default_gateway(self):
        os_name = platform.system()
        if os_name == "Windows":
            success, output = self.run_command(["ipconfig"])
            if success:
                for line in output.splitlines():
                    if "Default Gateway" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            gw = parts[1].strip()
                            if gw:
                                return gw
        elif os_name == "Darwin":
            success, output = self.run_command(["route", "-n", "get", "default"])
            if success:
                for line in output.splitlines():
                    if "gateway:" in line:
                        return line.split()[1]
        else:
            success, output = self.run_command(["ip", "route", "show", "default"])
            if success:
                parts = output.strip().split()
                if "via" in parts:
                    idx = parts.index("via")
                    return parts[idx + 1]
        return ""

    def check_gateway(self):
        gateway = self.get_default_gateway()
        if not gateway:
            self.log("Verificar gateway", False, "No se detectó la puerta de enlace")
            self.write_report()
            messagebox.showinfo("Puerta de enlace", "No se detectó la puerta de enlace")
            return False
        os_name = platform.system()
        cmd = ["ping", "-c", "1", gateway] if os_name != "Windows" else ["ping", "-n", "1", gateway]
        success, output = self.run_command(cmd)
        messagebox.showinfo("Puerta de enlace", "Respondió" if success else "Sin respuesta de la puerta de enlace")
        self.log("Verificar gateway", success, output)
        self.write_report()
        return success

    def detect_ip_conflict(self):
        ip = self.get_current_ip()
        if not ip:
            self.log("Detectar conflicto IP", False, "No se obtuvo IP actual")
            self.write_report()
            messagebox.showinfo("Conflicto IP", "No se pudo obtener la IP actual")
            return False
        os_name = platform.system()
        cmd = ["arp", "-a"] if os_name == "Windows" else ["arp", "-n"]
        success, output = self.run_command(cmd)
        conflict = False
        if success:
            if output.count(ip) > 1:
                conflict = True
        message = "Posible conflicto detectado" if conflict else "Sin conflictos"
        messagebox.showinfo("Conflicto IP", message)
        self.log("Detectar conflicto IP", not conflict, output)
        self.write_report()
        return not conflict

    def check_dhcp(self):
        ip = self.get_current_ip()
        problem = ip.startswith("169.254.") or ip == ""
        messagebox.showinfo("DHCP", "DHCP operativo" if not problem else "Problema con DHCP")
        self.log("Verificar DHCP", not problem, f"IP actual: {ip}")
        self.write_report()
        return not problem

    def check_port(self, host="8.8.8.8", port=53):
        try:
            with socket.create_connection((host, port), timeout=3):
                success = True
                output = "Conexión exitosa"
        except Exception as e:
            success = False
            output = str(e)
        messagebox.showinfo("Verificar puerto", "Conexión exitosa" if success else "El puerto parece bloqueado")
        self.log(f"Verificar puerto {port}", success, output)
        self.write_report()
        return success

    def diagnose_network(self):
        self.check_connection()
        self.check_gateway()
        self.check_dhcp()
        self.detect_ip_conflict()
        self.check_port()
        messagebox.showinfo("Diagnóstico", "Proceso completado. Revisar reporte")

    def fix_all(self):
        self.restart_adapter()
        self.renew_ip()
        self.flush_dns()
        self.change_dns()
        self.check_connection()
        messagebox.showinfo("Arreglar todo", f"Proceso completado. Revisar reporte en {self.report_path}")


def main():
    root = tk.Tk()
    app = WiFiFixer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
