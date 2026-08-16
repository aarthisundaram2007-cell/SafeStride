from pathlib import Path
from urllib.parse import urlparse
import os
import socket
from dotenv import load_dotenv
from supabase import create_client

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

url_loaded = bool(SUPABASE_URL)
key_loaded = bool(SUPABASE_KEY)
hostname = urlparse(SUPABASE_URL).hostname if SUPABASE_URL else "unknown"

print(
    f"Supabase diagnostics: URL loaded={url_loaded}, key loaded={key_loaded}, hostname={hostname}"
)

if not SUPABASE_URL:
    raise SystemExit(f"❌ SUPABASE_URL was not loaded from {ENV_FILE}")

if not SUPABASE_KEY:
    raise SystemExit(f"❌ SUPABASE_KEY was not loaded from {ENV_FILE}")

try:
    socket.gethostbyname(hostname)
except socket.gaierror as dns_error:
    print("❌ DNS resolution failed for the Supabase hostname.")
    print(f"Local DNS/network problem: {dns_error}")
    print("This points to local hostname resolution rather than missing Supabase credentials.")
    raise SystemExit(1)

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.schema("public").table("users").select("*").limit(1).execute()

    print("✅ Supabase connection successful!")
    print("Sample data:", response.data)
except Exception as e:
    print("❌ Supabase connection failed:")
    print(e)