import logging
import sys

def setup_logger() -> logging.Logger:
	logger = logging.getLogger(__name__)
	logger.propagate = False

	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.DEBUG)
	stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)
	logger.addHandler(stdout_handler)

	stderr_handler = logging.StreamHandler(sys.stderr)
	stderr_handler.setLevel(logging.DEBUG)
	stderr_handler.addFilter(lambda r: r.levelno >= logging.WARNING)
	logger.addHandler(stderr_handler)
	logger.setLevel(logging.DEBUG)

	return logger