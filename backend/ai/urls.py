from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AIDecisionPointViewSet, AIPromptViewSet,
    AIResponseViewSet, AILogViewSet
)

router = DefaultRouter()
router.register(r'decision-points', AIDecisionPointViewSet)
router.register(r'prompts', AIPromptViewSet)
router.register(r'responses', AIResponseViewSet)
router.register(r'logs', AILogViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 