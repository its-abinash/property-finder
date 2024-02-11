class ValidationError(Exception):
    # Indicates an error validating data
    def __init__(self, error, status_code=400):
        super().__init__(error)  
        self.error = error
        self.status_code = status_code

    def __str__(self):
        return f"Validation error for {self.error}: {self.status_code}"


class InsufficientDataException(ValueError):
    """
    Exception raised when there is insufficient data.
    """

    def __init__(self,error="Insufficient data provided.", status_code=400):
        super().__init__(error)
        self.status_code = status_code 
        self.error = error

    def __str__(self):
        return f"InsufficientDataException error for {self.error}: {self.status_code}"


class HttpException(Exception):
    def __init__(self, error, status_code=500):
        super().__init__(error)
        self.status_code = status_code
        self.error = error

    def __str__(self):
        return f"HttpException error for {self.error}: {self.status_code}"


class TimeoutException(Exception):
    def __init__(self, error, status_code=504):
        super().__init__(error)
        self.status_code = status_code
        self.error = error

    def __str__(self):
        return f"TimeoutException error for {self.error}: {self.status_code}"
