COMMANDS = [
	("events", "", "show important events", "show all important performers and tasks events."),
	("daily_report", "", "show daily report", "show daily report describing probable risks and predictive analytics."),
	("help", "", "show command description", "show full description for complete list of commands."),
	("backlog", "", "show current backlog", "show current backlog."),

	("task_add", "<task_id> [<tag1> ... <tagN>]", "", "add task <task_id> with specific tags <tag1>, ... , <tagN> to current backlog."),
	("task_start", "<task_id>", "", "start new working session on the task <task_id>."),
	("task_stop", "<task_id>", "", "stop current working session on the task <task_id>."),

	("tag_add", "<task_id> [<tag1> ... <tagN>]", "", "add set of tags <tag1>, ... , <tagN> to task <task_id>.")
]

def help_response():
	response = "avaible commands:\n"
	for command, args, _, full_description in COMMANDS:
		response += "/% s % s - % s\n" % (command, args, full_description)
	return response

def botfather_help():
	response = ""
	for command, args, short_description, _ in COMMANDS:
		if args == "": response += "% s % s - % s\n" % (command, args, short_description)
	return response	


def task_stop_response(task_id, total_time_spent, sessions_time_spent):
	return "you have finished work on {task_id}.\n" \
	    "a total of {total_time_spent:1.1f} hours were spent on {task_id}.\n" \
	    "today you spent on {task_id} {sessions_time_spent:1.1f} hours.\n"\
	    "please mark the time spent." \
	    .format(task_id = task_id, total_time_spent = total_time_spent, sessions_time_spent = sessions_time_spent)


