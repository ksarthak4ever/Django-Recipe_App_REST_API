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

		return self.serializer_class