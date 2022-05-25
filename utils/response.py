def create_template(context: any = None, message: str = '') -> dict:
    """
    Create a template response.
    """
    default_context = {
        'message': message,
        'data': context if context else {}
    }
    return default_context