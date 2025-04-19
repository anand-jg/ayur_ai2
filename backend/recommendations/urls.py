from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorReviewViewSet, AppointmentViewSet, DoctorRecommendationViewSet

router = DefaultRouter()
router.register(r'reviews', DoctorReviewViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'recommendations', DoctorRecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 