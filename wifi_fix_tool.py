import os
import platform
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class WiFiFixer:
    def __init__(self, root):
        self.root = root
        root.title("WiFi Fixer")
        root.geometry("400x350")
        self.status_var = tk.StringVar()
        self.status_var.set("Estado de conexión: desconocido")

        tk.Label(root, textvariable=self.status_var, font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Verificar conexión", command=self.check_connection).pack(pady=5)
        tk.Button(root, text="Reiniciar adaptador", command=self.restart_adapter).pack(pady=5)
        tk.Button(root, text="Renovar IP", command=self.renew_ip).pack(pady=5)
        tk.Button(root, text="Limpiar DNS", command=self.flush_dns).pack(pady=5)
        tk.Button(root, text="Cambiar DNS", command=self.change_dns).pack(pady=5)
        tk.Button(root, text="Arreglar todo", command=self.fix_all, bg="lightgreen").pack(pady=10)

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

    def log(self, action, success, output):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{now} - {action}: {'OK' if success else 'ERROR'}\n{output}\n"
        self.report.append(entry)

    def write_report(self):
        home = os.path.expanduser("~")
        path = os.path.join(home, "wifi_fix_report.txt")
        with open(path, "a", encoding='utf-8') as f:
            for line in self.report:
                f.write(line)
            f.write("\n")
        self.report = []

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
        success = True
        output_total = ""
        for cmd in commands:
            ok, out = self.run_command(cmd)
            success = success and ok
            output_total += out
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
        success = True
        output_total = ""
        for cmd in commands:
            ok, out = self.run_command(cmd)
            success = success and ok
            output_total += out
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
        success = True
        output_total = ""
        for cmd in commands:
            ok, out = self.run_command(cmd)
            success = success and ok
            output_total += out
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
        success = True
        output_total = ""
        for cmd in commands:
            ok, out = self.run_command(cmd)
            success = success and ok
            output_total += out
        messagebox.showinfo("Cambiar DNS", "Completado" if success else "Hubo errores")
        self.log("Cambiar DNS", success, output_total)
        self.write_report()

    def fix_all(self):
        self.restart_adapter()
        self.renew_ip()
        self.flush_dns()
        self.change_dns()
        self.check_connection()
        messagebox.showinfo("Arreglar todo", "Proceso completado")


def main():
    root = tk.Tk()
    app = WiFiFixer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
