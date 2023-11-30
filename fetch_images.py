import requests
import os
import glob

out_dir = "bio-pics"
os.makedirs(out_dir, exist_ok=True)
url_stub = (
    "https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/{}&width={}"
)
img_list = glob.glob("./bio-pics/*.*")

data = requests.get(
    "https://raw.githubusercontent.com/emt-project/emt-entities/main/json_dumps/persons.json"
).json()


headers = {
    "User-Agent": "My User Agent 1.0",
    "From": "youremail@domain.example",  # This is another valid field
}

for key, value in data.items():
    emt_id = value["emt_id"]
    img_name = value["img_name"]
    if img_name:
        image_url = url_stub.format(img_name, "250")
        img_format = img_name.split(".")[-1]
        img_name = os.path.join(out_dir, f"{emt_id}.{img_format}")
        if img_name in img_list:
            continue
        r = requests.get(image_url, headers=headers)
        img_data = r.content
        print(r.status_code)
        with open(img_name, "wb") as f:
            f.write(img_data)
