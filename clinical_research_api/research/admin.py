from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Study, Site, SubjectAssignment, SubjectData


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('administrators',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'study', 'location', 'created_at')
    list_filter = ('study', 'created_at')
    search_fields = ('name', 'location')


@admin.register(SubjectAssignment)
class SubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'site', 'assigned_at')
    list_filter = ('site__study', 'assigned_at')
    search_fields = ('subject__username', 'subject__first_name', 'subject__last_name')


@admin.register(SubjectData)
class SubjectDataAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'site', 'uploader', 'uploaded_at')
    list_filter = ('site__study', 'uploaded_at')
    search_fields = ('subject_name', 'uploader__username')
    readonly_fields = ('uploaded_at',)
