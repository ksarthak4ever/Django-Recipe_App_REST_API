from django.urls import path,include
from rest_framework.routers import DefaultRouter

from recipe import views 

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe' #so that when we identify the app the reverse function can look up the correct urls

urlpatterns = [
	path('', include(router.urls))
]