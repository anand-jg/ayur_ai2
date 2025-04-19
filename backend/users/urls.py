from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorProfileViewSet, UserHealthProfileViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'doctors', DoctorProfileViewSet)
router.register(r'health-profiles', UserHealthProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='logout'),
] 