from common.utils import custom_http_exception_handler

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            print("resp: ", response and response.status_code)
        except Exception as exc:
            self.custom_http_exception_handler(request, exc=exc)
        return response

    def custom_http_exception_handler(self, request, exc):
        custom_http_exception_handler(request, exc)
