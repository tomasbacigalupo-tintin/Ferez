import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class Logger:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, action: str, data: Dict[str, Any]):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "data": data,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
