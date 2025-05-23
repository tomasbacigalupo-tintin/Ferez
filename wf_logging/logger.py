import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class Logger:
    """Simple logger that can output entries in JSON or plain text format."""

    def __init__(self, path: Path | str, *, fmt: str = "json"):
        """Create a new logger.

        Parameters
        ----------
        path:
            Destination file where logs are written.
        fmt:
            Either ``"json"`` or ``"text"`` to select the output format.
        """

        self.path = Path(path)
        self.format = fmt
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, action: str, data: Dict[str, Any]):
        """Append an entry to the log file."""

        timestamp = datetime.utcnow().isoformat()
        if self.format == "text":
            line = f"{timestamp} - {action}: {data}\n"
            with self.path.open("a", encoding="utf-8") as f:
                f.write(line)
            return

        entry = {
            "timestamp": timestamp,
            "action": action,
            "data": data,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
