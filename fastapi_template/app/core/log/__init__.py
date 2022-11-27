from starlette.requests import Request


def create_request_id(request: Request):
    """Create a request-id baed on the attributes of the passed request.
    Parameters:
        request: the request to create the id for.
    Returns:
        the request-id.
    """
    return abs(hash(f'{request.client}{request.headers}{request.body}'))
