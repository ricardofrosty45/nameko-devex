#!/bin/bash

# Check if rabbit is up and running before starting the service.
until nc -z localhost 5672; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

# Check if redis is up and running before starting the service.
until nc -z localhost 6379; do
    echo "$(date) - waiting for redis..."
    sleep 2
done

# Check if postgres is up and running before starting the service.
until nc -z localhost 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 2
done

# Create the database if it doesn't exist and set up the connection pool
python -c """
import psycopg2 as db
from psycopg2 import pool
from urllib.parse import urlparse

result = urlparse('${POSTGRES_URI}')
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

connection_pool = pool.SimpleConnectionPool(
    minconn=1,  # Minimum number of connections
    maxconn=10,  # Maximum number of connections
    user='postgres',
    password='postgres',
    host=hostname,
    port=port,
    dbname=database
)

try:
    con = connection_pool.getconn()
    con.autocommit = True
    cursor = con.cursor()
    cursor.execute('CREATE DATABASE orders')
    connection_pool.putconn(con)
except Exception as e:
    print('Error creating database:', str(e))
    exit(1)
"""

# setting up local environment
export AMQP_URI=amqp://guest:guest@localhost:5672
export POSTGRES_URI=postgresql://postgres:postgres@localhost:5432/orders
export REDIS_URI=redis://localhost:6379/dev

./run.sh $@

