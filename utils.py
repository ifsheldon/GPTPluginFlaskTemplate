import logging

from flask import abort, request

logger = logging.getLogger("backend_functions")
TEMP_AUTH_CODE = "hello"


def check_request_json(*required_json_field: str):
    if request.is_json:
        try:
            request_json = request.get_json()
            for field in required_json_field:
                if field not in request_json:
                    logger.warning(request_json)
                    abort(400, "无效 JSON")
            return request_json
        except Exception as e:
            abort(400, f"请求体必须是有效 JSON: {e}")
    else:
        logger.warning(request.data)
        abort(400, "请求体必须是 JSON")


def require_authorization(view_function):
    function_name = view_function.__name__

    def decorated_function(*args, **kwargs):
        has_auth = 'Authorization' in request.headers
        if has_auth:
            auth_header = request.headers.get('Authorization')
            token_type, _, auth_code = auth_header.partition(' ')
            if token_type == 'Bearer' and auth_code == TEMP_AUTH_CODE:
                return view_function(*args, **kwargs)
            else:
                logger.warning(f"Accessing {function_name} - Invalid Authorization: {auth_header}")
                abort(401)
        else:
            logger.warning(f"Accessing {function_name} - Missing Authorization in headers")
            abort(401)

    decorated_function.__name__ = function_name  # needed because Flask register functions by name (I guess)
    return decorated_function
