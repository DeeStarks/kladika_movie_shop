def create_template(context: any = None, status: bool = True, message: str = '') -> dict:
    """
    Create a template response.
    """
    default_context = {
        'status': status,
        'message': message,
        'data': context
    }
    return default_context