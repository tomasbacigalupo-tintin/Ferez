import platform
import subprocess


def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = result.returncode == 0
        output = result.stdout + result.stderr
    except Exception as e:
        success = False
        output = str(e)
    return success, output


def run_commands(commands):
    success = True
    output_total = ""
    for cmd in commands:
        ok, out = run_command(cmd)
        success = success and ok
        output_total += out
    return success, output_total


# Interface detection per OS

def get_windows_interface():
    success, output = run_command(["netsh", "interface", "show", "interface"])
    if success:
        for line in output.splitlines():
            if "Connected" in line:
                parts = line.split()
                if parts:
                    return parts[-1]
    return "Wi-Fi"


def get_linux_interface():
    success, output = run_command(["nmcli", "-t", "-f", "DEVICE,STATE", "device"])
    if success:
        for line in output.splitlines():
            if line.endswith(":connected"):
                return line.split(":")[0]
    return "wlan0"


def get_macos_interface():
    return "en0"


def get_interface():
    os_name = platform.system()
    if os_name == "Windows":
        return get_windows_interface()
    if os_name == "Darwin":
        return get_macos_interface()
    return get_linux_interface()
