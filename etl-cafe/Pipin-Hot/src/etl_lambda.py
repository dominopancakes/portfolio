from utils import s3_utils, db_utils, sql_utils

import extract
import transform
import load
import json
import logging
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SSM_ENV_VAR_NAME = 'SSM_PARAMETER_NAME'

def lambda_handler(event, context):
    file_path = 'NOT_SET'   # makes the exception handler compile

    try:
        bucket_name, file_path = s3_utils.get_file_info(event)

        df_raw = extract.get_data(bucket_name=bucket_name, s3_key=file_path)

        df_orders, df_products, df_order_items = transform.transform_data(df_raw)

        LOGGER.info(f'orders ({df_orders.shape[0]} rows, {df_orders.shape[1]} cols):\n{df_orders.head(3).to_string()}')
        LOGGER.info(f'products ({df_products.shape[0]} rows, {df_products.shape[1]} cols):\n{df_products.head(3).to_string()}')
        LOGGER.info(f'order_items ({df_order_items.shape[0]} rows, {df_order_items.shape[1]} cols):\n{df_order_items.head(3).to_string()}')

        ssm_param_name = os.environ.get(SSM_ENV_VAR_NAME, 'NOT_SET')
        LOGGER.info(f'lambda_handler: ssm_param_name={ssm_param_name} from ssm_env_var_name={SSM_ENV_VAR_NAME}')

        redshift_details = db_utils.get_ssm_param(ssm_param_name)

        conn, cur = db_utils.get_connection_and_cursor(redshift_details)

        sql_utils.create_db_tables(conn, cur)


        load.load(df_orders, "orders", cur=cur, conn=conn)
        load.load(df_products, "products", cur=cur, conn=conn)
        load.load(df_order_items, "order_items", cur=cur, conn=conn)

        cur.close()
        conn.close()

        LOGGER.info(f'lambda_handler: done')

    except Exception as e:
        LOGGER.error(f'lambda_handler: failure: error={e}, file=')




    # # TODO implement
    # print('Hello from Lambda')
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello, Marcell!')
    # }
