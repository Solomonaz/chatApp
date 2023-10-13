from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('index/', views.index, name='index'),
        # path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
