__all__ = ['get_headers', 'get_endpoint']


def get_headers(correlation_id, request_user_id):
    return {
        'CORRELATION_ID': correlation_id,
        'USER_ID': str(request_user_id),
        'Content-Type': "application/json",
    }


def get_endpoint(endpoint, host, port):
    return 'http://{host}:{port}/{endpoint}'.format(host=host, port=port, endpoint=endpoint)
