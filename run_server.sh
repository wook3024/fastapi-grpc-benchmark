python3 backend/grpc/main.py &
uvicorn backend.rest.main:app --host 0.0.0.0 --reload --reload-exclude logs/