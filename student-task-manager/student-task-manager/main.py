# main.py
# Student Task Manager - menu and user input part
# Run with:  python main.py

from datetime import date, datetime
import storage
import analysis


def ask_text(message):
    while True:
        text = input(message).strip()
        if text != "":
            return text
        print("This cannot be empty. Try again.")


def ask_date(message):
    while True:
        text = input(message).strip()
        try:
            d = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Wrong format. Use YYYY-MM-DD, for example 2026-11-20")
            continue
        if d < date.today():
            print("Deadline cannot be in the past.")
            continue
        return text


def ask_int(message, low, high):
    while True:
        text = input(message).strip()
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print("Enter a whole number from", low, "to", high)


def ask_hours(message):
    while True:
        text = input(message).strip()
        try:
            h = float(text)
        except ValueError:
            print("Please enter a number, like 2 or 1.5")
            continue
        if h <= 0 or h > 24:
            print("Hours must be more than 0 and at most 24.")
            continue
        return h


def print_tasks(task_list):
    if len(task_list) == 0:
        print("No tasks to show.")
        return
    print()
    print("ID  Title                  Subject      Deadline    Pri  Hrs  Status")
    print("-" * 70)
    for t in task_list:
        print(str(t["id"]).ljust(3), t["title"][:22].ljust(22), t["subject"][:12].ljust(12),
              t["deadline"], str(t["priority"]).center(4), str(t["hours"]).ljust(4), t["status"])


def add_task(tasks):
    print("\n--- Add New Task ---")
    title = ask_text("Title: ")
    subject = ask_text("Subject: ")
    deadline = ask_date("Deadline (YYYY-MM-DD): ")
    priority = ask_int("Priority (1=low, 2=medium, 3=high): ", 1, 3)
    hours = ask_hours("Estimated hours needed: ")

    task = {
        "id": storage.next_id(tasks),
        "title": title,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
        "hours": hours,
        "status": "Pending",
    }
    tasks.append(task)
    storage.save_tasks(tasks)
    print("Task added with ID", task["id"])

    # warn straight away if this makes a day too heavy
    if deadline in analysis.find_overloaded_days(tasks):
        print("Warning: you now have too many hours due on", deadline)


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def mark_done(tasks):
    print_tasks(analysis.get_pending(tasks))
    if len(analysis.get_pending(tasks)) == 0:
        return
    task_id = ask_int("\nEnter ID of the task you finished: ", 1, 100000)
    task = find_task(tasks, task_id)
    if task is None:
        print("No task with that ID.")
    elif task["status"] == "Done":
        print("That task is already done.")
    else:
        task["status"] = "Done"
        storage.save_tasks(tasks)
        print("Marked as done:", task["title"])


def delete_task(tasks):
    print_tasks(tasks)
    if len(tasks) == 0:
        return
    task_id = ask_int("\nEnter ID of the task to delete: ", 1, 100000)
    task = find_task(tasks, task_id)
    if task is None:
        print("No task with that ID.")
        return
    sure = input("Delete '" + task["title"] + "'? (y/n): ").strip().lower()
    if sure == "y":
        tasks.remove(task)
        storage.save_tasks(tasks)
        print("Deleted.")
    else:
        print("Cancelled.")


def search_by_subject(tasks):
    word = ask_text("Subject to search: ").lower()
    found = []
    for t in tasks:
        if word in t["subject"].lower():
            found.append(t)
    print_tasks(found)


def show_priority_list(tasks):
    ranked = analysis.rank_tasks(tasks)
    if len(ranked) == 0:
        print("No pending tasks.")
        return
    print("\n--- What to do first ---")
    n = 1
    for t in ranked:
        left = analysis.days_left(t)
        if left < 0:
            when = "OVERDUE by " + str(-left) + " day(s)"
        elif left == 0:
            when = "due TODAY"
        else:
            when = "due in " + str(left) + " day(s)"
        print(str(n) + ".", t["title"], "(" + t["subject"] + ") -", when,
              "| score:", analysis.task_score(t))
        n += 1


def show_subject_summary(tasks):
    summary = analysis.subject_summary(tasks)
    if len(summary) == 0:
        print("No tasks yet.")
        return
    print("\n--- Subject Summary ---")
    for s in summary:
        info = summary[s]
        print(s + ":", info["done"], "of", info["total"], "done,",
              info["pending_hours"], "hours still pending")
    print("Overall completion:", round(analysis.completion_rate(tasks), 1), "%")


def show_workload(tasks):
    overloaded = analysis.find_overloaded_days(tasks)
    print("\n--- Workload Check (limit:", analysis.DAILY_HOUR_LIMIT, "hours/day) ---")
    if len(overloaded) == 0:
        print("No overloaded days. Good!")
    for d in overloaded:
        print(d, "->", overloaded[d], "hours of work due")


def show_suggestions(tasks):
    print("\n--- Suggestions ---")
    for tip in analysis.get_suggestions(tasks):
        print("*", tip)


def save_report(tasks):
    text = analysis.make_report(tasks)
    with open("report.txt", "w") as f:
        f.write(text)
    print("Report saved as report.txt")


def show_menu():
    print("\n===== STUDENT TASK MANAGER =====")
    print("1. Add task")
    print("2. View all tasks")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Search by subject")
    print("6. What should I do first? (priority list)")
    print("7. Subject summary")
    print("8. Workload check")
    print("9. Suggestions")
    print("10. Save report to file")
    print("0. Exit")


def main():
    tasks = storage.load_tasks()
    print("Welcome! Loaded", len(tasks), "task(s).")

    while True:
        show_menu()
        choice = ask_int("Choose an option: ", 0, 10)

        if choice == 1:
            add_task(tasks)
        elif choice == 2:
            print_tasks(tasks)
        elif choice == 3:
            mark_done(tasks)
        elif choice == 4:
            delete_task(tasks)
        elif choice == 5:
            search_by_subject(tasks)
        elif choice == 6:
            show_priority_list(tasks)
        elif choice == 7:
            show_subject_summary(tasks)
        elif choice == 8:
            show_workload(tasks)
        elif choice == 9:
            show_suggestions(tasks)
        elif choice == 10:
            save_report(tasks)
        elif choice == 0:
            print("Goodbye!")
            break


main()
