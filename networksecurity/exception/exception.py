import sys
import logging
from networksecurity.logging.logger import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        # _ → ignore exception type
        # _ → ignore exception value
        # exc_tb → traceback object

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in Python script: {self.file_name} at line {self.lineno} with message: {self.error_message}"

if __name__=='__main__':

    try:
        logger.info("enter the try block")
        a=1/0
        print("this will not be printed",a)
    except Exception as e:
        logger.error("an exception occured",exc_info=True)
        raise NetworkSecurityException(e,sys)                