import ray
import time
import psutil

from os import environ
from celery import Celery

from .utils.save import save_image_data


num_logical_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_logical_cpus)


celery_conf = {
    "broker": environ.get(
        "CELERY_BROKER_URL",
        "redis://localhost:6379",
    ),
    "backend": environ.get(
        "CELERY_RESULT_BACKEND",
        "elasticsearch://elasticsearch:9200/background_task/result",
    ),
}
celery = Celery(
    celery_conf=__name__,
    broker=celery_conf.get("broker"),
    backend=celery_conf.get("backend"),
)


@celery.task(name="save image")
def save_image_task(contents: str, save_image_path: str, delay: int = 0) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return {"save_path": save_image_path, "image_shape": image_shape, "delay": delay}


def default_multiprocessing_task(
    contents: str, save_image_path: str, delay: int = 0
) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return {"save_path": save_image_path, "image_shape": image_shape, "delay": delay}


@celery.task
def celery_multiprocessing_task(
    contents: str, save_image_path: str, delay: int = 0
) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return {"save_path": save_image_path, "image_shape": image_shape, "delay": delay}


@ray.remote
def ray_multiprocessing_task(
    contents: str, save_image_path: str, delay: int = 0
) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return {"save_path": save_image_path, "image_shape": image_shape, "delay": delay}
