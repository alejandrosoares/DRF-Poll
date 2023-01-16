from django.urls import path

from .views import UserListView, UserCreateView, LoginView

app_name = 'users'
urlpatterns = [
    path('', UserListView.as_view(), name="list"),
    path('create', UserCreateView.as_view(), name="create"),
    path('login', LoginView.as_view(), name='login')
]
