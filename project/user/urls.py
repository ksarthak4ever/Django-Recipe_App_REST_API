from django.urls import path

from user import views


app_name = 'user' #app_name is set to identify which app we are creating the url from when we use our reverse function

urlpatterns = [
	path('create/', views.CreateUserView.as_view(), name='create'),
	path('token/', views.CreateUserView.as_view(), name='token'),
]