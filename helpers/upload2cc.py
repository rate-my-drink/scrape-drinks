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

    def upload_image(self, image_bytes: bytes, folder_path: str):
        image_path = self._upload_img_bytes(image_bytes, folder_path)
        public_url = self._get_image_url(image_path)
        table_res = self._update_image_table(public_url)
        return table_res

    def _get_drink(self, href) -> int or None:
        res = self.client.from_("drinks").select("id").eq("href", href).execute()
        if res.data:
            return res.data[0]["id"]
        return None

    def upload_drink(
        self,
        name: str,
        producer_id: int,
        href: str,
        description: str = "",
        image_bytes: bytes = None,
    ):
        if image_bytes:
            image_id = self.upload_image(image_bytes, f"drinks/{producer_id}")
        else:
            image_id = None

        drink_id = self._get_drink(href)
        if drink_id:
            res = (
                self.client.from_("drinks")
                .update(
                    {
                        "name": name,
                        "description": description,
                        "producer": producer_id,
                        "user_id": self.user_id,
                        "image": image_id,
                    }
                )
                .eq("id", drink_id)
                .execute()
            )
        else:
            res = (
                self.client.from_("drinks")
                .insert(
                    {
                        "name": name,
                        "description": description,
                        "producer": producer_id,
                        "href": href,
                        "user_id": self.user_id,
                        "image": image_id,
                    }
                )
                .execute()
            )
        return res


if __name__ == "__main__":
    image_path = Path(r"/home/tom/Pictures/default_coffee.webp")
    image_bytes = image_path.read_bytes()
    href = "https://caffeinecritics.com/"
    client_cc = SupabaseCC()

    res = client_cc.upload_drink(
        "test",
        3,
        description="hello from python",
        href=href,
        image_bytes=image_bytes,
    )

    print(res)
    res2 = client_cc.upload_drink(
        "test 2",
        3,
        description="hello from python, again",
        href=href,
        image_bytes=image_bytes,
    )
    print(res2)
