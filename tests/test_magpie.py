from magpie import Magpie, crunch_reminder
from task import (EVENT_HANDLERS, EVENTS_LOG, MAILBOX,
                  EventType, Task, TaskPerform, TaskStatus,
                  backlog_len, clear_enviroment, fetch_task, fetch_task_perform, run_time_machine)
import task as storage

def test_error():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("user1", "")

    assert response == "error occurred. use '/help' for list of avaible commands."


def test_unknown_command():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("user1", "task_add task99 tag256")

    assert response == "unknown command 'task_add'. use '/help' for list of avaible commands."


def test_admin_time_machine():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("admin", "/admin_time_machine 12.49")

    assert response == "and so 12.5 hours have passed..."


def test_help():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("user1", "/help")

    assert response.startswith("avaible commands:\n")


def test_add_task1():
    clear_enviroment()
    magpie = Magpie()

    assert backlog_len() == 0

    response = magpie.request("user1", "/task_add task42")

    assert response == "➕ task42 has been added."
    assert backlog_len() == 1
    assert fetch_task("task42") == Task("task42", set(), TaskStatus.NEW)


def test_add_task2():
    clear_enviroment()
    magpie = Magpie()

    assert backlog_len() == 0

    response = magpie.request("user1", "/task_add task1 tag2 tag1")

    assert response == "➕ task1 has been added.\ntask1 relates to tag1, tag2."
    assert backlog_len() == 1
    assert fetch_task("task1") == Task(
        "task1", {"tag1", "tag2"}, TaskStatus.NEW)


def test_add_tasks1():
    clear_enviroment()
    magpie = Magpie()

    assert backlog_len() == 0

    magpie.request("user1", "/task_add task1 tag1 tag2")
    magpie.request("user1", "/task_add task2 tag2")

    assert backlog_len() == 2
    assert fetch_task("task1") == Task(
        "task1", {"tag1", "tag2"}, TaskStatus.NEW)
    assert fetch_task("task2") == Task("task2", {"tag2"}, TaskStatus.NEW)


def test_backlog():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("user1", "/backlog")

    assert response == "backlog is empty."

    magpie.request("user1", "/task_add task1 tag1 tag2")
    magpie.request("user1", "/task_add task2 tag2")
    magpie.request("user1", "/task_add task3 tag1 tag2 tag3")
    response = magpie.request("user1", "/backlog")

    assert response == "backlog:\n" \
                       "🐦 NEW(3):\n" \
                       "task1 relates to tag1, tag2.\n" \
                       "task2 relates to tag2.\n" \
                       "task3 relates to tag1, tag2, tag3."

    magpie.request("user1", "/task_add task4")
    magpie.request("user2", "/task_start task1")
    magpie.request("user3", "/task_done task2")
    magpie.request("user3", "/task_start task1")
    magpie.request("user3", "/task_stop task1")
    magpie.request("user3", "/task_start task4")
    magpie.request("user3", "/task_stop task4")

    response = magpie.request("user1", "/backlog")

    assert backlog_len() == 4
    assert response == "backlog:\n" \
                       "🐦 NEW(1):\ntask3 relates to tag1, tag2, tag3.\n\n" \
                       "⏸ SUSPENDED(1):\ntask4 relates to .\n\n" \
                       "🛠 IN PROGRESS(1):\ntask1 relates to tag1, tag2.\n\n" \
                       "✅ DONE(1):\ntask2 relates to tag2."


def test_start_stop_single_user():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("user1", "/task_add task1 tag1 tag2 tag3")

    response = magpie.request("user1", "/task_start task1")

    assert fetch_task("task1") == Task(
        "task1", {"tag1", "tag2", "tag3"}, TaskStatus.IN_PROGRESS)
    assert fetch_task_perform("task1", "user1") == TaskPerform(
        "user1", "task1", 0, [0])
    assert storage.fetch_all_task_sessions("task1") == {"user1"}
    assert response == "🛠 you started working on task1.\n" \
                       "task1 relates to tag1, tag2, tag3.\n" \
                       "⭐ no one else currently working on task1."

    run_time_machine(4)
    response = magpie.request("user1", "/task_stop task1")

    assert not storage.is_have_any_sessions()
    assert fetch_task("task1") == Task(
        "task1", {"tag1", "tag2", "tag3"}, TaskStatus.SUSPENDED)
    assert fetch_task_perform("task1", "user1") == TaskPerform(
        "user1", "task1", 4, [4])
    assert response == "⏸ you have finished work on task1.\n" \
                       "a total of 4.0 hours were spent on task1.\n" \
                       "today you spent on task1 4.0 hours.\n" \
                       "please mark the time spent."


def test_time_format():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("user1", "/task_add task1 tag1 tag2 tag3")
    magpie.request("user1", "/task_start task1")
    run_time_machine(0.49)
    response = magpie.request("user1", "/task_stop task1")

    assert response == "⏸ you have finished work on task1.\n" \
                       "a total of 0.5 hours were spent on task1.\n" \
                       "today you spent on task1 0.5 hours.\n" \
                       "please mark the time spent."


