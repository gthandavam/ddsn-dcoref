__author__ = 'gt'


import logging

def setup_custom_logger(name):
  formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

  handler = logging.StreamHandler()
  handler.setFormatter(formatter)

  logger = logging.getLogger(name)
  logger.setLevel(logging.WARN)
  logger.addHandler(handler)
  return logger