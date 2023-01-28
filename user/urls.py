from django.urls import path
from . import views


urlpatterns = [
    path('user/',views.UserViewset.as_view()),
    path('user/reset-password/',views.reset_password)
]