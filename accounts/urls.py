from django.urls import path
from accounts.views import CustomTokenObtainPairView,  AuthorCreateUpdateView, UserProfileUpdateView, CurrentUserView, AuthorImageView
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', csrf_exempt(CustomTokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('token/refresh/', csrf_exempt(TokenRefreshView.as_view()), name='token_refresh'),
    path('authors/', AuthorCreateUpdateView.as_view(), name='create-author'),
    path('authors/<int:pk>/', AuthorCreateUpdateView.as_view(), name='update-author'),
    path('profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('authors/<int:pk>/image/', AuthorImageView.as_view(), name='upload-author-image'),
]


