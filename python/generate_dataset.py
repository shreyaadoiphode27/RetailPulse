import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 10000
NUM_PRODUCTS = 500
NUM_ORDERS = 50000
NUM_REVIEWS = 30000
NUM_RETURNS = 5000

OUTPUT_DIR = Path("../data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# BASIC DATA
# --------------------------------------------------

first_names = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Rahul",
    "Priya", "Rohan", "Sneha", "Karan", "Isha",
    "Aditya", "Neha", "Vikram", "Pooja", "Kabir",
    "Riya", "Yash", "Simran", "Aman", "Shreya"
]

last_names = [
    "Sharma", "Patel", "Mehta", "Shah", "Gupta",
    "Joshi", "Desai", "Verma", "Kulkarni", "Singh",
    "Khan", "Nair", "Rao", "Mishra", "Jain"
]

cities = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad",
    "Pune", "Chennai", "Kolkata", "Ahmedabad",
    "Jaipur", "Lucknow"
]

states = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Bangalore": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh"
}

categories = {
    "Electronics": [
        "Smartphones", "Laptops", "Headphones",
        "Smart Watches", "Cameras"
    ],
    "Fashion": [
        "Men Clothing", "Women Clothing",
        "Footwear", "Ethnic Wear", "Accessories"
    ],
    "Home & Kitchen": [
        "Kitchen Appliances", "Furniture",
        "Home Decor", "Storage", "Cookware"
    ],
    "Beauty": [
        "Skincare", "Haircare", "Makeup",
        "Fragrances", "Personal Care"
    ],
    "Sports": [
        "Fitness Equipment", "Sportswear",
        "Outdoor", "Yoga", "Team Sports"
    ],
    "Books": [
        "Fiction", "Non Fiction", "Academic",
        "Self Help", "Technology"
    ],
    "Accessories": [
        "Bags", "Wallets", "Sunglasses",
        "Jewellery", "Travel Accessories"
    ]
}

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash on Delivery",
    "Net Banking",
    "Wallet"
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Cancelled"
]

return_reasons = [
    "Damaged Product",
    "Wrong Product",
    "Poor Quality",
    "Size Issue",
    "Changed Mind",
    "Late Delivery"
]

# --------------------------------------------------
# CUSTOMERS
# --------------------------------------------------

print("Generating customers...")

customers = []

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)

for i in range(1, NUM_CUSTOMERS + 1):

    name = random.choice(first_names) + " " + random.choice(last_names)
    city = random.choice(cities)

    signup_date = start_date + timedelta(
        days=random.randint(0, 1095)
    )

    customers.append([
        f"CUST{i:05d}",
        name,
        random.choice(["Male", "Female", "Other"]),
        random.randint(18, 65),
        city,
        states[city],
        signup_date.date()
    ])

customers_df = pd.DataFrame(
    customers,
    columns=[
        "customer_id",
        "customer_name",
        "gender",
        "age",
        "city",
        "state",
        "signup_date"
    ]
)

customers_df.to_csv(
    OUTPUT_DIR / "customers.csv",
    index=False
)

# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

print("Generating products...")

products = []

for i in range(1, NUM_PRODUCTS + 1):

    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])

    unit_price = round(
        np.random.uniform(300, 50000), 2
    )

    cost_price = round(
        unit_price * np.random.uniform(0.45, 0.85),
        2
    )

    products.append([
        f"PROD{i:04d}",
        f"{subcategory} Product {i}",
        category,
        subcategory,
        unit_price,
        cost_price
    ])

products_df = pd.DataFrame(
    products,
    columns=[
        "product_id",
        "product_name",
        "category",
        "sub_category",
        "unit_price",
        "cost_price"
    ]
)

products_df.to_csv(
    OUTPUT_DIR / "products.csv",
    index=False
)

# --------------------------------------------------
# ORDERS
# --------------------------------------------------

print("Generating orders...")

orders = []

