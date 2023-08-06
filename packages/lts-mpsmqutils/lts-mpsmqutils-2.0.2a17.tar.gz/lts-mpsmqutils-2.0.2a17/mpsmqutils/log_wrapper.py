import os

class LogWrapper():
	def init(self):
		print("log_wrapper - init")
		configured_log_level = os.getenv('APP_LOG_LEVEL', 'INFO')
		if configured_log_level == 'DEBUG':
			print("log_wrapper - set debug")
			self.log_level = 0
		elif configured_log_level == 'INFO':
			print("log_wrapper - set info")
			self.log_level = 1
		elif configured_log_level == 'WARNING':
			print("log_wrapper - set warning")
			self.log_level = 2
		elif configured_log_level == 'ERROR':
			print("log_wrapper - set error")
			self.log_level = 3
		else:
			# if configured wrong, we default to info
			print("log_wrapper - set default (info)")
			print("log level configured incorrectly, defaulting to INFO")
			self.log_level = 1

	def debug(self, message):
		if self.log_level <= 0:
			print(message)

	def info(self, message):
		if self.log_level <= 1:
			print(message)

	def warning(self, message):
		if self.log_level <= 2:
			print(message)

	def error(self, message):
		if self.log_level <= 3:
			print(message)
