import pandas as pd

df = pd.read_csv(
    "sample-data.csv",
    sep="\t",
    header=None,
    names=[
        "datetime",
        "store",
        "customer",
        "products",
        "total",
        "payment_method",
        "card_number"
    ]
)

records = df.to_dict(orient="records")

print(f"Records extracted: {len(records)}")

for record in records[:5]:
    print(record)
    