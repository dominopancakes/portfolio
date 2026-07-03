from utils import s3_utils

import pandas as pd
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def get_data(bucket_name, s3_key):

    try:
        s3_object = s3_utils.create_s3_object(bucket_name, s3_key)

        df = pd.read_csv(
            s3_object['Body'],
            header=None,
            names=["payment_time", "city", "customer_name", "basket", "total_price", "payment_method", "card_number"]
            )

    except pd.errors.ParserError:
        LOGGER.error(f'Error: CSV parsing failed for {s3_key}')
        raise

    except Exception as e:
        LOGGER.error(f'Error loading {s3_key}: {e}')
        raise e

    return df