from django.test import TestCase
from django.contrib.auth import get_user_model #as if we directly import user model then if we want to make changes in the future to the user model then it will be tricky and importing get_user_model can help in this as we just have to make changes at one place and change all the references of the user model

from core import models #importing models from core app


def sample_user(email='ksarthak4ever@gmail.com', password='randompassword'): #creating a sample user
	return get_user_model().objects.create_user(email, password)



class ModelTests(TestCase):

	def test_create_user_with_email_successful(self): #Test creating a new user with an email is successful
		email = 'ksarthak4ever@gmail.com'
		password = 'TestPass123' #no need for password or email to actually be true as test will only for an instance while test runs before being deleted
		user = get_user_model().objects.create_user(
				email=email,
				password=password
			)

		self.assertEqual(user.email, email) #checking if email address of our created user is equal to email address passed in
		self.assertTrue(user.check_password(password)) #as password is encrypted so using check_password i.e helper function that comes with django user model and returns True if password is correct


	def test_new_user_email_normalized(self): #Test the email for a new user is normalized i.e using normalize_email() method that Normalizes email addresses by lowercasing the domain portion of the email address
		email = 'ksarthak4ever@GMAIL.COM'
		user = get_user_model().objects.create_user(email, 'ThrowawayString')

		self.assertEqual(user.email, email.lower())

 
	def test_new_user_invalid_email(self): #Test creating user with no email raises error
		with self.assertRaises(ValueError): #making sure that if we call create_user function and dont pass email address then we raise an Value Error
			get_user_model().objects.create_user(None, 'ThrowableString')


	def test_create_new_superuser(self): #Test creating a new superuser
		user = get_user_model().objects.create_superuser(
			'kumarsarthak800@gmail.com',
			'test123'
		)

		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)


	def test_tag_str(self): #Test the tag string representation i.e test that creates a tag and verifies that it converts to the correct string representation
		tag = models.Tag.objects.create(
			user=sample_user(),
			name='Vegan'
			)
		self.assertEqual(str(tag), tag.name)

