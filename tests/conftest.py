import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAGS = ROOT / "dags"

sys.path.insert(0, str(DAGS))