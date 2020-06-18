from functools import wraps

from mylogger import logger_api_caller

def apicalllog(func):
    @wraps(func)
    # def inner(*args, **kargs):
    def inner(url):
        logger_api_caller.info(url)
        response = func(url)
        logger_api_caller.info(response)
        logger_api_caller.info(response.json())
        return response
    return inner

