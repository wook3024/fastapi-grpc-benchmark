from pathlib import PurePath
from fastapi import UploadFile, File, APIRouter
from datetime import datetime
from threading import Thread
from fastapi.responses import ORJSONResponse

from ...utils.save import save_bytes_data
from .. import schemas


router = APIRouter()


@router.post("/image", status_code=201, response_model=schemas.Url)
async def image_upload(file: UploadFile = File(...)) -> ORJSONResponse:
    data = await file.read()
    current_datetime = datetime.now()
    save_url = "assets/images/{fn}_{cd}.png".format(
        fn=PurePath(file.filename).stem, cd=current_datetime
    )
    t = Thread(
        target=save_bytes_data,
        args=(
            save_url,
            data,
        ),
    )
    t.start()
    return ORJSONResponse(content={"url": save_url}, status_code=201)
