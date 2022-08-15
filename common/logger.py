import os
import logging
import logging.handlers

LOG_EXT = ".log"
BASE_DIR = './logs'

def create_logger(log_filename, log_dir=BASE_DIR, level='info'):
    # Create log path
    create_directory(log_dir)

    # Create logger instance
    logger = logging.getLogger()

    # Create formatter
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

    # Create handler (stream, file)
    streamHandler = logging.StreamHandler()
    fileHandler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(log_dir, log_filename + LOG_EXT),
                                                            when='midnight', interval=1, encoding='utf-8')

    # Set logger instance fomatter
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # Set logger instance handler
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.suffix = "%Y%m%d"

    # Set logger instnace log
    logger.setLevel(level=logger_level(level))

    return logging.getLogger(__name__)


# Create log diretory
def create_directory(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


# Custom set log level
def logger_level(level):
    return {
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }.get(level, 'info')