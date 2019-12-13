import os


def set_log_permission(file, permission):
	os.chmod(file, permission)

def close_log_w_permission(file, permission):
	f = file.name
	file.close()
	os.chmod(f, 1)
