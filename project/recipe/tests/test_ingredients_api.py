from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase) : #Test the publically available ingredients API

	def setUp(self):
		self.client = APIClient()

	def test_login_required(self): #Test that login is required to access the endpoint
		res = self.client.get(INGREDIENTS_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase): #Test the private ingredients api
	
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'ksarthak4ever@gmail',
			'hakunamatata'
		)
		self.client.force_authenticate(self.user)

	def test_retrieve_ingredients_list(self): #Test retrieving a list of ingredients
		Ingredient.objects.create(user=self.user, name='Potato')
		Ingredient.objects.create(user=self.user, name='Peas')

		res = self.client.get(INGREDIENTS_URL)

		ingredients = Ingredient.objects.all().order_by('-name')
		serializer = IngredientSerializer(ingredients, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_ingredients_limited_to_user(self): #Test that ingredients for the authenticated user are returned
		user2 = get_user_model().objects.create_user(
			'harshkumar800@gmail.com',
			'testpass'
		)
		Ingredient.objects.create(user=user2, name='Vinegar')
		ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

		res = self.client.get(INGREDIENTS_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data),1 )
		self.assertEqual(res.data[0]['name'], ingredient.name)



