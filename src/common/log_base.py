import logging


class BaseLogger:
	def __init__(self, name, log_file='default.log', level=logging.INFO):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(level)
		self._setup_console_handler()
		self._setup_file_handler(log_file)

	def _setup_console_handler(self):
		console_handler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		console_handler.setFormatter(console_format)
		self.logger.addHandler(console_handler)

	def _setup_file_handler(self, log_file):
		file_handler = logging.FileHandler(log_file)
		file_handler.setLevel(logging.DEBUG)
		file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		file_handler.setFormatter(file_format)
		self.logger.addHandler(file_handler)

	def debug(self, message):
		self.logger.debug(message)

	def info(self, message):
		self.logger.info(message)

	def warning(self, message):
		self.logger.warning(message)

	def error(self, message):
		self.logger.error(message)

	def critical(self, message):
		self.logger.critical(message)


if __name__ == '__main__':
	logger = BaseLogger(name='ConvertRedis', log_file='convert_redis.log')
	logger.debug('This is a debug message')
