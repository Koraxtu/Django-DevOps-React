from django.urls import path # type: ignore
from api.views import users_views as views # type: ignore

urlpatterns = [
    path('register/', views.registerUser, name='register_user'),
]