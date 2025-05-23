import os
from datetime import datetime

class Logger:
    def __init__(self, report_path=None):
        if report_path is None:
            home = os.path.expanduser("~")
            report_path = os.path.join(home, "wifi_fix_report.txt")
        self.report_path = report_path
        self.entries = []

    def log(self, action: str, success: bool, output: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{now} - {action}: {'OK' if success else 'ERROR'}\n{output}\n"
        self.entries.append(entry)

    def flush(self) -> None:
        if not self.entries:
            return
        with open(self.report_path, "a", encoding="utf-8") as f:
            for line in self.entries:
                f.write(line)
            f.write("\n")
        self.entries = []
