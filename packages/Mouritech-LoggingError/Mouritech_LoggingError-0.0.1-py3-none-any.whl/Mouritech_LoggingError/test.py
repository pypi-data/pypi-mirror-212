import logging
from File_Errors import LoggerDemoConsole
# Create a logger
logger = logging.getLogger("fileerrors:")
logger.setLevel(logging.ERROR)

# Define a custom error handler
class LoggerDemoConsoleHandler(logging.Handler):
    def emit(self, record):
        if isinstance(record.exc_info[1], LoggerDemoConsole):
            print(f"Custom Error: {record.msg}")
            

# Add the custom error handler to the logger
logger.addHandler(LoggerDemoConsoleHandler())
