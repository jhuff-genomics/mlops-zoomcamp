
# Lock dependencies and create virtual environment
```bash
uv pip compile requirements.in -o requirements.txt
uv venv 06-best-practices
```

## Activate venv and install dependencies
```bash
source 06-best-practices/bin/activate
uv pip sync requirements.txt
```

## Run the batch script
```bash
python batch.py 2023 03
```

## Add pytest
```bash
uv pip install pytest
```

## Add localstack
```bash
uv pip install localstack
```

## Docker Compose S3 localstack service
```bash
docker-compose up -d s3
```

## Check localstack S3 buckets
```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

## Make localstack S3 bucket
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://bucket
```

## Run integration tests
```bash
pytest tests/test_integration.py
aws --endpoint-url=$S3_ENDPOINT_URL s3 ls s3://bucket/
```
