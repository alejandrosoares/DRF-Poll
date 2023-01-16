from rest_framework.exceptions import PermissionDenied

def is_own_or_raise_exception(user_id, creator_id, msg):
    if user_id != creator_id:
        raise PermissionDenied(msg)