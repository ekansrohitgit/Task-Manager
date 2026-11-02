# analysis.py
# All the "thinking" part of the project: ranking, overload check,
# subject summary, suggestions and report generation

from datetime import date, datetime

DAILY_HOUR_LIMIT = 6   # more than this many hours due on one day = overload


def days_left(task):
    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
    return (deadline - date.today()).days


def task_score(task):
    # higher score = should be done sooner
    left = days_left(task)

    if left < 0:
        urgency = 50
    elif left == 0:
        urgency = 40
    elif left <= 2:
        urgency = 30
    elif left <= 7:
        urgency = 20
    else:
        urgency = 10

    # priority is 1 (low) to 3 (high)
    score = urgency + task["priority"] * 10

    # long tasks need an earlier start, so add a little (max 10)
    extra = task["hours"]
    if extra > 10:
        extra = 10
    return score + extra


def get_pending(tasks):
    pending = []
    for t in tasks:
        if t["status"] == "Pending":
            pending.append(t)
    return pending


def rank_tasks(tasks):
    ranked = get_pending(tasks)
    # simple bubble sort on score (biggest first)
    n = len(ranked)
    for i in range(n):
        for j in range(0, n - i - 1):
            if task_score(ranked[j]) < task_score(ranked[j + 1]):
                ranked[j], ranked[j + 1] = ranked[j + 1], ranked[j]
    return ranked


def find_overloaded_days(tasks):
    # add up the hours of pending tasks for each deadline date
    hours_per_day = {}
    for t in get_pending(tasks):
        d = t["deadline"]
        hours_per_day[d] = hours_per_day.get(d, 0) + t["hours"]

    overloaded = {}
    for d in hours_per_day:
        if hours_per_day[d] > DAILY_HOUR_LIMIT:
            overloaded[d] = hours_per_day[d]
    return overloaded


def subject_summary(tasks):
    summary = {}
    for t in tasks:
        s = t["subject"]
        if s not in summary:
            summary[s] = {"total": 0, "done": 0, "pending_hours": 0}
        summary[s]["total"] += 1
        if t["status"] == "Done":
            summary[s]["done"] += 1
        else:
            summary[s]["pending_hours"] += t["hours"]
    return summary


def completion_rate(tasks):
    if len(tasks) == 0:
        return 0
    done = 0
    for t in tasks:
        if t["status"] == "Done":
            done += 1
    return done / len(tasks) * 100


def get_suggestions(tasks):
    tips = []
    pending = get_pending(tasks)

    if len(tasks) == 0:
        return ["No tasks yet. Add your first task to get started."]
    if len(pending) == 0:
        return ["All tasks are done. Great work!"]

    overdue = 0
    due_today = 0
    for t in pending:
        left = days_left(t)
        if left < 0:
            overdue += 1
        elif left == 0:
            due_today += 1

    if overdue > 0:
        tips.append(str(overdue) + " task(s) are overdue. Finish these first.")
    if due_today > 0:
        tips.append(str(due_today) + " task(s) are due today.")

    for d in find_overloaded_days(tasks):
        tips.append("Too much work due on " + d + ". Start some of it earlier.")

    # subject with the most pending hours
    summary = subject_summary(tasks)
    busiest = ""
    most = 0
    for s in summary:
        if summary[s]["pending_hours"] > most:
            most = summary[s]["pending_hours"]
            busiest = s
    if busiest != "":
        tips.append("Most pending work is in " + busiest + " (" + str(most) + " hours).")

    rate = completion_rate(tasks)
    if rate < 30:
        tips.append("Only " + str(round(rate)) + "% of tasks are done. Try finishing one small task today.")
    elif rate >= 70:
        tips.append("You have completed " + str(round(rate)) + "% of your tasks. Keep going!")

    if len(tips) == 0:
        tips.append("Nothing urgent. You are on track.")
    return tips


def make_report(tasks):
    lines = []
    lines.append("STUDENT TASK MANAGER - REPORT")
    lines.append("Generated on: " + str(date.today()))
    lines.append("=" * 40)
    lines.append("Total tasks : " + str(len(tasks)))
    lines.append("Pending     : " + str(len(get_pending(tasks))))
    lines.append("Completed   : " + str(len(tasks) - len(get_pending(tasks))))
    lines.append("Completion  : " + str(round(completion_rate(tasks), 1)) + "%")
    lines.append("")

    lines.append("Subject-wise summary")
    lines.append("-" * 40)
    summary = subject_summary(tasks)
    for s in summary:
        info = summary[s]
        lines.append(s + ": " + str(info["done"]) + "/" + str(info["total"]) +
                     " done, " + str(info["pending_hours"]) + " hrs pending")
    lines.append("")

    lines.append("Priority order (pending)")
    lines.append("-" * 40)
    number = 1
    for t in rank_tasks(tasks):
        lines.append(str(number) + ". " + t["title"] + " [" + t["subject"] +
                     "] due " + t["deadline"] + " (score " + str(task_score(t)) + ")")
        number += 1
    lines.append("")

    lines.append("Suggestions")
    lines.append("-" * 40)
    for tip in get_suggestions(tasks):
        lines.append("- " + tip)

    return "\n".join(lines)
