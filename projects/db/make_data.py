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