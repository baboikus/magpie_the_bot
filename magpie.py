from task import BACKLOG, TASK_PERFORM_LOG, SESSIONS, EVIROMENT_MUTEX
from task import clear_enviroment, run_time_machine, Task, TaskStatus, TaskPerform

class Magpie:
	def request(self, user, req):
			EVIROMENT_MUTEX.acquire(1)
		#try:
			tokens = req.split()
			command = tokens[0]
			args = tokens[1:]
			
			response = ""
			if command == "/task_add": response = self.__dispatch_task_add(user, args)
			elif command == "/tag_add": response = self.__dispatch_tag_add(user, args)
			elif command == "/backlog": response = self.__dispatch_backlog(user, args)
			elif command == "/events": response = self.__dispatch_events(user, args) 
			elif command == "/start": response = self.__dispatch_start(user, args)
			elif command == "/stop": response = self.__dispatch_stop(user, args)
			elif command == "/help": response = self.__dispatch_help(user, args)

			elif command == "/admin_time_machine":
				EVIROMENT_MUTEX.release()
				hours = float(args[0])
				run_time_machine(hours)
				return "and so % s hours have passed..." % (hours) 

			else: response = self.__dispatch_unknown_command(user, command, args)

			EVIROMENT_MUTEX.release()

			return response

		#except Exception as e:
			#EVIROMENT_MUTEX.release()
			#print(e);
			return "error occurred. use '/help' for list of avaible commands."


	def __dispatch_unknown_command(self, user, command, args):
		return "unknown command '% s'. use '/help' for list of avaible commands." % command


	def __dispatch_task_add(self, user, args):
		task_id = args[0]
		tags = args[1:]

		task = Task(task_id, set(tags), TaskStatus.NEW)

		response = "% s has been added." % (task.task_id)
		if len(task.tags) > 0:
			response += "\n% s relates to % s." % (task.task_id, task.tags_str()) 
		return response


	def __dispatch_backlog(self, user, args):
		if len(BACKLOG) == 0: return "backlog is empty."

		response = "backlog:"
		for task in BACKLOG.values():
			tags = list(task.tags)
			tags.sort()
			response += "\n% s: " % task.task_id
			if len(task.tags) > 0: response += tags[0]
			for tag in tags[1:]: response += ", % s" % tag
		return response


	def __dispatch_help(self, user, args):
		return "avaible commands:\n/add_task\n/backlog\n/help"


	def __dispatch_start(self, user, args):
		task = BACKLOG[args[0]]
		task.status = TaskStatus.IN_PROGRESS

		if not (user, task.task_id) in TASK_PERFORM_LOG: TaskPerform(user, task.task_id, 0, [])
		TASK_PERFORM_LOG[(user, task.task_id)].sessions_time_spent += [0] 

		session = SESSIONS.get(task.task_id, set())
		session.add(user)
		SESSIONS[task.task_id] = session

		return "you started working on %s.\n% s relates to % s." % (task.task_id, task.task_id, task.tags_str())


	def __dispatch_stop(self, user, args):
		task = BACKLOG[args[0]]
		
		total_time_spent = 0
		sessions_time_spent = 0
		for perform_id in TASK_PERFORM_LOG:
			if perform_id[1] == task.task_id:
				perform = TASK_PERFORM_LOG[perform_id] 
				total_time_spent += perform.total_time_spent
				if perform_id[0] == user: sessions_time_spent += perform.sessions_time_spent[-1]

		SESSIONS[task.task_id].remove(user)
		if len(SESSIONS[task.task_id]) == 0:
			del SESSIONS[task.task_id]
			task.status = TaskStatus.SUSPENDED

		return "you have finished work on % s.\n" \
			   "a total of % s hours were spent on % s.\n" \
			   "today you spent on % s % s hours.\n"\
			   "please mark the time spent." \
			   % (task.task_id, total_time_spent, task.task_id, task.task_id, sessions_time_spent)


	def __dispatch_tag_add(self, user, args):
		task_id = args[0]
		tags = set(args[1:])
		task = BACKLOG[task_id]
		task.tags |= tags

		return "tags for % s updated. % s now relates to % s." \
			   % (task.task_id, task.task_id, task.tags_str())


	def __dispatch_events(self, user, args):
		all_tasks = list(BACKLOG.keys())
		all_tasks.sort()

		response = ""
		for task_id in all_tasks:
			task = BACKLOG[task_id]
			total_time_spent = 0
			task_alerts = ""
			for perform_id in TASK_PERFORM_LOG.keys():
				if perform_id[1] == task.task_id:
					perform = TASK_PERFORM_LOG[perform_id]
					total_time_spent += perform.total_time_spent
					for session_time in perform.sessions_time_spent:
						if session_time >= 8: 
							task_alerts += "% s spent % s hours on % s in a single session.\n" \
											% (perform.performer_id, session_time, perform.task_id)

			if total_time_spent > 0:
				response += "events for % s:\n" % (task.task_id)
				response += "a total of % s hours were spent on % s.\n" % (total_time_spent, task.task_id)
				tags_str = task.tags_str()
				if len(tags_str) > 0: response += "% s relates to % s.\n" % (task.task_id, tags_str)
				response += task_alerts
			else: response += "no events for %s.\n" % (task.task_id)
			response += "\n"

		return response






















