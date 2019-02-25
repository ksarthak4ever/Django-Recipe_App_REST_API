from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _ # for outputting messages to screen. Supports multiple languages

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): #Serializer for the user object # Create a new serializer that inherits from ModelSerializer

    class Meta:
        model = get_user_model() #specifying the model we want to base the ModelSerializer from
        fields = ('email', 'password', 'name') # Specify the fields to include in the serializer. These are the fields that will be converted to/from JSON when make our HTTP POST,retrieve in our view, then save to our model
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} #extra_kwargs allows us to configure few extra settings in our Serializer,here making sure password is write only and more than 5 characters.

    def create(self, validated_data): #Create a new user with encrypted password and return it
        return get_user_model().objects.create_user(**validated_data) # Call our custom create_user() function in order to create encrypted password for the new user. Use **validated_data to unwind validated_data into the params of create_user()

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None) #taking password out from validated data and removing it afterwards
        user = super().update(instance, validated_data) 

        # Set password if user provides one
        if password:
            user.set_password(password) #using set_password for encryption purpose
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer): #Serializer for the user authentication object
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        # Retrieve email and password from attrs DICT
        email = attrs.get('email')
        password = attrs.get('password')
        # Validate whether to pass/fail by using authenticate. See notes.
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # When authentication fails display message and error to user
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code='authentication')
        # Authentication passes so set attrs['user'] to user object
        attrs['user'] = user
        # Must return values(i.e attrs) at end when whenever overriding validate()
        return attrs