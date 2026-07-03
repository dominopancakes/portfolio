import pandas as pd
import uuid
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# def get_transaction_data():
#     """
#     Temporary extract function.
#     Replace with actual extract module later.
#     """
#     return pd.read_csv(
#         "./data/leeds_28-03-2025_09-00-00_1.csv",
#         header=None,
#         names=["payment_time", "city", "customer_name", "basket", "total_price", "payment_method", "card_number"]
#         )

# Add timestamp formatting .to_datetime() (change sql script datar type)

def generate_uuid():
    
    return str(uuid.uuid4())


def add_uuid(df, id_column_name):
    """
    Function for adding a UUID column to an existing df 
    """

    df[id_column_name] = [generate_uuid() for i in range(len(df))]

    return df


def remove_duplicates(df):
    '''
    Function to remove duplicate rows from our data
    '''
    
    return df.drop_duplicates()


def drop_sensitive_data(df):

    return df.drop(columns=["customer_name", "card_number"])




def normalise_to_1nf(df: pd.DataFrame):

    # atomise the df

    # create a new column named 'items', turn values in 'basket' into a list and populate the 'items' column with these lists
    df_1nf = df.assign(items=df['basket'].str.split(','))

    # turn each element of a list in a cell into seperate rows
    df_1nf = df_1nf.explode('items')

    # clean whitespaces
    df_1nf['items'] = df_1nf['items'].str.strip()

    # split items into product_name and product_price
    df_1nf[['product_name', 'product_price']] = df_1nf["items"].str.rsplit(' - ', n=1, expand=True)

    # drop unnecessary columns
    df_1nf = df_1nf.drop(columns=['basket', 'items'])

    return df_1nf


def create_orders_table(df: pd.DataFrame):
    # keep only relevant columns from the 1NF table and remove duplicates
    df_orders = df[['order_id', 'payment_time', 'city', 'total_price', 'payment_method']].drop_duplicates()

    return df_orders


def create_products_table(df: pd.DataFrame):
    # keep only relevant columns from the 1NF table and remove duplicates
    df_products = df[['product_name', 'product_price']].drop_duplicates()

    # add product ID
    df_products = add_uuid(df_products, 'product_id')

    return df_products


def create_order_items_table(df_1nf: pd.DataFrame, df_products: pd.DataFrame):
    # create table where order IDs are related to the product IDs and add a quantity column to avoid duplicates
    df_order_items = df_1nf.groupby(['order_id', 'product_name', 'product_price'], sort=False).size().reset_index(name='quantity')

    # merge with products table to get the product IDs
    df_order_items = df_order_items.merge(df_products[['product_id', 'product_name', 'product_price']], on=['product_name', 'product_price'])

    # keep relevant columns only
    df_order_items = df_order_items[['order_id', 'product_id', 'quantity']]

    return df_order_items


def transform_data(df):
    
    try:
        # remove duplicate rows
        df = remove_duplicates(df)

        LOGGER.info(f'transform_data: removed duplicates')

        # generate GUIDs for the orders
        df = add_uuid(df, "order_id")

        LOGGER.info(f'transform_data: added order id')

        # drop customer name and card number columns
        df = drop_sensitive_data(df)

        LOGGER.info(f'transform_data: removed sensitive data')

        # normalise to 1NF
        df_1nf = normalise_to_1nf(df)

        LOGGER.info(f'transform_data: normalised to 1NF')

        # normalise to 3NF: seperate the 1nf table into multiple tables with single dependencies

        df_orders = create_orders_table(df_1nf)
        df_products = create_products_table(df_1nf)
        df_order_items = create_order_items_table(df_1nf, df_products)

        LOGGER.info(f'transform_data: normalised to 3NF')

    except Exception as e:
        LOGGER.error(f'trasform_data failed: error={e}')
        raise e

    return df_orders, df_products, df_order_items


# test, remove later

# df = get_transaction_data()

# df_orders, df_products, df_order_items = transform_data(df)

# print(df_orders.head(10))
# print(df_products.head(10))
# print(df_order_items.head(10))

