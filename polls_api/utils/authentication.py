from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class BasicAuthentication:
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class Meta:
        abstract = True