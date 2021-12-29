# Tasks queue with FastAPI and Celery

How to handle background processes with FastAPI, Celery, Redis, RabbitMQ.

## Quickstart

### Build and start containers:

```sh
docker-compose up --build
```

Api docs: [http://localhost:8000/docs](http://localhost:8000/docs)
Flower dashboard: [http://localhost:5555](http://localhost:5555)

### Create task

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/background_task' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'delay=1' \
  -F 'file=@assets/fluentd-icon-color.png;type=image/png'
```

### Check task status

```sh
curl -X 'GET' \
  'http://0.0.0.0:8000/background_task/${id}' \
  -H 'accept: application/json'
```

### Multiple request
```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/background_task/multiple' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'delay=1' \
  -F 'files=@fluentd-icon-color.png;type=image/png' \
  -F 'files=@fluentd-icon-color.png;type=image/png' \
  -F 'files=@fluentd-icon-color.png;type=image/png'
```
### Comparison method
```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/background_task/comparison' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'count=10' \
  -F 'delay=1' \
  -F 'method_list=ray,default,celery' \
  -F 'file=@fluentd-icon-color.png;type=image/png'
```
