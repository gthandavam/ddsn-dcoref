__author__ = 'gt'


import logging

def setup_custom_logger(name):
  # formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
  #using line number in the log message
  formatter = logging.Formatter(fmt='%(levelname)s - %(module)s - %(message)s - %(lineno)d')

  handler = logging.StreamHandler()
  handler.setFormatter(formatter)

  logger = logging.getLogger(name)

  #enable a few log messages
  # logger.setLevel(logging.WARN)

  #suppress log messages
  logger.setLevel(logging.ERROR)

  logger.addHandler(handler)
  return logger