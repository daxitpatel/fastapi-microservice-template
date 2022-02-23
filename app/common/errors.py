__all__ = ['errors']

errors = {
    'Exception': {
        'ok': False,
        'error': 'SERVER_ERROR',
        'message': "Something went wrong while processing this request",
        'status': 500,
    },
    'InternalServerException': {
        'ok': False,
        'error': 'SERVER_ERROR',
        'message': "WotNot service is down. Please try again after some time!",
        'status': 500
    },
    'BadRequestError': {
        'ok': False,
        'error': 'BAD_REQUEST',
        'message': "",
        'status': 400
    },
    'BadMessageErrorException': {
        'ok': False,
        'error': 'BAD_REQUEST',
        'message': "",
        'status': 400
    }
}
