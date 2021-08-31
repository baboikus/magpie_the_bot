from task import (Task, TaskPerform,
                  TaskStatus, clear_enviroment, run_time_machine,
                  new_task, new_task_perform, fetch_task_perform,
                  add_session_performer)


def test_time_machine():
    clear_enviroment()

    new_task(Task("task_id1", {}, TaskStatus.IN_PROGRESS))
    new_task(Task("task_id2", {}, TaskStatus.NEW))
    new_task(Task("task_id3", {}, TaskStatus.SUSPENDED))
    new_task(Task("task_id4", {}, TaskStatus.DONE))

    new_task_perform(TaskPerform("performer_id1", "task_id1", 2))
    new_task_perform(TaskPerform("performer_id2", "task_id1", 0))

    add_session_performer("task_id1", "performer_id1")
    add_session_performer("task_id1", "performer_id2")

    new_task_perform(TaskPerform("performer_id1", "task_id2", 0))
    new_task_perform(TaskPerform("performer_id1", "task_id3", 6.2))
    new_task_perform(TaskPerform("performer_id2", "task_id4", 50.6))

    assert fetch_task_perform("task_id1", "performer_id1") \
        == TaskPerform("performer_id1", "task_id1", 2)
    assert fetch_task_perform("task_id1", "performer_id2") \
        == TaskPerform("performer_id2", "task_id1", 0)

    run_time_machine(12.5)

    assert fetch_task_perform("task_id1", "performer_id1") \
        == TaskPerform("performer_id1", "task_id1", 2 + 12.5, [2 + 12.5])
    assert fetch_task_perform("task_id1", "performer_id2") \
        == TaskPerform("performer_id2", "task_id1", 0 + 12.5, [12.5])

    assert fetch_task_perform("task_id2", "performer_id1") \
        == TaskPerform("performer_id1", "task_id2", 0)
    assert fetch_task_perform("task_id3", "performer_id1") \
        == TaskPerform("performer_id1", "task_id3", 6.2)
    assert fetch_task_perform("task_id4", "performer_id2") \
        == TaskPerform("performer_id2", "task_id4", 50.6)
