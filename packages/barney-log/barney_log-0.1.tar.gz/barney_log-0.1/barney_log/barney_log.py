import datetime
import logging
import sys
import os

# define to get abosolute path of the current script
def get_current_script_path():
    return os.path.abspath(__file__)
    # end get current script path function

# define to get abosolute path of the current script directory
def get_current_script_directory():
    return os.path.dirname(os.path.abspath(__file__))
    # end get current script directory function

# define console log function with timestamp and track level
def console_log(message, level):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {level} - {message}")
    
    # define log file name and directory with date
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = f'{get_current_script_directory()}/log/output_{date_str}.log'
    log_dir = os.path.dirname(file_name)
    
    # check if log directory exists, create it if it doesn't
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # check if log file exists, create it if it doesn't
    if not os.path.exists(file_name):
        open(file_name, 'w').close()

    # check if level is INFO, else if level is ERROR
    if level == "INFO":
        logging.basicConfig(filename=file_name, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        logging.info(message)
    elif level == "ERROR":
        logging.basicConfig(filename=file_name, level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')
        logging.error(message)
    # end console log function

# define console info function with timestamp
def console_info(message):
    console_log(message, "INFO")
    # end console info function

# define console error function with timestamp
def console_error(message):
    console_log(message, "ERROR")
    # end console error function

# define console debug function with timestamp
def console_debug(message):
    # Check for command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        console_log(message, "DEBUG")
    # end console debug function