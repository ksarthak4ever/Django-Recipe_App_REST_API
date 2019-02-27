from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings #as we want to use AUTH_USER_MODEL to apply foreign key.https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey

class UserManager(BaseUserManager): #to pull in all features of BaseUserManager and override some functions to handle our email instead of username

	def create_user(self, email, password=None, **extra_fields): #creates and saves a new user
		if not email:
			raise ValueError('Users must have an email address')
		user = self.model(email=self.normalize_email(email), **extra_fields) 
		user.set_password(password) #to store password as a hash
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password): #creates and saves a new super user
		user = self.create_user(email, password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin): #custom user model that supports using email instead of username
	email = models.EmailField(max_length=250, unique=True)
	name = models.CharField(max_length=250)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager() #assigning UserManager to the objects attribute i.e UserManager runs for every new object or new User

	USERNAME_FIELD = 'email' #so we can use email as a field to login


class Tag(models.Model): # Tag to be used for a recipe
	name = models.CharField(max_length=255)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.CASCADE, #as when we delete the user we delete the tags as well
	) #assigning foreign key to the User object.

	def __str__(self): #using dunder method to add string rep of the model
		return self.name


class Ingredient(models.Model): #Ingredient to be used in a recipe
	name = models.CharField(max_length=255)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)

	def __str__(self):
		return self.name