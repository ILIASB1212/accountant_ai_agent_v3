import sys

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = self.get_error_detail_message(error_message, error_details)

    @staticmethod
    def get_error_detail_message(error_message, error_details: sys):
        _, _, exc_tb = error_details.exc_info()
        
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        
        return f"Error file name: {file_name} --Line number: {line_number} -- Error message: {error_message}"
    
    def __str__(self):        
        # FIXED: Return the variable defined in __init__
        return self.error_message