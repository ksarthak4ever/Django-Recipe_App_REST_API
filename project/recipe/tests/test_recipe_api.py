from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params): #Helper function to Create and return a sample recipe.	
	defaults = {
		'title': 'Sample recipe',
		'time_minutes': 10,
		'price': 50.00
	}
	defaults.update(params) #this update function takes the dictionary object(here defaults) and it will update them, if they dont exist then it will create them.

	return Recipe.objects.create(user=user, **defaults) # **defaults work opposite of params i.e as params passes argument into the dictionary, the default will convert the dictionary into an argument


class PublicRecipeApiTests(TestCase): #Test unauthenticated recipe API access
	
	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self): #Test that authentication is required
		res = self.client.get(RECIPES_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase): #Test authenticated recipe API access
	
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'ksarthak4ever@gmail.com',
			'randompassword'
		)
		self.client.force_authenticate(self.user)

	def test_retrieve_recipes(self): #Test retrieving a list of recipes
		sample_recipe(user=self.user)
		sample_recipe(user=self.user) #creating two recipes

		res = self.client.get(RECIPES_URL)

		recipes = Recipe.objects.all().order_by('-id')
		serializer = RecipeSerializer(recipes, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_recipes_limited_to_user(self): #Test retrieving recipes for user
		user2 = get_user_model().objects.create_user(
			'kshubham155@gmail.com',
			'password123'
		)
		sample_recipe(user=user2)
		sample_recipe(user=self.user)

		res = self.client.get(RECIPES_URL)

		recipes = Recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes, many=True)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data, serializer.data)