import traceback
from common.custom_exceptions import HttpException
from rest_framework.response import Response
from rest_framework import status

def return_success_response(response):
    response["is_success"] = True
    response["status_code"] = status.HTTP_200_OK
    return Response(response)

def return_failure_response(exc, status_code=status.HTTP_400_BAD_REQUEST):
    _status_code = status_code
    error_msg = exc.error if hasattr(exc, "error") else exc
    error_dict = {
        "error": error_msg,
        "status_code": _status_code,
        "is_success": False,
    }
    return Response(data=error_dict, status=_status_code)

def custom_http_exception_handler(request, exc):
    tb = traceback.format_exc()
    print("traceback: ", tb)
    headers = getattr(exc, "headers", None)

    if isinstance(exc, HttpException): 
        return return_failure_response(exc, status_code=exc.status_code)

    if isinstance(exc, Exception):
        return Response(
            data = {
                "error": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "is_success": False,
            },
            headers=headers,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
