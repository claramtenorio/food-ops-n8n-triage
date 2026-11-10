import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
WORKFLOWS_DIR = ROOT_DIR / "workflows"
ASSETS_DIR = ROOT_DIR / "assets"

DATA_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

TICKETS_CSV_PATH = DATA_DIR / "sample_support_tickets.csv"
TRIAGED_CSV_PATH = DATA_DIR / "triaged_support_tickets.csv"
SHIFT_REPORT_MD_PATH = DATA_DIR / "shift_operations_report.md"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")