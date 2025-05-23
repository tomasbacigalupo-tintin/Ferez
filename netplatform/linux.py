import subprocess


def run_nmcli(args):
    return subprocess.run(["nmcli", *args], capture_output=True, text=True)


def get_interfaces() -> list[str]:
    result = run_nmcli(["-t", "-f", "DEVICE,STATE", "device"])
    interfaces = []
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            if line.endswith(":connected"):
                interfaces.append(line.split(":")[0])
    return interfaces
