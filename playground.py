def init_command_list():
	return [
		"/task_add speed_up_form_response sql ui html optimize",
		"/task_add change_ok_button_color ui html",
		"/task_add refactor_login_system refactoring backend js",
		"/task_add move_build_scripts git npm"
	]


def init(magpie):
	magpie.request_list("playground", init_command_list())