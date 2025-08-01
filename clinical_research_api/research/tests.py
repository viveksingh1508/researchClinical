from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Study, Site, SubjectAssignment, SubjectData


class ClinicalResearchAPITestCase(APITestCase):
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin1',
            first_name='John',
            last_name='Admin',
            email='admin@example.com',
            role='admin',
            password='adminpass'
        )
        
        self.subject_user = User.objects.create_user(
            username='subject1',
            first_name='Jane',
            last_name='Subject',
            email='subject@example.com',
            role='subject',
            password='subjectpass'
        )
        
        self.study = Study.objects.create(
            name='Test Study',
            description='A test clinical study'
        )
        self.study.administrators.add(self.admin_user)
        
        self.site = Site.objects.create(
            name='Test Site',
            study=self.study,
            location='Test Location'
        )
        
        self.assignment = SubjectAssignment.objects.create(
            subject=self.subject_user,
            site=self.site
        )
    
    def test_admin_can_create_study(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'New Study',
            'description': 'A new clinical study'
        }
        response = self.client.post('/api/studies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_subject_cannot_create_study(self):
        self.client.force_authenticate(user=self.subject_user)
        data = {
            'name': 'New Study',
            'description': 'A new clinical study'
        }
        response = self.client.post('/api/studies/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_subject_can_upload_data(self):
        self.client.force_authenticate(user=self.subject_user)
        data = {
            'subject_name': 'Jane Subject',
            'data': {'temperature': 98.6, 'heart_rate': 72},
            'site': self.site.id
        }
        response = self.client.post('/api/subject-data/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_site_subjects(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/sites/{self.site.id}/subjects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_study_subjects(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/studies/{self.study.id}/subjects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
