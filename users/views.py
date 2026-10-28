from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from healthcare.helper import error
from .serializers import RegisterSerializer


def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


# POST /api/auth/register/
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # tokens included so the user is logged in right after registering
    return Response({"user": serializer.data, **tokens_for(user)}, status=status.HTTP_201_CREATED)


# POST /api/auth/login/
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return error("email and password are required", status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)
    if user is None:
        # same message for unknown email and wrong password
        return error("invalid credentials", status.HTTP_401_UNAUTHORIZED)

    return Response(tokens_for(user))
