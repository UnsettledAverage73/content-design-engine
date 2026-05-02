import json
from pathlib import Path
from typing import List, Dict, Any

class SelectionLogger:
    def __init__(self, output_dir: Path):
        self.log_path = output_dir / "log.json"
        self.entries = []

    def log_evaluation(self, file_path: Path, score: Any, selected: bool):
        self.entries.append({
            "file": str(file_path.name),
            "technical_score": score.technical_score,
            "marketing_score": score.marketing_score,
            "justification": score.justification,
            "selected": selected
        })

    def save(self):
        with open(self.log_path, "w") as f:
            json.dump(self.entries, f, indent=4)
