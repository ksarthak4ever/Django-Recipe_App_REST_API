from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase): #Test the publicly available tags API

	def setUp(self):
		self.client = APIClient()

	def test_login_required(self): #Test that login is required for retrieving tags
		res = self.client.get(TAGS_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase): #Test that authorized user tags API
	
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			'ksarthak4ever@gmail.com',
			'password123'
		) #creating authenticated user for tests
		self.client = APIClient()
		self.client.force_authenticate(self.user) #force authenticating the user

	def test_retrieve_tags(self): #testing that tags are retrieved for the user
		Tag.objects.create(user=self.user, name='Vegan')
		Tag.objects.create(user=self.user, name='Dessert') #creating tags for a user

		res = self.client.get(TAGS_URL) #retrieving tags and storing response in res variable

		tags = Tag.objects.all().order_by('-name')
		serializer = TagSerializer(tags, many=True) #many=True as many serializer objects can be passed
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_tags_limited_to_user(self): #Testing that retrieved tags are for the authorized user only
		user2 = get_user_model().objects.create_user(
			'harshkumar800@gmail.com',
			'testpass'
		)
		Tag.objects.create(user=user2, name='Fruits') #creating tag for this user
		tag = Tag.objects.create(user=self.user, name='Comfort Food') #creating tag for authenticated user

		res = self.client.get(TAGS_URL) #retrieving tag

		self.assertEqual(res.status_code, status.HTTP_200_OK) #making sure tag is retrieved
		self.assertEqual(len(res.data), 1) #making sure only 1 tag is returned for authenticated user
		self.assertEqual(res.data[0]['name'], tag.name) #making sure tag of authenticated user here

	def test_create_tag_successful(self): #Test creating a new tag for recipe
		payload = {'name': 'Test tag'}
		self.client.post(TAGS_URL, payload)

		exists = Tag.objects.filter(
			user = self.user,
			name = payload['name']
		).exists()  #this will return boolean true or false
		self.assertTrue(exists)

	def test_create_tag_invalid(self): #Test creating a new tag with invalid payload
		payload = {'name': ''}
		res = self.client.post(TAGS_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

