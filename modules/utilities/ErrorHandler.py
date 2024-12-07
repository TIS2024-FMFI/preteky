class CustomError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.code = error_code
class IuError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
class IsOrieteeringApiError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
class GoogleCalendarServicesError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
class SandbergDatabaseError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
class HandlerError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
