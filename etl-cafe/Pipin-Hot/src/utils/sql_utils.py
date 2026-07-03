from utils import db_utils
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def create_db_tables(connection, cursor):
    LOGGER.info('create_db_tables: started')
    
    try:
        LOGGER.info('create_db_tables: creating orders, products, and order_items tables')
        # IDs are stored as string instead of UUID as currenct redshift version doesn't support UUID
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS orders (
                order_id VARCHAR(36) PRIMARY KEY,
                payment_time VARCHAR(16),
                city VARCHAR(58),
                total_price DECIMAL(10,2),
                payment_method  VARCHAR(5)
            );

            CREATE TABLE IF NOT EXISTS products (
                product_id VARCHAR(36) PRIMARY KEY,
                product_name VARCHAR(80),
                product_price DECIMAL(4,2)
            );

            CREATE TABLE IF NOT EXISTS order_items (
                order_id VARCHAR(36),
                product_id VARCHAR(36),
                quantity SMALLINT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
            '''
        )

        LOGGER.info('create_db_tables: committing')
        connection.commit()

        LOGGER.info('create_db_tables: done')

    except Exception as e:
        LOGGER.error(f'create_db_tables: failed to run sql: {e}')
        raise e
    
