"""
Views for user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, CreateAuthToken


class CreateUserView(generics.CreateAPIView):
    """create a new user in DB"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create token for user"""
    serializer_class = CreateAuthToken
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """retrieve or update user profile"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve & return the autheticated user"""
        return self.request.user
