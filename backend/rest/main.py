import time
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from .routes import index, upload, background_task


app = FastAPI(
    title="Tasks queue with FastAPI and Celery", default_response_class=ORJSONResponse
)
app.include_router(router=index.router, tags=["Index"])
app.include_router(router=upload.router, tags=["Upload"], prefix="/upload")
app.include_router(
    router=background_task.router, tags=["Background task"], prefix="/background_task"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print("{0} process time: {1:.8f}s".format(call_next.__name__, process_time))
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, log_level="info")
