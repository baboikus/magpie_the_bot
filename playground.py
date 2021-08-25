def init_command_list():
	return [
		("manager", "/task_add speed_up_form_response sql ui html optimize"),
		("manager", "/task_add change_ok_button_color ui html"),
		("manager", "/task_add refactor_login_system refactoring backend js"),
		("manager", "/task_add move_build_scripts git npm"),

		("time_master", "/admin_time_machine 2.5"),

		("developer1", "/task_start change_ok_button_color"),
		("time_master", "/admin_time_machine 1.0"),
		("developer1", "/tag_add change_ok_button_color css"),
		("time_master", "/admin_time_machine 0.5"),
		("developer2", "/task_start change_ok_button_color"),
		("time_master", "/admin_time_machine 2.1"),
		("developer1", "/task_stop change_ok_button_color"),
		("time_master", "/admin_time_machine 1.5"),
		("developer2", "/task_stop change_ok_button_color"),
		("developer2", "/task_done change_ok_button_color"),

		("time_master", "/admin_time_machine 3.5"),
		("developer3", "/task_start move_build_scripts"),
		("time_master", "/admin_time_machine 10.5"),
		("developer3", "/task_stop move_build_scripts"),

		("developer1", "/task_start speed_up_form_response"),
		("time_master", "/admin_time_machine 1.0")
	]


def init(magpie):
	for user, command in init_command_list():
		magpie.request(user, command)
