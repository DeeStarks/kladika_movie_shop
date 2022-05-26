def create_template(context: any = None, status: bool = True, message: str = '') -> dict:
    """
    Create a template response.
    """
    default_context = {
        'status': status,
        'message': message,
    }
    if status:
        default_context['data'] = context
    else:
        default_context['errors'] = context
    return default_context