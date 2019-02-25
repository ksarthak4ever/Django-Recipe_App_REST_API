from rest_framework import generics #https://www.django-rest-framework.org/api-guide/generic-views/
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView): #Create a new user in the app
	
	serializer_class = UserSerializer #as DRF makes it really easy to create Apis that do standard behavior like creating objects in the database using generics.


class CreateTokenView(ObtainAuthToken): #Create a new auth token for user
	serializer_class = AuthTokenSerializer
	render_classes = api_settings.DEFAULT_RENDERER_CLASSES #what render_classes is doing is it sets the renderer so we can view this endpoint in the browser with the browser API i.e we can login using chrome and type username and password and hit post and it should return a token.
															#If we dont do it then we might have to use some tool such as see url to make http post request