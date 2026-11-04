# Student Task Manager

A command-line task manager for students, written in plain Python (no external libraries).
Course project for **Computational Thinking and Programming (2026CSAE100)**.

## Problem
Students handle many assignments, labs and exams at once and often miss deadlines or
leave too much work for the last day. This program helps them record tasks and decide what to do first.

## Features
- Add, view, search, complete and delete tasks
- Tasks are saved in `tasks.csv` and loaded again on the next run
- **Priority ranking**: each pending task gets a score from its deadline, priority and hours needed
- **Workload check**: warns when more than 6 hours of work are due on one day
- **Subject summary**: tasks done and hours pending for each subject
- **Suggestions**: simple rule-based advice (overdue tasks, heavy subjects, progress)
- **Report**: saves a summary to `report.txt`
- Input checking for dates, numbers and empty text

## Files
| File | Purpose |
|------|---------|
| `main.py` | Menu and user input |
| `storage.py` | Reading and writing `tasks.csv` |
| `analysis.py` | Scoring, ranking, workload check, summary, suggestions, report |
| `test_project.py` | Tests for the analysis functions |

## How to run
```
python main.py
python test_project.py
```
Requires Python 3.6 or newer.

## Scoring rule
`score = urgency + (priority x 10) + hours (max 10)`

Urgency: overdue = 50, due today = 40, within 2 days = 30, within 7 days = 20, later = 10.

## Team
| Name | Part |
|------|------|
| Member 1 | Rohit Kumar |
| Member 2 | Aryaman Srivasta |
| Member 3 | Sparsh Kaushik |
| Member 4 | Harshit Pandey|
