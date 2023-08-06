import logging
import time

class PerformanceLogger:
    def __init__(self, logger_name, log_level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler = logging.StreamHandler()
        self.handler.setLevel(log_level)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_performance(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            self.logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
            return result
        return wrapper

