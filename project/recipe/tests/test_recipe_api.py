from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list') #i.e /api/recipe/recipes


def detail_url(recipe_id): #Return recipe detail url. i.e /api/recipe/recipes/1 and so on
	return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main Course'): #Helper function to create and return a simple tag
	return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Chicken'): #Helper function to create and return a sample ingredient
	return Ingredient.objects.create(user=user, name=name)


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

	def test_view_recipe_detail(self): #Test viewing a recipe detail
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tag(user=self.user))
		recipe.ingredients.add(sample_ingredient(user=self.user))

		url = detail_url(recipe.id)
		res = self.client.get(url)

		serializer = RecipeDetailSerializer(recipe) #as serializing only a single object/recipe so no need for many=True
		self.assertEqual(res.data, serializer.data)

	def test_create_basic_recipe(self): #Test creating recipe
		payload = {
			'title': 'Butter Chicken',
			'time_minutes': 30,
			'price': 400.00
		}
		res = self.client.post(RECIPES_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id']) #As in DRF when we create/call an object the values are returned in form of dictionary
		for key in payload.keys():
			self.assertEqual(payload[key], getattr(recipe, key)) #getattr allows us to retrieve the attribute using a variable

	def test_create_recipe_with_tags(self): #Test creating a recipe with tags
		tag1 = sample_tag(user=self.user, name='Vegan')
		tag2 = sample_tag(user=self.user, name='Dessert')
		payload = {
			'title': 'Blueberry Cheesecake',
			'tags': [tag1.id, tag2.id],
			'time_minutes': 60,
			'price': 200.00
		}
		res = self.client.post(RECIPES_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id']) #retrieving the created recipe
		tags = recipe.tags.all() #retrieving all the tags associated with this recipe and storing them in a variable tags
		self.assertEqual(tags.count(), 2) 
		self.assertIn(tag1, tags)
		self.assertIn(tag2, tags)

	def test_create_recipe_with_ingredients(self): #Test creating recipe with ingredients
		ingredient1 = sample_ingredient(user=self.user, name='Fish')
		ingredient2 = sample_ingredient(user=self.user, name='Ginger')
		payload = {
			'title': 'Fish Curry',
			'ingredients': [ingredient1.id, ingredient2.id],
			'time_minutes': 25,
			'price': 300.00
		}
		res = self.client.post(RECIPES_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		ingredients = recipe.ingredients.all()
		self.assertEqual(ingredients.count(), 2)
		self.assertIn(ingredient1, ingredients) #making sure the ingredient we created is present in recipe
		self.assertIn(ingredient2, ingredients)

