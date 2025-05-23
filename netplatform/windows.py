import subprocess


def run_netsh(args):
    return subprocess.run(["netsh", *args], capture_output=True, text=True)


def run_ipconfig(args=None):
    cmd = ["ipconfig"]
    if args:
        cmd.extend(args)
    return subprocess.run(cmd, capture_output=True, text=True)


def get_interfaces() -> list[str]:
    result = run_netsh(["interface", "show", "interface"])
    interfaces = []
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            if "Connected" in line:
                parts = line.split()
                if parts:
                    interfaces.append(parts[-1])
    return interfaces
