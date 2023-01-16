from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseForbidden


def build_bad_request_response(msg: str) -> Response:
    data = {
        'error': msg
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


def build_forbidden_response(msg: str) -> Response:
    return HttpResponseForbidden(msg)

    