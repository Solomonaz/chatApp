from django.urls import path
from .views import RegistrationView, CustomLoginView, CustomLogoutView, index

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('index/', index, name='index'),
]
