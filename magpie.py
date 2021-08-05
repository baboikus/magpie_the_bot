from task import BACKLOG, TASK_PERFORM_LOG, clear_enviroment, Task, TaskStatus, TaskPerform

class Magpie:
	def request(self, req):
		#try:
			tokens = req.split()
			command = tokens[0]
			args = tokens[1:]
			
			if command == "/task_add": return self.__dispatch_task_add(args)
			if command == "/backlog": return self.__dispatch_backlog(args)
			if command == "/help": return self.__dispatch_help(args)
			
			return self.__dispatch_unknown_command(command, args)

		#except Exception as e:
			#print(e);
			return "error occurred. use '/help' for list of avaible commands."


	def __dispatch_unknown_command(self, command, args):
		return "unknown command '% s'. use '/help' for list of avaible commands." % command


	def __dispatch_task_add(self, args):
		task_id = args[0]
		tags = args[1:]
		tags.sort()

		Task(task_id, set(tags), TaskStatus.NEW)

		response = "% s has been added." % (task_id)
		if len(tags) > 0:
			response += " % s relates to % s" % (task_id, tags[0])
			for tag in tags[1:]: response += ", % s" % tag
			response += "." 
		return response


	def __dispatch_backlog(self, args):
		if len(BACKLOG) == 0: return "backlog is empty."

		response = "backlog:"
		for task in BACKLOG.values():
			tags = list(task.tags)
			tags.sort()
			response += "\n% s: " % task.task_id
			if len(task.tags) > 0: response += tags[0]
			for tag in tags[1:]: response += ", % s" % tag
		return response


	def __dispatch_help(self, args):
		return "avaible commands:\n/add_task\n/backlog\n/help"





















