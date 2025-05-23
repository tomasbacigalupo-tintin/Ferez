import os
from pathlib import Path

from logging.logger import Logger as BaseLogger


class Logger:
    """Helper that logs each action in both text and JSON formats."""

    def __init__(self, report_path: str | os.PathLike | None = None):
        if report_path is None:
            home = os.path.expanduser("~")
            report_path = os.path.join(home, "wifi_fix_report.txt")
        self.report_path = Path(report_path)

        self._text_logger = BaseLogger(self.report_path, fmt="text")
        self._json_logger = BaseLogger(self.report_path.with_suffix(".jsonl"), fmt="json")

    def log(self, action: str, success: bool, output: str) -> None:
        data = {"success": success, "output": output}
        self._text_logger.log(action, data)
        self._json_logger.log(action, data)

    def flush(self) -> None:  # Compatibility with previous API
        pass
