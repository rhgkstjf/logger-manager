from logger_manager import LoggerManager

def test_logger_manager():
	line_notify_token = 'sonAjeRj34T7C7f2cTYTWMiYrFHrvrIavaoAj9XXqYT'
	logger_manager = LoggerManager.LoggerManager(logger_name='test-line-notify')
	logger_manager.add_line_logger(line_notify_token, level=10)

	logger = logger_manager.get_logger()
	logger.info("line test")

	logger_manager.close_logger()