def test_start_stop_many_users():
    clear_enviroment()
    magpie = Magpie()

    assert not storage.is_have_any_sessions()

    magpie.request("manager", "/task_add task1 tag1 tag2")
    run_time_machine(1)
    magpie.request("developer1", "/task_start task1")

    assert storage.fetch_all_task_sessions("task1") == {"developer1"}

    run_time_machine(2)
    response = magpie.request("developer2", "/task_start task1")

    assert storage.fetch_all_task_sessions("task1") == {"developer1", "developer2"}
    assert response == "🛠 you started working on task1.\n" \
                       "task1 relates to tag1, tag2.\n" \
                       "🤝 developer1 currently working on task1 also."

    response = magpie.request("developer3", "/task_start task1")

    assert storage.fetch_all_task_sessions("task1") == {"developer1", "developer2", "developer3"}
    assert response == "🛠 you started working on task1.\n" \
                       "task1 relates to tag1, tag2.\n" \
                       "🤝 developer1, developer2 currently working on task1 also."

    magpie.request("developer3", "/task_stop task1")
    run_time_machine(3)
    magpie.request("developer1", "/task_stop task1")

    assert storage.fetch_all_task_sessions("task1") == {"developer2"}
    assert fetch_task("task1") == Task(
        "task1", {"tag1", "tag2"}, TaskStatus.IN_PROGRESS)
    assert fetch_task_perform("task1", "developer1") == TaskPerform(
        "developer1", "task1", 5, [5])
    assert fetch_task_perform("task1", "developer2") == TaskPerform(
        "developer2", "task1", 3, [3])

    run_time_machine(1)
    magpie.request("developer2", "/task_stop task1")

    assert not storage.is_have_any_sessions()
    assert fetch_task("task1") == Task(
        "task1", {"tag1", "tag2"}, TaskStatus.SUSPENDED)
    assert fetch_task_perform("task1", "developer1") == TaskPerform(
        "developer1", "task1", 5, [5])
    assert fetch_task_perform("task1", "developer2") == TaskPerform(
        "developer2", "task1", 3 + 1, [3 + 1])


def test_add_tags():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("manager", "/task_add task1")

    assert len(fetch_task("task1").tags) == 0

    response = magpie.request("manager", "/tag_add task1 tag1")

    assert fetch_task("task1").tags == {"tag1"}
    assert response == "tags for task1 updated. task1 now relates to tag1."

    response = magpie.request("developer", "/tag_add task1 tag2 tag3")

    assert fetch_task("task1").tags == {"tag1", "tag2", "tag3"}
    assert response == "tags for task1 updated. task1 now relates to tag1, tag2, tag3."


def test_events_spent_time():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("manager", "/task_add task1 tag1 tag2")
    magpie.request("manager", "/task_add task2 tag1 tag3")
    magpie.request("developer1", "/task_start task1")
    run_time_machine(4)
    magpie.request("developer2", "/task_start task1")
    run_time_machine(5)
    magpie.request("developer1", "/task_stop task1")
    run_time_machine(1)
    magpie.request("developer2", "/task_stop task1")

    response = magpie.request("manager", "/events")

    assert response == "events for task1:\n" \
    "⏱ a total of 15.0 hours were spent on task.\n" \
               "ℹ task relates to tag1, tag2.\n" \
               "⚠ developer1 spent 9.0 hours on task in a single session.\n" \
               "\n" \
               "no events for task2.\n" \
               "\n"


def test_events_new_tags():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("manager", "/task_add task1 tag1 tag2")
    run_time_machine(2)
    magpie.request("developer1", "/tag_add task1 tag3")
    run_time_machine(4)

    response = magpie.request("manager", "/events")

    assert response == "events for task1:\n" \
    "ℹ task relates to tag1, tag2, tag3.\n" \
               "➕ developer1 added new tags for task: tag3.\n\n"



def test_crunch_reminder():
    clear_enviroment()
    EVENT_HANDLERS[EventType.CRUNCH] = crunch_reminder

    magpie = Magpie()

    magpie.request("manager", "/task_add task1 tag1 tag2")
    magpie.request("developer1", "/task_start task1")
    run_time_machine(7)

    assert len(EVENTS_LOG) == 0
    assert len(MAILBOX) == 0

    run_time_machine(1.5)

    assert len(EVENTS_LOG) == 0
    assert len(MAILBOX) == 1

    assert MAILBOX == [
    ("developer1", "⚠ you are working on task1 over 8 hours.")]


def test_daily_report():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("manager", "/daily_report")

    assert response == "there is no implementations for '/daily_report' command. YET."


def test_weekly_report():
    clear_enviroment()
    magpie = Magpie()

    response = magpie.request("manager", "/weekly_report")

    assert response == "there is no implementations for '/weekly_report' command. YET."


def test_task_done():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("manager", "/task_add task1 tag1")

    assert fetch_task("task1") == Task("task1", {"tag1"}, TaskStatus.NEW)

    response = magpie.request("manager", "/task_done task1")

    assert fetch_task("task1") == Task("task1", {"tag1"}, TaskStatus.DONE)
    assert response == "you marked task1 as done."


def test_events_task_done():
    clear_enviroment()
    magpie = Magpie()

    magpie.request("manager", "/task_add task1 tag1")
    response = magpie.request("developer", "/task_done task1")

    response = magpie.request("manager", "/events")

    assert response == "events for task1:\n" \
	    	       "ℹ task relates to tag1.\n" \
                       "✅ developer marked task as done.\n\n"
