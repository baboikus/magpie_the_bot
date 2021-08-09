from enum import Enum
from threading import Timer, Lock

BACKLOG = {}
TASK_PERFORM_LOG = {}
SESSIONS = {}
EVENTS_LOG = {}

EVIROMENT_MUTEX = Lock()

def clear_enviroment():
	EVIROMENT_MUTEX.acquire(1)

	BACKLOG.clear()
	TASK_PERFORM_LOG.clear()
	SESSIONS.clear()
	EVENTS_LOG.clear()

	EVIROMENT_MUTEX.release()

def update_enviroment_loop():
  Timer(60.0, update_enviroment_loop).start()
  run_time_machine(1.0 / 60.0)

def run_time_machine(hours):
	if hours <= 0: return

	EVIROMENT_MUTEX.acquire(1)

	in_progress = set()
	for task in BACKLOG.values():
		if task.status == TaskStatus.IN_PROGRESS: in_progress.add(task.task_id)

	for perform_id in TASK_PERFORM_LOG.keys():
		if perform_id[1] in in_progress:
			perform = TASK_PERFORM_LOG[perform_id]
			if perform.performer_id in SESSIONS[perform.task_id]: 
				perform.total_time_spent += hours
				perform.sessions_time_spent[-1] += hours

	EVIROMENT_MUTEX.release()

class TaskStatus(Enum):
	UNKNOWN = 1
	NEW = 2
	IN_PROGRESS = 3
	SUSPENDED = 4
	COMPLETE = 5

class Task:
	def __init__(self, task_id, tags, status):
		self.task_id = task_id
		self.tags = tags
		self.status = status
		BACKLOG[task_id] = self


	def __eq__(self, other):
		return self.task_id == other.task_id \
			   and self.tags == other.tags \
			   and self.status == other.status


	def __repr__(self): 
		return "Task id:% s tags:% s status:% s" % (self.task_id, self.tags, self.status)


	def tags_str(self):
		s = ""
		tags = list(self.tags)
		tags.sort()
		if len(tags) > 0: s += tags[0]
		for tag in tags[1:]: s += ", % s" % tag
		return s


class TaskPerform:
	def __init__(self, performer_id, task_id, total_time_spent, sessions_time_spent = None ):
		self.performer_id = performer_id
		self.task_id = task_id
		self.total_time_spent = total_time_spent
		if sessions_time_spent is None: self.sessions_time_spent = [total_time_spent]
		else: self.sessions_time_spent = sessions_time_spent
		TASK_PERFORM_LOG[(performer_id, task_id)] = self


	def __repr__(self): 
		return "TaskPerform performer_id:% s task_id:% s total_time_spent:% s sessions_time_spent: % s" \
			   % (self.performer_id, self.task_id, self.total_time_spent, self.sessions_time_spent)


	def __eq__(self, other):
		return self.performer_id == other.performer_id \
			   and self.task_id == other.task_id \
			   and self.total_time_spent == other.total_time_spent \
			   and self.sessions_time_spent == other.sessions_time_spent




