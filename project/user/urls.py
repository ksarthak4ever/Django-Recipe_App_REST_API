from django.urls import path

from user import views

# Define our app name to help ID which app we're creating the URL from
# when we use our reverse()
app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'), #i.e url for account of user that is authenticated 
]