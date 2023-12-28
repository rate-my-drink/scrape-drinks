from PIL import Image
import requests
import io


def load_img_from_url(image_url: str) -> bytes:
    img_data = requests.get(image_url).content
    image = Image.open(io.BytesIO(img_data))

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="WEBP")
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


if __name__ == "__main__":
    img_bytes_arr = load_img_from_url(
        image_url="https://www.simonlevelt.nl/media/image/de/4b/30/3fdcc7c0-d955-46ff-b4d3-bf852dde2bd6_600x600.png"
    )
    print(len(img_bytes_arr))
    print(img_bytes_arr[:100])
