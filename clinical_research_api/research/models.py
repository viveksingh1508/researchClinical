from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('subject', 'Research Subject'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='subject') 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class Study(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    administrators = models.ManyToManyField(
        User, 
        related_name='administered_studies',
        limit_choices_to={'role': 'admin'}
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "studies"


class Site(models.Model):
    name = models.CharField(max_length=200)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='sites')
    location = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.study.name})"


class SubjectAssignment(models.Model):
    subject = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='site_assignments',
        limit_choices_to={'role': 'subject'}
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='subject_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['subject', 'site']
    
    def __str__(self):
        return f"{self.subject} assigned to {self.site}"


class SubjectData(models.Model):
    subject_name = models.CharField(max_length=200)
    data = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='subject_data')
    uploader = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='uploaded_data',
        limit_choices_to={'role': 'subject'}
    )
    
    def __str__(self):
        return f"Data from {self.subject_name} at {self.site.name}"
    
    class Meta:
        verbose_name_plural = "subject data"
