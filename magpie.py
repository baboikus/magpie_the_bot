from task import TASK_PERFORM_LOG, SESSIONS, EVENTS_LOG, EVENT_HANDLERS
from task import clear_enviroment, run_atomic_state_action, new_event, new_mail, run_time_machine, backlog_len, fetch_task, fetch_all_tasks, fetch_all_tasks_ids
from task import Task, TaskStatus, TaskPerform, EventType
import utils
import messages

def crunch_reminder(perform):
	#TODO сделать одиночную отправку сообщений. сейчас отправка каждые N минут.
	new_mail(perform.performer_id, "⚠️ you are working on % s over 8 hours." % (perform.task_id))


class Magpie:
	def init_default_event_handlers(self):
		EVENT_HANDLERS[EventType.CRUNCH] = crunch_reminder 

	def request(self, user, req):
		try:
			tokens = req.split()
			command = tokens[0]
			args = tokens[1:]

			### admin commands block >>>
			if command == "/admin_time_machine":
				hours = float(args[0])
				run_time_machine(hours)
				return "and so %1.1f hours have passed..." % (hours) 
			elif command == "/admin_botfather_help": return messages.botfather_help()
			### <<< admin commands block 

			def action():
				response = ""
				if command == "/task_add": response = self.__dispatch_task_add(user, args)
				elif command == "/tag_add": response = self.__dispatch_tag_add(user, args)
				elif command == "/backlog": response = self.__dispatch_backlog(user, args)
				elif command == "/events": response = self.__dispatch_events(user, args) 
				elif command == "/task_start": response = self.__dispatch_start(user, args)
				elif command == "/task_stop": response = self.__dispatch_stop(user, args)
				elif command == "/task_done": response = self.__dispatch_done(user, args) 
				elif command == "/help": response = self.__dispatch_help(user, args)
				elif command == "/daily_report" \
					or command == "/weekly_report": response = "there is no implementations for '% s' command. YET." % command
				else: response = self.__dispatch_unknown_command(user, command, args)
				return response

			return run_atomic_state_action(action)

		except Exception as e:
			print(e)
			return "error occurred. use '/help' for list of avaible commands."


	def request_list(self, user, reqs):
		for req in reqs: self.request(user, req)


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
		if backlog_len() == 0: return "backlog is empty."

		#TODO добавить строчку с текущими исполнителями по каждой задаче
		response = "backlog:"
		new_tasks = ""
		new_tasks_counter = 0
		in_progress_tasks = ""
		in_progress_tasks_counter = 0
		done_tasks = ""
		done_tasks_counter = 0

		for task in fetch_all_tasks():
			task_str = "\n% s relates to % s." % (task.task_id, task.tags_str())
			if task.status == TaskStatus.NEW: 
				new_tasks += task_str
				new_tasks_counter += 1
			elif task.status == TaskStatus.IN_PROGRESS: 
				in_progress_tasks += task_str
				in_progress_tasks_counter += 1
			elif task.status == TaskStatus.DONE: 
				done_tasks += task_str
				done_tasks_counter += 1

		if new_tasks_counter > 0:
			response += "\n🐦 NEW(% s):% s" % (new_tasks_counter, new_tasks)
		if in_progress_tasks_counter > 0:
			response += "\n🛠 IN PROGRESS(% s):% s" % (in_progress_tasks_counter, in_progress_tasks)
		if done_tasks_counter > 0: 
			response += "\n✅ DONE(% s):% s" % (done_tasks_counter, done_tasks)

		return response


	def __dispatch_help(self, user, args):
		return messages.help_response()


	def __dispatch_start(self, user, args):
		task = fetch_task(args[0])
		task.status = TaskStatus.IN_PROGRESS

		#TODO добавить эмоджи
		if not (user, task.task_id) in TASK_PERFORM_LOG: TaskPerform(user, task.task_id, 0, [])
		TASK_PERFORM_LOG[(user, task.task_id)].sessions_time_spent += [0] 
		
		session = SESSIONS.get(task.task_id, set())
		who_also_working_on_task_str = ""
		if len(session) > 0: who_also_working_on_task_str = "% s currently working on % s also." % (utils.make_sorted_str(session), task.task_id)
		else: who_also_working_on_task_str = "no one else currently working on % s." % (task.task_id)

		session.add(user)
		SESSIONS[task.task_id] = session

		return "you started working on %s.\n" % (task.task_id) \
			   + "% s relates to % s.\n" % (task.task_id, task.tags_str()) \
			   + who_also_working_on_task_str


	def __dispatch_stop(self, user, args):
		task = fetch_task(args[0])
		
		total_time_spent = 0
		sessions_time_spent = 0
		for perform in TASK_PERFORM_LOG.values():
			if perform.task_id == task.task_id:
				total_time_spent += perform.total_time_spent
				if perform.performer_id == user: sessions_time_spent += perform.sessions_time_spent[-1]

		SESSIONS[task.task_id].remove(user)
		if len(SESSIONS[task.task_id]) == 0:
			del SESSIONS[task.task_id]
			task.status = TaskStatus.SUSPENDED

		return messages.task_stop_response(task.task_id, total_time_spent, sessions_time_spent)


	def __dispatch_done(self, user, args):
		task_id = args[0]
		fetch_task(task_id).status = TaskStatus.DONE

		new_event(task_id, "✅ % s marked task as done." % (user))

		return "you marked % s as done." % (task_id)


	def __dispatch_tag_add(self, user, args):
		task_id = args[0]
		tags = set(args[1:])
		task = fetch_task(task_id)
		task.tags |= tags

		tags = list(tags)
		new_event(task.task_id, 
				  "➕ % s added new tags for task: % s." \
				  % (user, utils.make_sorted_str(tags)))

		return "tags for % s updated. % s now relates to % s." \
			   % (task.task_id, task.task_id, task.tags_str())


	def __crunch_threshold(): return 8.0
	def __dispatch_events(self, user, args):
		all_tasks = list(fetch_all_tasks_ids())
		all_tasks.sort()

		response = ""
		for task_id in all_tasks:
			task = fetch_task(task_id)
			total_time_spent = 0
			task_alerts = ""

			for perform in TASK_PERFORM_LOG.values():
				if perform.task_id == task.task_id:
					total_time_spent += perform.total_time_spent
					for session_time in perform.sessions_time_spent:
						if session_time >= Magpie.__crunch_threshold(): 
							task_alerts += "⚠️ % s spent %1.1f hours on task in a single session.\n" \
											% (perform.performer_id, session_time)

			for event in EVENTS_LOG.get(task.task_id, []):
				task_alerts += event + "\n"

			if total_time_spent > 0 or len(task_alerts) > 0:
				response += "events for % s:\n" % (task.task_id)
				if total_time_spent > 0:
					response += "⏱ " + ("a total of %1.1f hours were spent on task.\n" % (total_time_spent))
				tags_str = task.tags_str()
				if len(tags_str) > 0: response += "ℹ️ task relates to % s.\n" % (tags_str)
				response += task_alerts
			else: response += "no events for %s.\n" % (task.task_id)
			response += "\n"

		return response






















