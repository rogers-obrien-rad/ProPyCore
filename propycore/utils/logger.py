import logging
import pathlib

def setup(log_file_name, level="info", stream=False):
    """
    Creates a logging object
    
    Parameters
    ----------
    log_file_name : str
        how to name the log file
    level : str, default "info"
        the logging level to display messages
    stream : boolean, default False
        whether to include output in a Stream

    Returns
    -------
    logger : logging object
        a logger to debug
    """
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Clearing log instances
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create handler
    dir_path = pathlib.Path(__file__).resolve().parent
    f_handler = logging.FileHandler(f'{dir_path}/{log_file_name}.log',mode='w')

    # Set level
    if level.lower() == "debug":
        log_level = logging.DEBUG
    else: # default to info
        log_level = logging.INFO

    logging.getLogger().setLevel(log_level)

    # Create formatter and add it to handler
    f_format = logging.Formatter('%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')
    f_handler.setFormatter(f_format)

    # Add handler to the logger
    logger.addHandler(f_handler)

    if stream:
        # repeat the above steps but for a StreamHandler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(log_level)
        c_format = logging.Formatter('%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

    return logger