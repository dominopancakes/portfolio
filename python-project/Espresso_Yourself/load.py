from database_connect import get_connection


def load_product(product_id, product_name, product_price):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO product (
            product_id,
            product_name,
            product_price
        )
        VALUES (%s, %s, %s)
    """, (
        product_id,
        product_name,
        product_price
    ))

    conn.commit()

    cur.close()
    conn.close()


def load_order(
    order_id,
    customer_id,
    branch_id,
    timestamp,
    total_amount,
    payment_method,
    card_number
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO customer_order (
            order_id,
            customer_id,
            branch_id,
            order_timestamp,
            total_amount,
            payment_method,
            card_number
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        order_id,
        customer_id,
        branch_id,
        timestamp,
        total_amount,
        payment_method,
        card_number
    ))

    conn.commit()

    cur.close()
    conn.close()