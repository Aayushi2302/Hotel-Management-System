"""Module containing decorator for handling all types of exception of project."""
from functools import wraps
import logging
import sqlite3

from config.prompts import Prompts

logger = logging.getLogger(__name__)

def error_handler(func):
    """
        Decorator function for handling all types of exception happening in project.
        Parameter : function
        Return type : None
    """
    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        """
            Wrapper function for executing the function and raising exception whenever occur.
            Parameter : *args: tuple, **kwargs: dict
            Return type : None
        """
        try:
            return func(*args, **kwargs)
        except sqlite3.IntegrityError as error:
            logger.exception(error)
            print(Prompts.INTEGRITY_ERROR_MESSAGE + "\n")
        except sqlite3.OperationalError as error:
            logger.exception(error)
            print(Prompts.OPERATIONAL_ERROR_MESSAGE + "\n")
        except sqlite3.ProgrammingError as error:
            logger.exception(error)
            print(Prompts.PROGRAMMING_ERROR_MESSAGE + "\n")
        except sqlite3.Error as error:
            logger.exception(error)
            print(Prompts.GENERAL_EXCEPTION_MESSAGE + "\n")
        except ValueError as error:
            logger.exception(error)
            print(Prompts.INVALID_INPUT + "\n")
        except TypeError as error:
            logger.exception(error)
            print(Prompts.INVALID_INPUT + "\n")
        except Exception as error:
            logger.exception(error)
            print(Prompts.GENERAL_EXCEPTION_MESSAGE + "\n")
    return wrapper