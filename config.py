import sys
import utilities.utilities as utils

# Get utilities
try:
    utils.clean_logger()
    config_object = utils.read_config()
    global_logger = utils.configure_logger()
except Exception as e:
    print(e, file=sys.stderr)
    exit()

if not config_object:
    global_logger.critical("[CRITICAL]: Config file not found")
    exit()