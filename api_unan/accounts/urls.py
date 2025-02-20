from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, GroupViewSet, StudentViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'users', AccountViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
