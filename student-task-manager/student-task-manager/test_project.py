# test_project.py
# Simple tests for the analysis functions. Run with:  python test_project.py

from datetime import date, timedelta
import analysis


def make_task(title, days_from_now, priority, hours, status="Pending", subject="Maths"):
    d = date.today() + timedelta(days=days_from_now)
    return {"id": 1, "title": title, "subject": subject, "deadline": str(d),
            "priority": priority, "hours": hours, "status": status}


def test_overdue_beats_future():
    late = make_task("late", -1, 1, 1)
    later = make_task("far", 10, 3, 1)
    assert analysis.task_score(late) > analysis.task_score(later)
    print("overdue vs future: OK")


def test_ranking_order():
    tasks = [make_task("far", 10, 1, 1), make_task("today", 0, 3, 2), make_task("soon", 3, 2, 2)]
    ranked = analysis.rank_tasks(tasks)
    assert ranked[0]["title"] == "today"
    assert ranked[2]["title"] == "far"
    print("ranking order: OK")


def test_done_tasks_not_ranked():
    tasks = [make_task("a", 1, 3, 1, "Done"), make_task("b", 1, 3, 1)]
    assert len(analysis.rank_tasks(tasks)) == 1
    print("done tasks skipped: OK")


def test_overload():
    tasks = [make_task("a", 2, 2, 4), make_task("b", 2, 2, 4), make_task("c", 5, 1, 1)]
    assert len(analysis.find_overloaded_days(tasks)) == 1
    print("overload detection: OK")


def test_completion_rate():
    tasks = [make_task("a", 1, 1, 1, "Done"), make_task("b", 1, 1, 1)]
    assert analysis.completion_rate(tasks) == 50
    assert analysis.completion_rate([]) == 0
    print("completion rate: OK")


def test_empty_list():
    assert len(analysis.get_suggestions([])) == 1
    assert analysis.rank_tasks([]) == []
    print("empty list: OK")


test_overdue_beats_future()
test_ranking_order()
test_done_tasks_not_ranked()
test_overload()
test_completion_rate()
test_empty_list()
print("\nAll tests passed.")
