from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    BookViewSet,
    LoanViewSet,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 🔹 Login JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
