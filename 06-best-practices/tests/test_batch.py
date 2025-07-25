from datetime import datetime
import pandas as pd

import batch


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
 
    df = pd.DataFrame(data, columns=columns)
    df_prepared = batch.prepare_data(df, ['PULocationID', 'DOLocationID'])

    data_expected = [
    (str(int(-1)), str(int(-1)), datetime(2023, 1, 1, 1, 1, 0), datetime(2023, 1, 1, 1, 10, 0), (9.0)),
    (str(int(1)), str(int(1)), datetime(2023, 1, 1, 1, 2, 0), datetime(2023, 1, 1, 1, 10, 0), (8.0))
    ]

    columns_expected = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
    df_expected = pd.DataFrame(data_expected, columns=columns_expected)

    assert df_prepared.shape == (2, 5)
    assert df_prepared.equals(df_expected)
