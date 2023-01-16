from rest_framework.response import Response

from users.models import User

from datetime import datetime

def build_login_response(user: User) -> Response:
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'last_login_date': datetime.now(),
        'token': user.auth_token.key
    }
    return Response(data)