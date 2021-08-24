from task import (BACKLOG, SESSIONS, TASK_PERFORM_LOG, Task, TaskPerform,
                  TaskStatus, clear_enviroment, run_time_machine)


def test_time_machine():
	clear_enviroment()

	Task("task_id1", {}, TaskStatus.IN_PROGRESS)
	Task("task_id2", {}, TaskStatus.NEW)
	Task("task_id3", {}, TaskStatus.SUSPENDED)
	Task("task_id4", {}, TaskStatus.DONE)

	TaskPerform("performer_id1", "task_id1", 2)
	TaskPerform("performer_id2", "task_id1", 0)

	SESSIONS["task_id1"] = {"performer_id1", "performer_id2"}

	TaskPerform("performer_id1", "task_id2", 0)
	TaskPerform("performer_id1", "task_id3", 6.2)
	TaskPerform("performer_id2", "task_id4", 50.6)

	assert TASK_PERFORM_LOG[("performer_id1", "task_id1")] \
		   == TaskPerform("performer_id1", "task_id1", 2)
	assert TASK_PERFORM_LOG[("performer_id2", "task_id1")] \
	       == TaskPerform("performer_id2", "task_id1", 0)

	run_time_machine(12.5)

	assert TASK_PERFORM_LOG[("performer_id1", "task_id1")] \
		   == TaskPerform("performer_id1", "task_id1", 2 + 12.5, [2 + 12.5])
	assert TASK_PERFORM_LOG[("performer_id2", "task_id1")] \
	       == TaskPerform("performer_id2", "task_id1", 0 + 12.5, [12.5])

	assert TASK_PERFORM_LOG[("performer_id1", "task_id2")] \
		   == TaskPerform("performer_id1", "task_id2", 0)
	assert TASK_PERFORM_LOG[("performer_id1", "task_id3")] \
		   == TaskPerform("performer_id1", "task_id3", 6.2)
	assert TASK_PERFORM_LOG[("performer_id2", "task_id4")] \
		   == TaskPerform("performer_id2", "task_id4", 50.6)














