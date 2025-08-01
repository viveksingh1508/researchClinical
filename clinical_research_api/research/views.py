from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import User, Study, Site, SubjectAssignment, SubjectData
from .serializers import (
    UserSerializer, StudySerializer, SiteSerializer, 
    SubjectAssignmentSerializer, SubjectDataSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        study = self.get_object()
        assignments = SubjectAssignment.objects.filter(site__study=study)
        serializer = SubjectAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        site = self.get_object()
        assignments = SubjectAssignment.objects.filter(site=site)
        serializer = SubjectAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subject_data(self, request, pk=None):
        site = self.get_object()
        data = SubjectData.objects.filter(site=site)
        serializer = SubjectDataSerializer(data, many=True)
        return Response(serializer.data)


class SubjectAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SubjectAssignment.objects.all()
    serializer_class = SubjectAssignmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubjectDataViewSet(viewsets.ModelViewSet):
    queryset = SubjectData.objects.all()
    serializer_class = SubjectDataSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return SubjectData.objects.all()
        else:
            assignments = SubjectAssignment.objects.filter(subject=user)
            return SubjectData.objects.filter(site__in=[a.site for a in assignments])
    
    def perform_create(self, serializer):
        user = self.request.user
        site_id = serializer.validated_data['site'].id
        
        if user.role != 'subject':
            return Response(
                {'error': 'Only subjects can upload data'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        assignment = SubjectAssignment.objects.filter(
            subject=user, site_id=site_id
        ).first()
        
        if not assignment:
            return Response(
                {'error': 'User not assigned to this site'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(uploader=user)
