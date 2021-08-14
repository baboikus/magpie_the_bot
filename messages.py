def stop(args):
	return "you have finished work on {task_id}.\n" \
	    "a total of {total_time_spent:1.1f} hours were spent on {task_id}.\n" \
	    "today you spent on {task_id} {sessions_time_spent:1.1f} hours.\n"\
	    "please mark the time spent.".format(**args)