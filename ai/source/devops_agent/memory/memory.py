# memory/memory.py
import json
from pathlib import Path

FILE = Path("memory/history.json")

def save_report(report):
  history = load_history()
  history.append(report)
  FILE.write_text(json.dumps(history, indent=2))

def load_history():
  if not FILE.exists():
    return []
  return json.loads(FILE.read_text())
