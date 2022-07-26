import logging
import os

os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from src.logger_manager.LoggerManager import LoggerManager

def test_fluentd_logger_send():
	fluentd_tag, host, port = 'bie-fluent-log', 'localhost', 24224
	logger_manager = LoggerManager(logger_name='test-fluentd')
	logger_manager.add_fluentd_logger(fluentd_tag, host, port)

	logger = logger_manager.get_logger()
	logger.info("fluentd test")

	logger_manager.close_logger()

	assert True

def test_line_logger_send():
	line_notify_token = 'sonAjeRj34T7C7f2cTYTWMiYrFHrvrIavaoAj9XXqYT'
	logger_manager = LoggerManager(logger_name='test-line-notify')
	logger_manager.add_line_logger(line_notify_token, level=logging.DEBUG)

	logger = logger_manager.get_logger()
	logger.info("line test")

	logger_manager.close_logger()

	assert True