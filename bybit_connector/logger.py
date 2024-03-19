import logging
import configparser


def setup_logger(config_file="logging.ini"):
  """
  Sets up logging configuration based on settings in an INI file.

  Args:
      config_file (str, optional): Path to the INI file containing logging configuration. Defaults to "logging.ini".
  """
  config = configparser.ConfigParser()
  config.read(config_file)

  logging.config.fileConfig(config)


def get_logger(name):
  """
  Retrieves a logger instance with the specified name.

  Args:
      name (str): Name for the logger.

  Returns:
      logging.Logger: An instance of the logger.
  """
  logger = logging.getLogger(name)
  return logger
