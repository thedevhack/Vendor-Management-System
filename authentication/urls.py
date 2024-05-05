from django.urls import path
from authentication.views import RegisterUser

urlpatterns = [
    path("register/", RegisterUser.as_view())
]
