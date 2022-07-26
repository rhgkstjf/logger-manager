import json
import logging
import socket
import requests

from fluent import asynchandler, sender, handler
from urllib3 import Retry
from functools import partial, partialmethod

class LoggerManager:
	"""
	Logging Reference
	https://docs.python.org/ko/3/howto/logging.html
	https://docs.python.org/3/library/logging.handlers.html#httphandler
	"""
	def __init__(self, logger_name, level=logging.DEBUG):

		logging.NOTICE = 25
		logging.addLevelName(logging.NOTICE, 'NOTICE')
		logging.Logger.notice = partialmethod(logging.Logger.log, logging.NOTICE)
		logging.notice = partial(logging.log, logging.NOTICE)

		self.logger=logging.getLogger(logger_name)
		self.logger.setLevel(level)
		self.custom_handlers=[]
		self.custom_format = {
			'host': socket.gethostname(),
			'pid': '%(process)d',
			'datetime': '%(asctime)s',
			'where': '%(module)s.%(funcName)s',
			'lineno': '%(lineno)d',
			'type': '%(levelname)s',
			'message': '%(message)s',
		}
		logging.basicConfig(format=json.dumps(self.custom_format))

	def add_fluentd_logger(self, tag, host, port, level=logging.DEBUG):
		"""
		https://docs.fluentd.org/v/0.12/articles/python
		https://github.com/fluent/fluent-logger-python
		:param tag: str
		:param host: str
		:param port: str
		:param level: int | str
		:return:
		"""
		fluentd_format = {
			'host': socket.gethostname(),
			'pid': '%(process)d',
			'datetime': '%(asctime)s',
			'where': '%(module)s.%(funcName)s',
			'lineno': '%(lineno)d',
			'type': '%(levelname)s',
		}

		# check fluentd connect
		fluentd_sender = sender.FluentSender(tag, host=host, port=port)
		if not fluentd_sender.emit('connect-test', {'': ''}):
			raise ConnectionError("fluentd not connect")
		fluentd_sender.close()

		fluentd_handler = asynchandler.FluentHandler(tag, host=host, port=port)
		formatter = handler.FluentRecordFormatter(fluentd_format)
		fluentd_handler.setFormatter(formatter)
		fluentd_handler.setLevel(level)
		self.logger.addHandler(fluentd_handler)
		self.custom_handlers.append(fluentd_handler)


	def add_line_logger(self, token, level=logging.DEBUG):
		"""
		https://developers.line.biz/en/reference/messaging-api/#status-codes
		:param token: str
		:param level: int | str
		:return:
		"""
		url = "https://notify-api.line.me/api/notify"
		line_handler = CustomHttpHandler(url=url, token=token, level=level)
		formatter = logging.Formatter(json.dumps(self.custom_format))
		line_handler.setFormatter(formatter)
		self.logger.addHandler(line_handler)
		self.custom_handlers.append(line_handler)

	def get_logger(self):
		return self.logger

	def close_logger(self):
		[ custom_handler.close() for custom_handler in self.custom_handlers ]



class CustomHttpHandler(logging.Handler):
	def __init__(self, url, token, level, max_pool_size=1):
		super().__init__(level=level)
		self.url=url
		self.token=token
		self.max_pool_size = max_pool_size
		self.session = requests.Session()
		self.session.headers.update({
            'Authorization': 'Bearer %s' % self.token
		})

		self.session.mount('https://', requests.adapters.HTTPAdapter(
			max_retries=Retry(
				total=5,
				backoff_factor=0.5,
				status_forcelist=[500]
			),
			pool_connections=self.max_pool_size,
			pool_maxsize=self.max_pool_size
		))

	def emit(self, record):
		log_entry = json.loads(self.format(record))
		log_entry = json.dumps(log_entry, indent=4)
		response = self.session.post(self.url, params={'message': log_entry})

		if response.status_code != 200:
			raise ConnectionError(response.reason)

	def close(self):
		self.session.close()
