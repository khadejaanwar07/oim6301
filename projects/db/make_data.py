import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Set up the data folder
data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)

# Use the same random data each time
random.seed(6301)

# Choose the reference date
as_of = date(2026, 11, 1)

# Function to save data into CSV files
def save_csv(filename, columns, rows):
    with open(data_folder / filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)


# Members Table
# Generate 50 loyalty members

members = []

for i in range(1, 51):
    member_id = i
    first_name = f"Member{i}"
    mobile = f"617555{i:04d}"
    email = f"member{i}@example.com" if i % 5 != 0 else ""
    join_date = date(2025, 1, 1) + timedelta(days=random.randint(0, 300))
    points_balance = random.randint(0, 500)

    members.append([
        member_id,
        first_name,
        mobile,
        email,
        join_date,
        points_balance
    ])

save_csv(
    "members.csv",
    ["member_id", "first_name", "mobile", "email", "join_date", "points_balance"],
    members
)

print("Created 50 loyalty members")

# Products Table
# Generate 25 menu products

product_names = [
    "Latte", "Cappuccino", "Americano", "Espresso",
    "Mocha", "Cold Brew", "Iced Latte", "Macchiato",
    "Flat White", "Drip Coffee",
    "Green Tea", "Black Tea", "Chai Latte",
    "Matcha Latte", "Iced Tea",
    "Blueberry Muffin", "Croissant", "Bagel",
    "Chocolate Cookie", "Banana Bread",
    "Sandwich", "Brownie", "Yogurt",
    "Bottled Water", "Orange Juice"
]

products = []

for i, name in enumerate(product_names, start=1):

    if i <= 10:
        category = "coffee"
    elif i <= 15:
        category = "tea"
    elif i <= 23:
        category = "food"
    else:
        category = "other"

    cost = round(random.uniform(0.50, 3.00), 2)
    price = round(cost + random.uniform(1.00, 4.00), 2)
    available_today = random.choice([True, True, True, False])

    products.append([
        i,
        name,
        category,
        price,
        cost,
        available_today
    ])

save_csv(
    "products.csv",
    ["product_id", "name", "category", "price", "cost", "available_today"],
    products
)

print("Created 25 menu products")

# Options Table
# Generate 10 drink add-ons

option_names = [
    "Extra Shot",
    "Oat Milk",
    "Almond Milk",
    "Soy Milk",
    "Vanilla Syrup",
    "Caramel Syrup",
    "Hazelnut Syrup",
    "Whipped Cream",
    "Chocolate Drizzle",
    "Extra Ice"
]

options = []

for i, name in enumerate(option_names, start=1):
    cost = round(random.uniform(0.05, 0.50), 2)
    price = round(random.uniform(0.00, 1.50), 2)

    options.append([
        i,
        name,
        price,
        cost
    ])

save_csv(
    "options.csv",
    ["option_id", "name", "price", "cost"],
    options
)

print("Created 10 drink options")

# Orders Table
# Generate 1,200 orders over 12 months

from datetime import datetime, time

orders = []

for i in range(1, 1201):
    order_id = i

    # Generate a random date within the past 12 months
    days_ago = random.randint(0, 364)
    order_date = as_of - timedelta(days=days_ago)

    # Generate a time between 7 AM and 7 PM
    hour = random.choices(
    population=list(range(7, 19)),
    weights=[8, 15, 18, 16, 12, 17, 16, 8, 6, 5, 4, 3],
    k=1
)[0]
    minute = random.randint(0, 59)

    ordered_at = datetime.combine(
        order_date,
        time(hour, minute)
    )

    # Some customers are loyalty members, others are not
    member_id = random.randint(1, 45) if random.random() < 0.75 else ""

    # Orders can be placed at the counter or through the app
    channel = random.choice(["counter", "app"])

    orders.append([
        order_id,
        ordered_at,
        member_id,
        channel
    ])

save_csv(
    "orders.csv",
    ["order_id", "ordered_at", "member_id", "channel"],
    orders
)

print("Created 1,200 orders")

# Order Lines Table
# Generate 1 to 3 product lines for each order

order_lines = []
line_id = 1

for order in orders:
    order_id = order[0]

    # Each order has between 1 and 3 products
    num_lines = random.randint(1, 3)

    # Choose products without repeating them in the same order
    selected_products = random.sample(products[:-2], num_lines)

    for product in selected_products:
        product_id = product[0]
        quantity = random.randint(1, 3)
        unit_price = product[3]

        order_lines.append([
            line_id,
            order_id,
            product_id,
            quantity,
            unit_price
        ])

        line_id += 1

save_csv(
    "order_lines.csv",
    ["line_id", "order_id", "product_id", "quantity", "unit_price"],
    order_lines
)

print(f"Created {len(order_lines)} order lines")

# Line Options Table
# Generate add-ons for coffee and tea products

line_options = []

for line in order_lines:
    line_id = line[0]
    product_id = line[2]

    # Only coffee and tea products can have add-ons
    product_category = products[product_id - 1][2]

    if product_category in ["coffee", "tea"]:

        # Some drinks have no add-ons
        num_options = random.randint(0, 3)

        selected_options = random.sample(options, num_options)

        for option in selected_options:
            option_id = option[0]
            price_charged = option[2]

            line_options.append([
                line_id,
                option_id,
                price_charged
            ])

save_csv(
    "line_options.csv",
    ["line_id", "option_id", "price_charged"],
    line_options
)

print(f"Created {len(line_options)} line options")

# Payments Table
# Generate payments for every order

from decimal import Decimal

payments = []
payment_id = 1

# Calculate the total for each order
order_totals = {order[0]: Decimal("0.00") for order in orders}

# Add the cost of products
for line in order_lines:
    line_id, order_id, product_id, quantity, unit_price = line

    order_totals[order_id] += Decimal(str(unit_price)) * quantity

# Add the cost of options
line_details = {
    line[0]: (line[1], line[3])
    for line in order_lines
}

for line_id, option_id, price_charged in line_options:
    order_id, quantity = line_details[line_id]

    order_totals[order_id] += Decimal(str(price_charged)) * quantity

# Generate payments
for order_id, total in order_totals.items():

    # Create exactly two orders with incorrect payment totals
    if order_id in [1, 2]:
        total += Decimal("1.00")

    # Some orders use split payments
    if random.random() < 0.25 and total >= Decimal("2.00"):

        first_amount = (total / 2).quantize(Decimal("0.01"))
        second_amount = total - first_amount

        payments.append([
            payment_id, order_id, "card", first_amount
        ])
        payment_id += 1

        payments.append([
            payment_id, order_id, "points", second_amount
        ])
        payment_id += 1

    else:
        method = random.choice(["cash", "card", "app", "points"])

        payments.append([
            payment_id, order_id, method, total
        ])
        payment_id += 1

save_csv(
    "payments.csv",
    ["payment_id", "order_id", "method", "amount"],
    payments
)

print(f"Created {len(payments)} payments")
print("Intentional payment mismatches: Orders 1 and 2")
