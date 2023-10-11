import csv

with open("exemple.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "email", "phone"])
