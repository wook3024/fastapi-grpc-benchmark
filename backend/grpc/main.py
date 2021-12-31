import grpc

from datetime import datetime
from concurrent import futures
from threading import Thread

import upload_pb2
import upload_pb2_grpc

from backend.utils.save import save_bytes_data


class Upload(upload_pb2_grpc.UploadServicer):
    def UploadImage(self, request, context):
        current_datetime = datetime.now()
        save_url = "assets/images/{fn}_{cd}.png".format(
            fn=request.filename, cd=current_datetime
        )
        t = Thread(
            target=save_bytes_data,
            args=(
                save_url,
                request.data,
            ),
        )
        t.start()
        return upload_pb2.UploadImageReply(url=save_url)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    upload_pb2_grpc.add_UploadServicer_to_server(Upload(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
