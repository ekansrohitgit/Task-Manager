# storage.py
# Handles reading and writing tasks to the CSV file

import csv
import os

FILE_NAME = "tasks.csv"
FIELDS = ["id", "title", "subject", "deadline", "priority", "hours", "status"]


def load_tasks():
    tasks = []
    if not os.path.exists(FILE_NAME):
        return tasks

    with open(FILE_NAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # csv gives everything as text, so convert the numbers back
            try:
                row["id"] = int(row["id"])
                row["priority"] = int(row["priority"])
                row["hours"] = float(row["hours"])
                tasks.append(row)
            except (ValueError, KeyError):
                print("Skipping a broken row in", FILE_NAME)
    return tasks


def save_tasks(tasks):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for t in tasks:
            writer.writerow(t)


def next_id(tasks):
    if len(tasks) == 0:
        return 1
    biggest = 0
    for t in tasks:
        if t["id"] > biggest:
            biggest = t["id"]
    return biggest + 1
