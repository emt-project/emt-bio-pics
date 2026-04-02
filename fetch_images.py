import requests
import os
import glob
from PIL import Image

out_dir = "bio-pics"
os.makedirs(out_dir, exist_ok=True)
url_stub = (
    "https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/{}&width={}"  # noqa: E501
)
img_list = glob.glob("bio-pics/*.*")

data = requests.get(
    "https://raw.githubusercontent.com/emt-project/emt-entities/main/json_dumps/persons.json"  # noqa: E501
).json()


headers = {
    'User-Agent': f'EMT/1.0 ({os.environ.get("PROJECT_URL")}; {os.environ.get("CONTACT_EMAIL")})'
}

for key, value in data.items():
    emt_id = value["emt_id"]
    img_name = value["img_name"]
    if img_name:
        image_url = url_stub.format(img_name, "250")
        img_format = img_name.split(".")[-1]
        img_name = os.path.join(out_dir, f"{emt_id}.{img_format}".lower())
        check_name = img_name.replace(img_name.split(".")[-1], "jpg")
        if check_name in img_list:
            continue
        print(
            f"{image_url} does not exist, downloading as {img_name}"
        )
        try:
            r = requests.get(image_url, headers=headers)
            r.raise_for_status()
            img_data = r.content
            with open(img_name, "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"Failed to download {image_url}: {e}")
            continue
        
        try:
            if not img_name.endswith(".jpg"):
                im = Image.open(img_name)
                rgb_im = im.convert("RGB")
                new_name = os.path.splitext(img_name)[0] + ".jpg"
                rgb_im.save(new_name)
        except Exception as e:
            print(f"Failed to convert {img_name}: {e}")
            continue

for x in sorted(glob.glob(f"{out_dir}/*.*")):
    if x.endswith(".jpg"):
        pass
    else:
        os.remove(x)
