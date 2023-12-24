import json
from pathlib import Path
from uuid import uuid4

from supabase import Client, create_client

secrets_path = Path(__file__).absolute().parents[1] / "secrets.json"
secrets = json.loads(secrets_path.read_bytes())
url: str = secrets.get("SUPABASE_URL")
key: str = secrets.get("SUPABASE_KEY")
user_name: str = secrets.get("USER_NAME_CC")
password: str = secrets.get("PASSWORD_CC")


class SupabaseCC:
    client: Client
    bucket_name: str = "coffee-images"
    user_id: str

    def __init__(self):
        # Authentications
        self.client: Client = create_client(url, key)

        user_data = self.client.auth.sign_in_with_password(
            {"email": user_name, "password": password}
        )
        session = user_data.session

        self.user_id = user_data.user.id
        self.client.postgrest.auth(
            # verified that this was real
            token=session.access_token
        )
        storageSessionDict = self.client.storage.session.__dict__
        storageSessionDict["_headers"]["authorization"] = (
            "Bearer " + session.access_token
        )

    def _upload_img_bytes(self, image_bytes: bytes, folder_path: str) -> str:
        if not folder_path.endswith("/"):
            folder_path += "/"
        # Upload image
        file_response = (
            self.client.storage.from_(self.bucket_name)
            .upload(
                file=image_bytes,
                path=rf"public/{folder_path}{uuid4()}.webp",
                file_options={"content-type": "image/webp"},
            )
            .json()
        )
        image_path = file_response["Key"]
        return image_path

    def _get_image_url(self, image_path):
        public_url = (
            self.client.storage.from_(self.bucket_name)
            .get_public_url(image_path)
            .replace(f"{self.bucket_name}/{self.bucket_name}/", f"{self.bucket_name}/")
        )
        return public_url

    def _update_image_table(self, public_url) -> int:
        pass
        # Upload drink
        res = (
            self.client.table("images")
            .insert(
                {
                    "url": public_url,
                    "storage_vendor": "supabase",
                    "user": self.user_id,
                }
            )
            .execute()
        )
        return res.data[0]["id"]

    def upload_image(self, image_bytes, folder_path):
        image_path = self._upload_img_bytes(image_bytes, folder_path)
        public_url = self._get_image_url(image_path)
        table_res = self._update_image_table(public_url)
        return table_res


image_path = Path(r"/home/tom/Pictures/default_coffee.webp")
image_bytes = image_path.read_bytes()

client_cc = SupabaseCC()

image_id = client_cc.upload_image(image_bytes, "drinks/test")

print(res)
