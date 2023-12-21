import json
from pathlib import Path

from supabase import Client, create_client

secrets_path = Path(__file__).absolute().parents[1] / "secrets.json"
secrets = json.loads(secrets_path.read_bytes())
url: str = secrets.get("SUPABASE_URL")
key: str = secrets.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
