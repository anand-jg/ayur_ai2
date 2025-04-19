from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, UserResponseViewSet, DiagnosisViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'responses', UserResponseViewSet)
router.register(r'diagnoses', DiagnosisViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 