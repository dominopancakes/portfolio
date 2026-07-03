from transform_poc import get_transaction_data, transform_data
from load_poc import load

df_raw = get_transaction_data()

df_orders, df_products, df_order_items = transform_data(df_raw)

load(df_orders, "orders_test")
load(df_products, "products_test")
load(df_order_items, "order_items_test")