from django.urls import include, path
from .views import TodoOperations, RegisterApi, LoginApi, LogoutApi

urlpatterns = [
    path('', TodoOperations.as_view(), name="todo"),
    path('register/', RegisterApi.as_view(), name="register"),
    path('login/', LoginApi.as_view(), name="login"),
    path('logout/', LogoutApi.as_view(), name="logout"),
]