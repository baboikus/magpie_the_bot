from task import BACKLOG, TASK_PERFORM_LOG, SESSIONS, clear_enviroment, run_time_machine, Task, TaskStatus, TaskPerform 
from magpie import Magpie

# def test_error():
# 	clear_enviroment()
# 	magpie = Magpie()

# 	response = magpie.request("user1", "")

# 	assert response == "error occurred. use '/help' for list of avaible commands."


def test_unknown_command():
	clear_enviroment()
	magpie = Magpie()

	response = magpie.request("user1", "task_add task99 tag256")

	assert response == "unknown command 'task_add'. use '/help' for list of avaible commands."


def test_help():
	clear_enviroment()
	magpie = Magpie()

	response = magpie.request("user1", "/help")

	assert response == "avaible commands:\n/add_task\n/backlog\n/help"	


def test_add_task1():
	clear_enviroment()
	magpie = Magpie()

	assert len(BACKLOG) == 0

	response = magpie.request("user1", "/task_add task42")

	assert response == "task42 has been added."
	assert len(BACKLOG) == 1
	assert BACKLOG["task42"] == Task("task42", set(), TaskStatus.NEW)


def test_add_task2():
	clear_enviroment()
	magpie = Magpie()

	assert len(BACKLOG) == 0

	response = magpie.request("user1", "/task_add task1 tag2 tag1")

	assert response == "task1 has been added.\ntask1 relates to tag1, tag2."
	assert len(BACKLOG) == 1
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2"}, TaskStatus.NEW)


def test_add_tasks1():
	clear_enviroment()
	magpie = Magpie()

	assert len(BACKLOG) == 0

	magpie.request("user1", "/task_add task1 tag1 tag2")
	magpie.request("user1", "/task_add task2 tag2")

	assert len(BACKLOG) == 2
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2"}, TaskStatus.NEW)
	assert BACKLOG["task2"] == Task("task2", {"tag2"}, TaskStatus.NEW)


def test_backlog():
	clear_enviroment()
	magpie = Magpie()

	response = magpie.request("user1", "/backlog")

	assert response == "backlog is empty."

	magpie.request("user1", "/task_add task1 tag1 tag2")
	response = magpie.request("user1", "/backlog")

	assert response == "backlog:\ntask1: tag1, tag2"

	magpie.request("user1", "/task_add task2 tag3")
	magpie.request("user1", "/task_add task3 tag1 tag3")
	response = magpie.request("user1", "/backlog")	

	assert len(BACKLOG) == 3
	assert response == "backlog:\ntask1: tag1, tag2\ntask2: tag3\ntask3: tag1, tag3"


def test_start_stop_single_user():
	clear_enviroment()
	magpie = Magpie()

	magpie.request("user1", "/task_add task1 tag1 tag2 tag3")

	assert len(TASK_PERFORM_LOG) == 0
	assert len(SESSIONS) == 0

	response = magpie.request("user1", "/start task1")

	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2", "tag3"}, TaskStatus.IN_PROGRESS)
	assert TASK_PERFORM_LOG[("user1", "task1")] == TaskPerform("user1", "task1", 0, [0])
	assert SESSIONS["task1"] == {"user1"}
	assert response == "you started working on task1.\ntask1 relates to tag1, tag2, tag3."

	run_time_machine(4)
	response = magpie.request("user1", "/stop task1")

	assert len(SESSIONS) == 0
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2", "tag3"}, TaskStatus.SUSPENDED)
	assert TASK_PERFORM_LOG[("user1", "task1")] == TaskPerform("user1", "task1", 4, [4])
	assert response == "you have finished work on task1.\n" \
					   "a total of 4.0 hours were spent on task1.\n" \
					   "today you spent on task1 4.0 hours.\n" \
					   "please mark the time spent." 

def test_time_format():
	clear_enviroment()
	magpie = Magpie()

	magpie.request("user1", "/task_add task1 tag1 tag2 tag3")
	magpie.request("user1", "/start task1")
	run_time_machine(0.49)
	response = magpie.request("user1", "/stop task1")

	assert response == "you have finished work on task1.\n" \
				   "a total of 0.5 hours were spent on task1.\n" \
				   "today you spent on task1 0.5 hours.\n" \
				   "please mark the time spent." 


def test_start_stop_many_users():
	clear_enviroment()
	magpie = Magpie()

	assert len(SESSIONS) == 0

	magpie.request("manager", "/task_add task1 tag1 tag2")
	run_time_machine(1)
	magpie.request("developer1", "/start task1")

	assert SESSIONS["task1"] == {"developer1"}

	run_time_machine(2)
	magpie.request("developer2", "/start task1")

	assert SESSIONS["task1"] == {"developer1", "developer2"}

	run_time_machine(3)
	magpie.request("developer1", "/stop task1")

	assert SESSIONS["task1"] == {"developer2"}
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2"}, TaskStatus.IN_PROGRESS)
	assert TASK_PERFORM_LOG[("developer1", "task1")] == TaskPerform("developer1", "task1", 5, [5])
	assert TASK_PERFORM_LOG[("developer2", "task1")] == TaskPerform("developer2", "task1", 3, [3])

	run_time_machine(1)
	magpie.request("developer2", "/stop task1")

	assert len(SESSIONS) == 0
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2"}, TaskStatus.SUSPENDED)
	assert TASK_PERFORM_LOG[("developer1", "task1")] == TaskPerform("developer1", "task1", 5, [5])
	assert TASK_PERFORM_LOG[("developer2", "task1")] == TaskPerform("developer2", "task1", 3 + 1, [3 + 1])		


def test_add_tags():
	clear_enviroment()
	magpie = Magpie()

	magpie.request("manager", "/task_add task1")

	assert len(BACKLOG["task1"].tags) == 0

	response = magpie.request("manager", "/tag_add task1 tag1")

	assert BACKLOG["task1"].tags == {"tag1"}
	assert response == "tags for task1 updated. task1 now relates to tag1."

	response = magpie.request("developer", "/tag_add task1 tag2 tag3")

	assert BACKLOG["task1"].tags == {"tag1", "tag2", "tag3"}
	assert response == "tags for task1 updated. task1 now relates to tag1, tag2, tag3."


def test_events_spent_time():
	clear_enviroment()
	magpie = Magpie()

	magpie.request("manager", "/task_add task1 tag1 tag2")
	magpie.request("manager", "/task_add task2 tag1 tag3")
	magpie.request("developer1", "/start task1")
	run_time_machine(4)
	magpie.request("developer2", "/start task1")
	run_time_machine(5)
	magpie.request("developer1", "/stop task1")
	run_time_machine(1)	
	magpie.request("developer2", "/stop task1")

	response = magpie.request("manager", "/events")

	assert response == "events for task1:\n" \
		   "a total of 15.0 hours were spent on task1.\n" \
		   "task1 relates to tag1, tag2.\n" \
		   "developer1 spent 9.0 hours on task1 in a single session.\n" \
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
		   "task1 relates to tag1, tag2, tag3.\n" \
		   "developer1 added new tags for task1: tag3.\n" \
		   "\n" \


















