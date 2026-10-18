import sys

sys.path.append("scripts")  # lets Python find bmi.py, which now lives in the root scripts folder
import bmi

result = bmi.compute_bmi(70, 1.75)
print(f"Computed BMI: {result:.2F}")

people = [
    {"name": "Alice", "height": 1.75, "weight": 70},
    {"name": "Bob", "height": 1.80, "weight": 75},
    {"name": "Charlie", "height": 1.68, "weight": 65},
    {"name": "Diana", "height": 1.62, "weight": 58},
    {"name": "Ethan", "height": 1.90, "weight": 88},
    {"name": "Fiona", "height": 1.70, "weight": 64},
]

for person in people:
    print(person)

print(person["height"])
print(people["height"])

for person in people:
    value = bmi(person["height"], person["weight"])
    print(person["name"], round(value, 1), category(value))

counts = {}
highest_person = None
highest_bmi = 0

for person in people:
    value = bmi(person["height"], person["weight"])
    cat = category(value)
    counts[cat] = counts.get(cat, 0) + 1
 
    if value > highest_bmi:
        highest_bmi = value
        highest_person = person

        print(counts)
print("Highest BMI:", highest_person["name"], round(highest_bmi, 1))