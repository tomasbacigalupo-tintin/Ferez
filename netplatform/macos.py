import subprocess


def run_networksetup(args):
    return subprocess.run(["networksetup", *args], capture_output=True, text=True)


def get_interfaces() -> list[str]:
    result = run_networksetup(["-listallhardwareports"])
    interfaces = []
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            if line.startswith("Device: "):
                interfaces.append(line.split()[1])
    return interfaces
