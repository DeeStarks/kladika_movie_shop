from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now create a bew field - 'message' and set it to the error message
    # The custom JSON renderer can only read the message field
    if response is not None:
        response.data['error'] = True
        response.data['message'] = response.data['detail']
    return response