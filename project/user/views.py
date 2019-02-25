from rest_framework import generics, authentication, permissions #https://www.django-rest-framework.org/api-guide/generic-views/
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView): #create a new user in the app

    serializer_class = UserSerializer  #as DRF makes it really easy to create Apis that do standard behavior like creating objects in the database using generics.


class CreateTokenView(ObtainAuthToken): #Create a new auth token for user
    serializer_class = AuthTokenSerializer
    # Use default renderer classes so we have a browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView): #Manage the authenticated user
    serializer_class = UserSerializer

    # Add class vars for authentication and permission
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # Add a get_object() function to just return the user that's authenticated
    def get_object(self):
        return self.request.user