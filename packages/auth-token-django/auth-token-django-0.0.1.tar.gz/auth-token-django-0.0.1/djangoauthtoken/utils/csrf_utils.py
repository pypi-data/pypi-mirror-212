from django.middleware import csrf

def get_or_create_csrf_token(request) -> str:
    token = request.META.get('CSRF_COOKIE', None)
    if token is None:
        token = csrf._get_new_csrf_string()
    return token