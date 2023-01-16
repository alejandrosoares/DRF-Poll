from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AnonymousUser

from utils.views.response.builder import build_forbidden_response
from utils.helpers import convert_queryset_to_list_id
from .permission import Role


class InvalidAuthorizationHeader(Exception):
    pass


class RetrieveUser:
    HEADER = 'Authorization'
    KEYWORD = TokenAuthentication.keyword

    def __get_auth_header(headers):
        auth_header = headers.get(RetrieveUser.HEADER, None)
        if auth_header is None:
            raise InvalidAuthorizationHeader()
        return auth_header

    def __validate_keyword(keyword):
        if keyword != RetrieveUser.KEYWORD:
            raise InvalidAuthorizationHeader()
            
    def __get_valid_token(auth_header):
        try:
            pair = auth_header.split()
            keyword = pair[0]
            token = pair[1]
            RetrieveUser.__validate_keyword(keyword)
        except IndexError:
            raise InvalidAuthorizationHeader()
        return token
        
    def __get_token_from(headers):
        auth_header = RetrieveUser.__get_auth_header(headers)
        token = RetrieveUser.__get_valid_token(auth_header)
        return token

    def __get_user_by(token):
        try:
            user_token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise InvalidAuthorizationHeader()
        return user_token.user

    @staticmethod
    def get_user_by_token(headers):
        try:
            token = RetrieveUser.__get_token_from(headers)
            user = RetrieveUser.__get_user_by(token)
        except InvalidAuthorizationHeader:
            user = None
        return user


class RoleDecorator:
    
    FORBIDDEN = 'You do not have permissions to perfom this action.'

    def __is_not_anonymous(user):
        return (
            not isinstance(user, AnonymousUser) 
            and user is not None
        )

    def __get_all_user_role(user):
        return user.groups.all()

    def __check_match(roles, user_roles):
        user_roles_id = convert_queryset_to_list_id(user_roles)
        for role in roles:
            if role in user_roles_id:
                return True
        return False

    def __has_some_role(user, roles):
        user_roles = RoleDecorator.__get_all_user_role(user)
        match = RoleDecorator.__check_match(roles, user_roles)
        return match
    
    def __get_headers_from_args(args):
        pos_request = 0
        request = args[pos_request]
        headers = request.headers
        return headers

    @staticmethod
    def get_response_by_role(fn, roles, *args, **kwargs):
        headers = RoleDecorator.__get_headers_from_args(args)
        user = RetrieveUser.get_user_by_token(headers)
        if (
            RoleDecorator.__is_not_anonymous(user) 
            and RoleDecorator.__has_some_role(user, roles)
        ):
            return fn(*args, **kwargs)
        return build_forbidden_response(RoleDecorator.FORBIDDEN)


def admin_role(fn):
    
    def wrapper(*args, **kwargs):
        return RoleDecorator.get_response_by_role(
            fn,
            [Role.ADMIN],
            *args,
            **kwargs
        )

    return wrapper


def pollster_role(fn):
    
    def wrapper(*args, **kwargs):
        return RoleDecorator.get_response_by_role(
            fn,
            [Role.POLLSTER],
            *args,
            **kwargs
        )

    return wrapper


def pollee_role(fn):
    
    def wrapper(*args, **kwargs):
        return RoleDecorator.get_response_by_role(
            fn,
            [Role.POLLEE],
            *args,
            **kwargs
        )

    return wrapper


def admin_pollster_role(fn):
    
    def wrapper(*args, **kwargs):
        return RoleDecorator.get_response_by_role(
            fn,
            [Role.ADMIN, Role.POLLSTER],
            *args,
            **kwargs
        )

    return wrapper