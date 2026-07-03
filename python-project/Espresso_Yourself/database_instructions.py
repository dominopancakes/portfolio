def create_order_table():
    result = """
    CREATE TABLE IF NOT EXISTS Orders (
        id SERIAL PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        customer_address VARCHAR(255) NOT NULL,
        customer_phone_number VARCHAR(20) NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'Pending'
    );
    """
    return result

def create_branch_table():
    result = """
    CREATE TABLE branch (
    branch_guid UUID PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
    """
    return result


def create_product_table():
    result = """
    CREATE TABLE product (
    product_guid UUID PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    product_price DECIMAL(10,2) NOT NULL
);
    """
    return result

def create_customer_order_table():
    result = """
    CREATE TABLE customer_order (
    order_guid UUID PRIMARY KEY,
    branch_guid UUID NOT NULL,
    order_timestamp TIMESTAMP NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,

    CONSTRAINT fk_order_branch
        FOREIGN KEY (branch_guid)
        REFERENCES branch(branch_guid),

   
);
    """
    return result

def create_order_item_table():
    result = """
    CREATE TABLE order_item (
    order_item_guid UUID PRIMARY KEY,
    order_guid UUID NOT NULL,
    product_guid UUID NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT fk_orderitem_order
        FOREIGN KEY (order_guid)
        REFERENCES customer_order(order_guid),

    CONSTRAINT fk_orderitem_product
        FOREIGN KEY (product_guid)
        REFERENCES product(product_guid)
);
    """
    return result


###=========================================

