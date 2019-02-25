from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _ #whenever we output any msgs in the python code that are gonna be outputted in the screen its good idea to pass them through this translation system,so if we add any new languages to the project we can easily add the language file and it will automatically convert all the texts to the correct language

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): #Serializer for the users object. https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
	
	class Meta:
		model = get_user_model() #specifying the model we want to base the ModelSerializer from
		fields = ('email', 'password', 'name')
		extra_kwargs = {'password': {'write_only':True, 'min_length': 5}} #extra_kwargs allows us to configure few extra settings in our ModelSerializer,here making sure password is write only and more than 5 characters.

	def create(self, validated_data): #create a new user with encrypted password and return it
		return get_user_model().objects.create_user(**validated_data) # ** is used to unwing the validated_data into the parameters of the create_user function . 
																		#validated_data is all the data that was passed in the serializer i.e JSON data made in the http post.


class AuthTokenSerializer(serializers.Serializer): #Serializer for the user authenticate object
	email = serializers.CharField()
	password = serializers.CharField(
		style = { 'input_type': 'password'},
		trim_whitespace=False
	)

	def validate(self, attrs): #Validating and authenticating the user. attrs attribute here is any field that makes up our serializer 
		email = attrs.get('email')
		password = attrs.get('password')

		user = authenticate(
			request = self.context.get('request'),
			username = email,
			password = password
		)
		if not user:
			msg = ('Unable to authenticate with provided credentials')
			raise serializers.ValidationError(msg, code='authentication')

		attrs['user'] = user
		return attrs         #Note when we are overwriting the validate function we must return the values at the end once the validation is successful
