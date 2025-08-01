from rest_framework import serializers
from .models import User, Study, Site, SubjectAssignment, SubjectData


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudySerializer(serializers.ModelSerializer):
    administrators = UserSerializer(many=True, read_only=True)
    administrator_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Study
        fields = ['id', 'name', 'description', 'created_at', 'administrators', 'administrator_ids']
    
    def create(self, validated_data):
        administrator_ids = validated_data.pop('administrator_ids', [])
        study = Study.objects.create(**validated_data)
        if administrator_ids:
            administrators = User.objects.filter(id__in=administrator_ids, role='admin')
            study.administrators.set(administrators)
        return study


class SiteSerializer(serializers.ModelSerializer):
    study_name = serializers.CharField(source='study.name', read_only=True)
    
    class Meta:
        model = Site
        fields = ['id', 'name', 'location', 'study', 'study_name', 'created_at']


class SubjectAssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.get_full_name', read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)
    
    class Meta:
        model = SubjectAssignment
        fields = ['id', 'subject', 'subject_name', 'site', 'site_name', 'assigned_at']


class SubjectDataSerializer(serializers.ModelSerializer):
    uploader_name = serializers.CharField(source='uploader.get_full_name', read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)
    
    class Meta:
        model = SubjectData
        fields = ['id', 'subject_name', 'data', 'uploaded_at', 'site', 'site_name', 'uploader', 'uploader_name']
    
    def create(self, validated_data):
        validated_data['uploader'] = self.context['request'].user
        return super().create(validated_data)