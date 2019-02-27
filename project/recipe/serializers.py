from rest_framework import serializers

from core.models import Tag, Ingredient


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

