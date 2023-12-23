import json
from pathlib import Path

from supabase import Client, create_client

secrets_path = Path(__file__).absolute().parents[1] / "secrets.json"
secrets = json.loads(secrets_path.read_bytes())
url: str = secrets.get("SUPABASE_URL")
key: str = secrets.get("SUPABASE_KEY")
user_name: str = secrets.get("USER_NAME_CC")
password: str = secrets.get("PASSWORD_CC")

# class SupabaseCC:
supabase: Client = create_client(url, key)

user_data = supabase.auth.sign_in_with_password(
    {"email": user_name, "password": password}
)
session = user_data.session

supabase.postgrest.auth(
    # verified that this was real
    token=session.access_token
)

# Upload drink
res = (
    supabase.table("drinks")
    .insert(
        {
            "name": "test",
            "description": "",
            "producer": 3,
            "user_id": user_data.user.id,
            "image": None,
        }
    )
    .execute()
)

# Upload image

image_path = Path(r"/home/tom/Pictures/default_coffee.webp")
image_bytes = image_path.read_bytes()

# I had to do this in order to get the storage to make the request correctly.
storageSessionDict = supabase.storage.session.__dict__
storageSessionDict["_headers"]["authorization"] = (
    "Bearer " + supabase.auth.get_session().__dict__["access_token"]
)

supabase.storage.from_("coffee-images").upload(
    file=image_bytes,
    path=r"public/drinks/test/coffee.webp",
    file_options={"content-type": "image/webp"},
)
