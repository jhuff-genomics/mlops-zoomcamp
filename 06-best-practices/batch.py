import sys
import pickle
import pandas as pd
import os


def read_data(filename, storage_options=None):
    df = pd.read_parquet(filename, storage_options=storage_options)

    return df


def prepare_data(df, categorical):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


def main(year, month):

    #input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_file='s3://bucket/file.parquet'
    output_file = f'yellow_tripdata_{year:04d}-{month:02d}.parquet'
    
    categorical=['PULocationID', 'DOLocationID']

    default_s3_pattern = 'http://localhost:4566'
    s3_pattern = os.getenv('S3_ENDPOINT_URL', default_s3_pattern)

    storage_options = {
        'client_kwargs': {
            'endpoint_url': s3_pattern
        }
    }

    df = prepare_data(read_data(input_file, storage_options), categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())
    print('predicted sum duration:', y_pred.sum())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    df_result.to_parquet(output_file, engine='pyarrow', index=False)

    
if __name__ == "__main__":
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2023
    month = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    main(year, month)
