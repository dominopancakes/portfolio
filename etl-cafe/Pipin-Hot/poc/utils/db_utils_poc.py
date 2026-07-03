import psycopg2 

#import os

# from dotenv import load_dotenv

# # LOAD ENVIRONMENT VARIABLES

# load_dotenv()

# host_name = os.environ.get("POSTGRES_HOST")
# port = os.environ.get("DB_PORT")
# database_name = os.environ.get("POSTGRES_DB")
# user_name = os.environ.get("POSTGRES_USER")
# user_password = os.environ.get("POSTGRES_PASSWORD")


# CONNECT TO DATABASE

# hardcode postgresql creds for testing

def get_connection():

    connection = psycopg2.connect(
        host='192.168.0.138',
        port='5432',
        dbname='postgres',
        user='postgres',
        password='mysecretpassword'
    )

    return connection


