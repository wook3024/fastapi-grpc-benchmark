import grpc
import argparse

from pathlib import Path
from alive_progress import alive_bar

import upload_pb2
import upload_pb2_grpc


def run(image_path, data):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = upload_pb2_grpc.UploadStub(channel)
        response = stub.UploadImage(
            upload_pb2.UploadImageRequest(data=data, filename=image_path.stem)
        )
    print("url: ", response.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()

    image_path = Path("assets/images/ImagebyLuuDofromPixabay.jpg")
    with image_path.open("rb") as f:
        data = f.read()
    with alive_bar(args.count, title="gRPC") as bar:
        for _ in range(args.count):
            run(image_path, data)
            bar()
