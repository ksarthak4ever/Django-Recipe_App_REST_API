from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse #so we can generate our api url

from rest_framework.test import APIClient #it's a test client we can use to make request to our api and check what the response is.
from rest_framework import status #contains some status code we can see in readable form ex:~ instead of 200 it's http 200 ok.


CREATE_USER_URL = reverse('user:create') #just a constant variable being assigned create user url using reverse.
TOKEN_URL = reverse('user:token') #the url we will to use to make the http post request to generate our token
ME_URL = reverse('user:me') # i.e url of the account of the user that is authenticated


# Helper function for creating a new user since we will do it multiple times
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Create our Public API test
class PublicUserApiTests(TestCase): #Test the users API (public)

    def setUp(self):
        # Make it easier to call our client in our tests that we can resuse
        self.client = APIClient()

    def test_create_valid_user_success(self): #Test creating user with valid payload is successful.
        payload = {
            'email': 'ksarthak4ever@gmail.com',
            'password': 'booyaka',
            'name': 'Sarthak Kumar'
        } #Payload is the object we pass to the api when we make a request
        res = self.client.post(CREATE_USER_URL, payload) #making http post request to the client to the url for CREATE_USER_URL and passing payload

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data) #testing if object is actually created
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data) #making sure password is not returned in the request as it can be a security vulnerability


    def test_user_exists(self): #Test creating a user that already exists fails
        payload = {
            'email': 'ksarthak4ever@gmail.com',
            'password': 'ksarthak4ver',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self): #Testing that password must be more that 5 characters
        payload = {
            'email': 'ksarthak4ever@gmail.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists) # Confirm that user was NOT created (i.e., .exists() = False)

    def test_create_token_for_user(self):
        payload = {
        	'email': 'ksarthak4ever@gmail.com',
        	'password': 'testpass'
        }
        create_user(**payload) # Create user that matches this authentication to test against user
        res = self.client.post(TOKEN_URL, payload) #make our request and pass it in response variable

        self.assertIn('token', res.data) # Assert that token was created and 'token' key in response data
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self): #Test that token is not created if invalid credentials are given
        create_user(email='ksarthak4ever@gmail.com', password='anything')
        payload = {
        	'email': 'ksarthak4ever@gmail.com',
        	'password': 'nothinglol'
        } #since here the user we created and the values entered/payload is diff so token shoul not be created
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self): #Test that token is not created if user doen'nt exist
        payload = {
        	'email': 'ksarthak4ever@gmail.com',
        	'password': 'helloworld'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self): #Test that email and password are required
        payload = {
        	'email': 'test@gmail.com',
        	'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""
    # Set authentication for each subsequent test

    def setUp(self):
        self.user = create_user(
            email='ksarthak4ever@gmail.com',
            password='testpass',
            name='Sarthak'
        )
        # Setup our reusable client but force authenticate method
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        # Already authenticated in setUp() so just make request
        res = self.client.get(ME_URL)

        # Assert that the response is good
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Assert that the user object returned is what we expected
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        # Make POST request and pass empty object
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}
        res = self.client.patch(ME_URL, payload)

        # Using the helper function refresh_from_db() to update the user
        self.user.refresh_from_db()

        # Verify that the values we provided were updated
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)