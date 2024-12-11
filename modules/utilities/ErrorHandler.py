class CustomError(Exception):
    def __init__(self, message, error_code=None):
        self.message = message
        self.code = error_code
        self.name = 'CustomError'
    def __str__(self):
        return f'{self.name}: {self.code} {self.message}'
    def __repr__(self):
        return f'{self.name}: {self.code} {self.message}'


class IuError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
        self.name = 'IuError'


class IsOrieteeringApiError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
        self.name = 'IsOrieteeringApiError'

class GoogleCalendarServicesError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
        self.name = 'GoogleCalendarServicesError'

class SandbergDatabaseError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
        self.name = 'SandbergDatabaseError'

class HandlerError(CustomError):
    def __init__(self, message, error_code=None):
        super().__init__(message, error_code)
        self.name = 'HandlerError'






