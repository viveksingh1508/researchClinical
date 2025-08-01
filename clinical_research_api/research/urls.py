from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'studies', views.StudyViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'assignments', views.SubjectAssignmentViewSet)
router.register(r'subject-data', views.SubjectDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]