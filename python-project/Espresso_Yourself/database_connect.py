import psycopg2
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from database_instructions import *
import json 

# Load environment variables from .env file
load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")


def create_orders_table_sql():
    return """
    CREATE TABLE IF NOT EXISTS orders (
        id UUID PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        location VARCHAR(100) NOT NULL,
        items_ordered TEXT NOT NULL,
        total_amount NUMERIC(10,2) NOT NULL,
        payment_method VARCHAR(20) NOT NULL
    );
    """

def load_orders_from_json(cursor, json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    insert_sql = """
        INSERT INTO orders (id, timestamp, location, items_ordered, total_amount, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """

    values = []
    for order_data in data.get("orders", []):
        order_id = order_data.get("order_id")
        timestamp = order_data.get("timestamp")
        if timestamp:
            timestamp = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")

        total_amount = float(order_data.get("total_amount", 0))
        values.append(
            (
                order_id,
                timestamp,
                order_data.get("location"),
                order_data.get("items_ordered", ""),
                total_amount,
                order_data.get("payment_method"),
            )
        )

    cursor.executemany(insert_sql, values)
    print(f"Loaded {len(values)} orders from {json_path}.")

def load_products_from_json(cursor, json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    insert_sql = """
        INSERT INTO product (product_id, product_name, product_price)
        VALUES (%s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING;
    """

    values = []
    for product in data.get("products", []):
        values.append(
            (
                product.get("product_id"),
                product.get("product_name"),
                product.get("price"),
            )
        )

    cursor.executemany(insert_sql, values)
    print(f"Loaded {len(values)} products from {json_path}.")


def create_database_tables():
    try:

        ### SETUP THE DATABASE CONNECTION
        print('Opening connection...')
        conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'
        # Establish a database connection
        with psycopg2.connect(conn_string) as connection:

            print('Opening cursor...')
            cursor = connection.cursor()

    # ============================================
    #                CREATE TABLES

            print('Creating tables...')

            # Create only the orders table
            cursor.execute("DROP TABLE IF EXISTS orders;")
            print('Creating Orders table...')
            cursor.execute(create_orders_table_sql())
            print('Orders table created successfully.')

            #Load the order table function thats above
            order_json_path = os.path.join(os.path.dirname(__file__), "leeds_shop_orders.json")
            load_orders_from_json(cursor, order_json_path)
            
            # Create the branch table
            cursor.execute("DROP TABLE IF EXISTS branch;")
            print('Creating Branch table...')
            create_branch_table_sql = create_branch_table()
            cursor.execute(create_branch_table_sql)
            print('Branch table created successfully.')

            # Create the product table
            cursor.execute("DROP TABLE IF EXISTS product;")
            print('Creating Product table...')
            create_product_table_sql = create_product_table()
            cursor.execute(create_product_table_sql)
            print('Product table created successfully.')

            order_json_path = os.path.join(os.path.dirname(__file__), "leeds_shop_orders.json")
            load_products_from_json(cursor, order_json_path)
            
            # Create the customer_order table
            cursor.execute("DROP TABLE IF EXISTS customer_order;")
            print('Creating Customer_Order table...')
            create_customer_order_table_sql = create_customer_order_table()
            cursor.execute(create_customer_order_table_sql)
            print('Customer_Order table created successfully.')


            #create the order_item table 
            cursor.execute("DROP TABLE IF EXISTS order_item;")
            print('Creating Order_Item table...')
            create_order_item_table_sql = create_order_item_table()
            cursor.execute(create_order_item_table_sql)
            print('Order_Item table created successfully.')


    except Exception as e:
        print(f"An error occurred: {e}")

create_database_tables()