import os
import psycopg2

connection_string = os.getenv('DATABASE_URL')
host = os.getenv('PGHOST')
port = os.getenv('PGPORT')
user = os.getenv('PGUSER')
password = os.getenv('PGPASSWORD')
database = os.getenv('PGDATABASE')

conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
