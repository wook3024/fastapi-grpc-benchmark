# gRPC vs FastAPI Benchmark

## Quickstart

### Build and start containers

```sh
docker-compose up -d --build
```

### Run grpc request

```sh
docker exec -it web bash -c "python3 backend/grpc/grpc_client.py"
```

### Run rest request

```sh
docker exec -it web bash -c "python3 backend/rest/rest_client.py"
```

## Comparison results
```
Rest |████████████████████████████████████████| 100/100 [100%] in 4.9s (20.52/s)
gRPC |████████████████████████████████████████| 100/100 [100%] in 1.0s (96.56/s)
```