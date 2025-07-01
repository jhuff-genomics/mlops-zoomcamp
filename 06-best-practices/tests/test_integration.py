import os
import pandas as pd
from datetime import datetime
import subprocess

import batch

S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')
INPUT_FILE_PATTERN = os.environ.get('INPUT_FILE_PATTERN')

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_save_input_parquet():
    data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    default_input_pattern = 's3://bucket/file.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)

    default_s3_pattern = 'http://localhost:4566'
    s3_pattern = os.getenv('S3_ENDPOINT_URL', default_s3_pattern)

    options = {
        'client_kwargs': {
            'endpoint_url': s3_pattern
        }
    }

    df.to_parquet(
        input_pattern,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

def test_batch_processing():
    result = subprocess.run(['python', 'batch.py'],
                            cwd='06-best-practices',
                            capture_output=True,
                            text=True)
    assert result.returncode == 0
