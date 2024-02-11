class HttpException(Exception):
    def __init__(self, error, status_code=500):
        super().__init__(error)
        self.status_code = status_code
        self.error = error

    def __str__(self):
        return f"HttpException error for {self.error}: {self.status_code}"