import csv
import json
import uuid

file_path = 'sample_leeds_data.csv'

def split_items(items_string):
    return [item.strip() for item in items_string.split(",")]

def read_leeds_data(file_path):
    print(f"--- Loading and parsing CSV file: {file_path} ---")

    leeds_store_orders = {}


    orders = []
    products = {}
    order_items = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)


        for row in csv_reader:
            
            # Remove sensitive data
            row.pop('Customer Name', None)
            row.pop('Card Number', None)

            # UUID instead of numeric ID
            order_id = str(uuid.uuid4())    

            #item split
            row["Items Ordered"] = split_items(row["Items Ordered"])

            #name + price structure
            structured_items = []


            for item in row["Items Ordered"]:
                name, price = item.rsplit(" - ", 1)

                structured_items.append({
                    "name": name.strip(),
                    "price": float(price.strip())
                })

            # Replace list with structured version
            row["Items Ordered"] = structured_items

            #Order table
            orders.append({
                "order_id": order_id,
                "timestamp": row["Timestamp"],
                "location": row["Location"],
                "total_amount": float(row["Total Amount"]),
                "payment_method": row["Payment Method"]
            })

            for item in structured_items:

                name = item["name"]
                price = item["price"]
                
                #Product table
                if name not in products:
                    product_id = str(uuid.uuid4())
                    products[name] = {
                        "product_id": product_id,
                        "price": price
                    }

                product_id = products[name]["product_id"]

                #Order_items table
                order_items.append({
                    "order_item_id": str(uuid.uuid4()),
                    "order_id": order_id,
                    "product_id": product_id
                })


    leeds_store_orders = {
        "orders": orders,
        "products": [
            {"product_name": name, "product_id": details["product_id"], "price": details["price"]}
            for name, details in products.items()
        ],
        "order_items": order_items
    }

    json_output = json.dumps(leeds_store_orders, indent=4)
    return json_output


leeds_json_data = read_leeds_data(file_path)

output_file = 'leeds_shop_orders.json'

with open(output_file, mode='w', encoding='utf-8') as json_file:
    json_file.write(leeds_json_data)

print("\n--- FINAL PARSED JSON DATA ---")
print(leeds_json_data)