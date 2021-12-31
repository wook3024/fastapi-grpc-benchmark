ARG PYTHON_VERSION=3.9

FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION}

LABEL maintainer="Shinuk Yi<wook3024@gmail.com>"

RUN groupadd -r appuser -g 1000 && \
    useradd -u 1000 -r -g appuser -s /sbin/nologin -c "Docker image user" appuser

RUN apt-get update && apt-get install -y libgl1-mesa-glx

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /workspace

COPY . /workspace
WORKDIR /workspace

RUN pip install --upgrade pip && \
    pip install pip-tools
RUN pip-sync requirements/prod.txt requirements/dev.txt

RUN python3 -m grpc_tools.protoc -Ibackend/grpc --python_out=backend/grpc/protos/ --grpc_python_out=backend/grpc/protos backend/grpc/protos/upload.proto

USER appuser

RUN mkdir /tmp/logs

ENTRYPOINT [ "sh", "run_server.sh"]
