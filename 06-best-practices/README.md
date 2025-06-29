
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