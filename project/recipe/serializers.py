from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer): #Serializer for tag object

	class Meta:
		model = Tag #The model serializer will access
		fields = ('id', 'name')
		read_only_fields = ('id',) 


class IngredientSerializer(serializers.ModelSerializer): #Serializer for ingredient objects
	
	class Meta:
		model = Ingredient
		fields = ('id','name')
		read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer): #Serializer for recipe
	
	ingredients = serializers.PrimaryKeyRelatedField(
		many = True,
		queryset = Ingredient.objects.all()
	) #it lists all the ingredients with their ids. https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
	tags = serializers.PrimaryKeyRelatedField(
		many = True,
		queryset = Tag.objects.all()
	)

	class Meta:
		model = Recipe
		fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes', 'price', 'link')
		read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer): #Serialize a recipe detail. Inheriting RecipeSerializer.
	ingredients = IngredientSerializer(many=True, read_only=True) #as DRF allows us to nest serializers inside serializers
	tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer): #Serializer for uploading images to recipes
	
	class Meta:
		model = Recipe
		fields = ('id', 'image')
		read_only_fields = ('id',)
