from task import BACKLOG, TASK_PERFORM_LOG, clear_enviroment, Task, TaskStatus, TaskPerform 
from magpie import Magpie


# def test_error():
# 	clear_enviroment()
# 	magpie = Magpie()

# 	response = magpie.request("")

# 	assert response == "error occurred. use '/help' for list of avaible commands."


def test_unknown_command():
	clear_enviroment()
	magpie = Magpie()

	response = magpie.request("task_add task99 tag256")

	assert response == "unknown command 'task_add'. use '/help' for list of avaible commands."


def test_help():
	clear_enviroment()
	magpie = Magpie()

	response = magpie.request("/help")

	assert response == "avaible commands:\n/add_task\n/backlog\n/help"	


def test_add_task1():
	clear_enviroment()
	magpie = Magpie()

	assert len(BACKLOG) == 0

	response = magpie.request("/task_add task42")

	assert response == "task42 has been added."
	assert len(BACKLOG) == 1
	assert BACKLOG["task42"] == Task("task42", set(), TaskStatus.NEW)


def test_add_task2():
	clear_enviroment()
	magpie = Magpie()

	assert len(BACKLOG) == 0

	response = magpie.request("/task_add task1 tag2 tag1")

	assert response == "task1 has been added. task1 relates to tag1, tag2."
	assert len(BACKLOG) == 1
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2"}, TaskStatus.NEW)


def test_add_tasks1():
	clear_enviroment()
	magpie = Magpie()

	assert len(BACKLOG) == 0

	magpie.request("/task_add task1 tag1 tag2")
	magpie.request("/task_add task2 tag2")

	assert len(BACKLOG) == 2
	assert BACKLOG["task1"] == Task("task1", {"tag1", "tag2"}, TaskStatus.NEW)
	assert BACKLOG["task2"] == Task("task2", {"tag2"}, TaskStatus.NEW)


def test_backlog():
	clear_enviroment()
	magpie = Magpie()

	response = magpie.request("/backlog")

	assert response == "backlog is empty."

	magpie.request("/task_add task1 tag1 tag2")
	response = magpie.request("/backlog")

	assert response == "backlog:\ntask1: tag1, tag2"

	magpie.request("/task_add task2 tag3")
	magpie.request("/task_add task3 tag1 tag3")
	response = magpie.request("/backlog")	

	assert len(BACKLOG) == 3
	assert response == "backlog:\ntask1: tag1, tag2\ntask2: tag3\ntask3: tag1, tag3"











