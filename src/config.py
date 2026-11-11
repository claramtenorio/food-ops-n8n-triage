import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
WORKFLOWS_DIR = BASE_DIR / "workflows"
ASSETS_DIR = BASE_DIR / "assets"

TICKETS_CSV_PATH = DATA_DIR / "support_tickets.csv"
TRIAGED_CSV_PATH = DATA_DIR / "triaged_support_tickets.csv"
SHIFT_REPORT_MD_PATH = DATA_DIR / "shift_operations_report.md"

# Live Google Sheets CSV export endpoint
GOOGLE_SHEET_CSV_URL = os.getenv(
    "GOOGLE_SHEET_CSV_URL",
    "https://docs.google.com/spreadsheets/d/1hayoxZPBpbhlvGPF5tfYOp0g00YGmzjYJQOwpn5OwMQ/export?format=csv&gid=0"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")