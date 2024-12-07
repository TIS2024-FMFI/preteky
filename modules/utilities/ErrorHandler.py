class CustomError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.code = error_code
class IsOrieteeringApiError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)