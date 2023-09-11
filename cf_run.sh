#!/bin/bash

# setting up cf environment
echo "Retrieving Production Environment Variables in CF.."

export AMQP_URI=$(echo ${VCAP_SERVICES} | jq -r '.rabbitmq[0].credentials.uri')
export POSTGRES_URI=$(echo ${VCAP_SERVICES} | jq -r '.postgresql[0].credentials.uri')/devex
export REDIS_URI=$(echo ${VCAP_SERVICES} | jq -r '.redis[0].credentials.uri')

# Create dbname for PostgreSQL
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
    minconn=1,
    maxconn=10,
    dbname=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)

import os
os.environ['DATABASE_CONNECTION_POOL'] = connection_pool
"""

./run.sh $@
