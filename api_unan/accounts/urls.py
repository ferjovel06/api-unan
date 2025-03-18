from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, StudentViewSet, TeacherViewSet, CareerViewSet, KnowledgeAreaViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'careers', CareerViewSet)
router.register(r'knowledge-areas', KnowledgeAreaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
