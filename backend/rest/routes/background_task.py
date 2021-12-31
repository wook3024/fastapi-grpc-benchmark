import json
import time
import base64

from os import environ
from typing import List
from fastapi import UploadFile, File, Body, APIRouter
from pathlib import Path, PurePath
from datetime import datetime
from celery.result import AsyncResult
from alive_progress import alive_bar
from multiprocessing import Process
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

from .. import schemas
from ...worker import (
    save_image_task,
    default_multiprocessing_task,
    ray_multiprocessing_task,
    celery_multiprocessing_task,
)

router = APIRouter()
save_image_dir_path = Path(
    environ.get("BASE_LOG_PATH", "/tmp"),
    environ.get("LOG_FOLDER_NAME", "logs"),
    environ.get("RECORD_DATE", datetime.now().strftime("%Y-%m-%d")),
    environ.get("IMAGE_FOLDER_NAME", "images"),
)


@router.post("", status_code=201, response_model=schemas.Id)
async def run_task(
    delay: int = Body(1), file: UploadFile = File(...)
) -> ORJSONResponse:
    contents = await file.read()
    encoded_contents = jsonable_encoder(base64.b64encode(contents))
    save_image_name = "{fn}.png".format(fn=PurePath(file.filename).stem)
    save_image_path = save_image_dir_path / save_image_name
    task = save_image_task.delay(encoded_contents, save_image_path.as_posix(), delay)
    return ORJSONResponse(content={"id": task.id}, status_code=201)


@router.get("", status_code=200, response_model=schemas.TaskResult)
async def get_status(id: str) -> ORJSONResponse:
    task_result = AsyncResult(id)
    result = {
        "id": task_result.id,
        "state": task_result.state,
        "result": task_result.result,
    }
    return ORJSONResponse(content=result, status_code=200)


@router.post("/multiple", status_code=200)
async def run_multiple_task(
    delay: int = Body(1),
    files: List[UploadFile] = File(...),
) -> ORJSONResponse:
    results = {}
    with alive_bar(len(files)) as bar:
        for file in files:
            response = await run_task(delay=delay, file=file)
            body = json.loads(response.body)
            assert "id" in body  # Request failed.
            results[PurePath(file.filename).stem] = body
            bar()
    return ORJSONResponse(content=results, status_code=200)


@router.post("/comparison", status_code=201)
async def comparison_method(
    count: int = Body(10),
    delay: int = Body(1),
    method_list: List[str] = Body(["ray", "multiprocessing", "celery"]),
    file: UploadFile = File(...),
) -> ORJSONResponse:
    contents = await file.read()
    encoded_contents = jsonable_encoder(base64.b64encode(contents))
    save_image_name = "{fn}.png".format(fn=PurePath(file.filename).stem)
    save_image_path = save_image_dir_path / save_image_name
    result = {}
    for method in method_list[0].split(","):
        with alive_bar(count, title=method) as bar:
            start_time = time.time()
            for _ in range(count):
                if method == "multiprocessing":
                    p = Process(
                        target=default_multiprocessing_task,
                        args=(encoded_contents, save_image_path.as_posix(), delay),
                    )
                    p.start()
                if method == "ray":
                    ray_multiprocessing_task.remote(
                        encoded_contents, save_image_path.as_posix(), delay
                    )
                if method == "celery":
                    celery_multiprocessing_task.delay(
                        encoded_contents, save_image_path.as_posix(), delay
                    )
                bar()
            end_time = time.time()
            result[method] = "{}s".format(round(end_time - start_time, 3))
    return ORJSONResponse(content=result, status_code=201)
