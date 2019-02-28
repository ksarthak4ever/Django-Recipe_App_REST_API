from rest_framework.decorators import action #this decorator is used to add custom actions to our viewsets
from rest_framework.response import Response #for returning a custom response
from rest_framework import viewsets, mixins, status
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin): #Base viewset for user owned recipe attributes.Creating base class to reduce code duplicacy and as i'm making this api in Test Driven Development i can do this without worry of breaking the code.
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self): #Return objects for current authenticated user
		return self.queryset.filter(user=self.request.user).order_by('-name')

	def perform_create(self, serializer): #Create a new object. The perform_create function allows us to hook into the create process when creating an object i.e what happens is when we do a create object in our viewset this function gets invoked and the validated serializer will be passed in as a serializer argument
		serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet): #Manage tags in the database. Inheriting BaseRecipeAttrViewSet class to reduce code duplicacy
	queryset = Tag.objects.all() #as ListModelMixin require queryset to be passed
	serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet): #Manage ingredients in the database
	queryset = Ingredient.objects.all() #as ListModelMixin require queryset to be passed
	serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet): #Manage recipes in the database
	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self): #Retrieve the recipes for the authenticated user
		return self.queryset.filter(user=self.request.user)

	def get_serializer_class(self): #Return appropriate serializer class. From DRF documentation:~https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer
		elif self.action == 'upload_image':
			return serializers.RecipeImageSerializer

		return self.serializer_class

	def perform_create(self, serializer): #Create a new Recipe
		serializer.save(user=self.request.user)

	@action(methods=['POST'], detail=True, url_path='upload-image')
	def upload_image(self, request, pk=None): #Upload an image to a recipe
		recipe = self.get_object()
		serializer = self.get_serializer(
			recipe,
			data=request.data
		)

		if serializer.is_valid():
			serializer.save()
			return Response(
				serializer.data,
				status=status.HTTP_200_OK
			)

		return Response(
			serializer.errors,
			status=status.HTTP_400_BAD_REQUEST
		)