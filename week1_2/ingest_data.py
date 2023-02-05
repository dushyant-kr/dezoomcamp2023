import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import requests

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'
    # os.system(f"wget {url} -O {csv_name}")
    # temp = wget.download(f"{url}, out = {csv_name}")
    print(url)
    req=requests.get(url)
    csv_file=open(csv_name,'wb')
    csv_file.write(req.content)
    csv_file.close()

    # download the csv

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # engine.connect()

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    print(df.shape)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    # df.head(n=0).to_sql(name=table_name, con=engine)

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)

        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk... took %.3f seconds' %(t_end-t_start))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv')

    args = parser.parse_args()

    main(args)
