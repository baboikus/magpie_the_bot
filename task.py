from enum import Enum

BACKLOG = {}
TASK_PERFORM_LOG = {}
EVENTS_LOG = {}

def clear_enviroment():
	BACKLOG.clear()
	TASK_PERFORM_LOG.clear()

class TaskStatus(Enum):
	UNKNOWN = 1
	NEW = 2
	IN_PROGRESS = 3
	COMPLETE = 4

class Task:
	def __init__(self, task_id, tags, status):
		self.task_id = task_id
		self.tags = tags
		self.status = status
		BACKLOG[task_id] = self

	def __eq__(self, other):
		return self.task_id == other.task_id and self.tags == other.tags and self.status == other.status

	def __repr__(self): 
		return "Task id:% s tags:% s status:% s" % (self.task_id, self.tags, self.status)

class TaskPerform:
	def __init__(self, performer_id, task_id, time_spent):
		self.performer_id = performer_id
		self.task_id = task_id
		self.time_spent = time_spent
		TASK_PERFORM_LOG[(performer_id, task_id)] = self