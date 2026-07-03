from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    ProfileView,
    RefreshView,
    RegisterView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    # Endpoints d'authentification et de gestion des utilisateurs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list_User/', UserListView.as_view(), name='list_user'),
    path('delete_User/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('modify_User/<int:pk>/', UserUpdateView.as_view(), name='modify_user'),
]
