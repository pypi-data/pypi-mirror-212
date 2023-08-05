import sys


class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        _, _, tb = sys.exc_info()
        self.file_name = tb.tb_frame.f_code.co_filename
        self.line_number = tb.tb_lineno

    def __str__(self):
        return f"Error occurred in {self.file_name} at line {self.line_number}: {self.message}"