customer_ids = customers_df["customer_id"].tolist()

for i in range(1, NUM_ORDERS + 1):

    customer = random.choice(customer_ids)

    order_date = start_date + timedelta(
        days=random.randint(0, 1095)
    )

    city = random.choice(cities)

    orders.append([
        f"ORD{i:06d}",
        customer,
        order_date.date(),
        random.choice(payment_methods),
        city,
        states[city],
        random.choice(order_statuses)
    ])

orders_df = pd.DataFrame(
    orders,
    columns=[
        "order_id",
        "customer_id",
        "order_date",
        "payment_method",
        "shipping_city",
        "shipping_state",
        "order_status"
    ]
)

orders_df.to_csv(
    OUTPUT_DIR / "orders.csv",
    index=False
)

# --------------------------------------------------
# ORDER ITEMS
# --------------------------------------------------

print("Generating order items...")

order_items = []

product_records = products_df.to_dict("records")

for order_id in orders_df["order_id"]:

    number_of_products = random.randint(1, 4)

    selected_products = random.sample(
        product_records,
        number_of_products
    )

    for product in selected_products:

        quantity = random.randint(1, 5)

        discount = round(
            random.uniform(0, 0.30),
            2
        )

        revenue = round(
            product["unit_price"] *
            quantity *
            (1 - discount),
            2
        )

        profit = round(
            revenue -
            (product["cost_price"] * quantity),
            2
        )

        order_items.append([
            order_id,
            product["product_id"],
            quantity,
            discount,
            revenue,
            profit
        ])

order_items_df = pd.DataFrame(
    order_items,
    columns=[
        "order_id",
        "product_id",
        "quantity",
        "discount",
        "revenue",
        "profit"
    ]
)

order_items_df.to_csv(
    OUTPUT_DIR / "order_items.csv",
    index=False
)

# --------------------------------------------------
# REVIEWS
# --------------------------------------------------

print("Generating reviews...")

reviews = []

for i in range(1, NUM_REVIEWS + 1):

    order = orders_df.sample(1).iloc[0]

    product = random.choice(
        products_df["product_id"].tolist()
    )

    rating = random.choices(
        [1, 2, 3, 4, 5],
        weights=[5, 8, 15, 30, 42]
    )[0]

    reviews.append([
        f"REV{i:06d}",
        order["order_id"],
        order["customer_id"],
        product,
        rating
    ])

reviews_df = pd.DataFrame(
    reviews,
    columns=[
        "review_id",
        "order_id",
        "customer_id",
        "product_id",
        "rating"
    ]
)

reviews_df.to_csv(
    OUTPUT_DIR / "reviews.csv",
    index=False
)

# --------------------------------------------------
# RETURNS
# --------------------------------------------------

print("Generating returns...")

returns = []

selected_orders = orders_df.sample(
    NUM_RETURNS,
    random_state=42
)

for i, (_, order) in enumerate(
    selected_orders.iterrows(),
    start=1
):

    return_date = pd.to_datetime(
        order["order_date"]
    ) + timedelta(
        days=random.randint(2, 20)
    )

    returns.append([
        f"RET{i:06d}",
        order["order_id"],
        return_date.date(),
        random.choice(return_reasons)
    ])

returns_df = pd.DataFrame(
    returns,
    columns=[
        "return_id",
        "order_id",
        "return_date",
        "return_reason"
    ]
)

returns_df.to_csv(
    OUTPUT_DIR / "returns.csv",
    index=False
)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n===================================")
print("RETAILPULSE DATASET CREATED!")
print("===================================")

print(f"Customers:   {len(customers_df):,}")
print(f"Products:    {len(products_df):,}")
print(f"Orders:      {len(orders_df):,}")
print(f"Order Items: {len(order_items_df):,}")
print(f"Reviews:     {len(reviews_df):,}")
print(f"Returns:     {len(returns_df):,}")

print("\nFiles saved inside the data folder.")