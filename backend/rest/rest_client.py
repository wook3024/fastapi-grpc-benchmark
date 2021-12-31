import argparse

from httpx import Client
from pathlib import Path
from alive_progress import alive_bar


def run(image_path, data):
    with Client() as client:
        response = client.post(
            url="http://localhost:8000/upload/image",
            files={"file": (image_path.stem, data, "image/jpeg")},
        )
        result = response.json()
    print("url: ", result.get("url"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()

    image_path = Path("assets/images/ImagebyLuuDofromPixabay.jpg")
    with image_path.open("rb") as f:
        data = f.read()
    with alive_bar(args.count, title="Rest") as bar:
        for _ in range(args.count):
            run(image_path, data)
            bar()
