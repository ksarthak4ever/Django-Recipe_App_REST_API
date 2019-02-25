from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse #so we can generate our api url

from rest_framework.test import APIClient #it's a test client we can use to make request to our api and check what the response is.
from rest_framework import status #contains some status code we can see in readable form ex:~ instead of 200 it's http 200 ok.


CREATE_USER_URL = reverse('user:create') #just a constant variable being assigned create user url using reverse.
TOKEN_URL = reverse('user:token') #the url we will to use to make the http post request to generate our token


def create_user(**params): #a helper function.It is used to do anything we do multiple times in different tests so instead of creating a user each time for diff tests we make one user.params is a dynamic list of arguments we can pass directly into the create_user model which gives us a lot of flexibility about fields we can assign to the users we create.
	return get_user_model().objects.create_user(**params) #retrieve user model and 


class PublicUserApiTests(TestCase): #Test the users API (public)
	
	def setUp(self):
		self.client = APIClient()

	
	def test_create_valid_user_success(self): #Test creating user with valid payload is successful.
		payload = {
			'email': 'ksarthak4ever@gmail.com',
			'password': 'randomchikibum',
			'name': 'Sarthak kumar'
		} #Payload is the object we pass to the api when we make a request
		res = self.client.post(CREATE_USER_URL, payload) #making http post request to the client to the url for CREATE_USER_URL and passing payload

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(**res.data) #testing if object is actually created
		self.assertTrue(user.check_password(payload['password']))
		self.assertNotIn('password', res.data) #making sure password is not returned in the request as it can be a security vulnerability

	
	def test_user_exists(self): #Test creating a user that already exists fails
		payload = {
			'email' : 'ksarthak4ever@gmail.com',
			'password': 'testpass'
		}
		create_user(**payload)

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_password_too_short(self): #Testing that password must be more that 5 characters
		payload = {
			'email' : 'ksarthak4ever@gmail.com',
			'password' : 'pw'
		}
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		user_exists = get_user_model().objects.filter(
			email=payload['email']
		).exists()
		self.assertFalse(user_exists) #making sure user doen'nt exist. NOTE- every test refreshes the db so we can use same email in diff test fns. 


	def test_create_token_for_user(self): #Test that a token is created for the user
		payload = {
			'email': 'ksarthak4ever@gmail.com',
			'password': 'testpass'
		}
		create_user(**payload)# Create user that matches this authentication to test against user
		res = self.client.post(TOKEN_URL, payload)# Make our request and store it in response variables

		self.assertIn('token', res.data)# Assert that token was created and 'token' key in response data
		self.assertEqual(res.status_code, status.HTTP_200_OK)# Assert that we get HTTP_200_OK


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
			'password': 'anything'
		}
		res = self.client.post(TOKEN_URL, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_create_token_missing_field(self): #Test that email and password are required
		res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	












