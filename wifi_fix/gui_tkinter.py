import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

from .core import WiFiFixCore


class WiFiFixerApp:
    def __init__(self, root):
        self.core = WiFiFixCore()
        self.root = root
        root.title("WiFi Fixer")
        root.geometry("420x480")
        self.status_var = tk.StringVar()
        self.status_var.set("Estado de conexión: desconocido")

        tk.Label(root, textvariable=self.status_var, font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Verificar conexión", command=self.check_connection).pack(pady=5)
        tk.Button(root, text="Reiniciar adaptador", command=self.restart_adapter).pack(pady=5)
        tk.Button(root, text="Renovar IP", command=self.renew_ip).pack(pady=5)
        tk.Button(root, text="Limpiar DNS", command=self.flush_dns).pack(pady=5)
        tk.Button(root, text="Cambiar DNS", command=self.change_dns).pack(pady=5)
        tk.Button(root, text="Diagnóstico avanzado", command=self.diagnose_network).pack(pady=5)
        tk.Button(root, text="Arreglar todo", command=self.fix_all, bg="lightgreen").pack(pady=10)
        tk.Button(root, text="Abrir reporte", command=self.open_report).pack(pady=5)

    def open_report(self):
        path = self.core.logger.report_path
        try:
            if not os.path.exists(path):
                messagebox.showinfo("Abrir reporte", "El archivo de reporte aún no existe")
                return
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Abrir reporte", str(e))

    def check_connection(self):
        success = self.core.check_connection()
        self.status_var.set("Estado de conexión: Conectado" if success else "Estado de conexión: Sin conexión")
        messagebox.showinfo("Verificar conexión", "Conectado a internet" if success else "Sin conexión a internet")

    def restart_adapter(self):
        success = self.core.restart_adapter()
        messagebox.showinfo("Reiniciar adaptador", "Completado" if success else "Hubo errores")

    def renew_ip(self):
        success = self.core.renew_ip()
        messagebox.showinfo("Renovar IP", "Completado" if success else "Hubo errores")

    def flush_dns(self):
        success = self.core.flush_dns()
        messagebox.showinfo("Limpiar DNS", "Completado" if success else "Hubo errores")

    def change_dns(self):
        success = self.core.change_dns()
        messagebox.showinfo("Cambiar DNS", "Completado" if success else "Hubo errores")

    def diagnose_network(self):
        self.core.diagnose_network()
        messagebox.showinfo("Diagnóstico", "Proceso completado. Revisar reporte")

    def fix_all(self):
        self.core.fix_all()
        messagebox.showinfo("Arreglar todo", f"Proceso completado. Revisar reporte en {self.core.logger.report_path}")


def main():
    root = tk.Tk()
    app = WiFiFixerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
