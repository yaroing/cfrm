"""
Configuration de l'interface d'administration pour les utilisateurs
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    Organization, Role, User, UserSession, 
    UserActivity, UserPreference
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact_email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'is_psea_authorized', 'can_escalate', 
        'can_assign', 'can_close', 'can_view_analytics', 'created_at'
    ]
    list_filter = [
        'is_psea_authorized', 'can_escalate', 'can_assign', 
        'can_close', 'can_view_analytics', 'created_at'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


class UserSessionInline(admin.TabularInline):
    model = UserSession
    extra = 0
    readonly_fields = ['session_key', 'ip_address', 'created_at', 'last_activity']


class UserActivityInline(admin.TabularInline):
    model = UserActivity
    extra = 0
    readonly_fields = ['action', 'description', 'ip_address', 'created_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'full_name', 'organization', 
        'role', 'is_active', 'is_verified', 'last_login', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_verified', 'is_staff', 'is_superuser',
        'organization', 'role', 'created_at', 'last_login'
    ]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_activity', 'last_login_ip']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone', 'organization', 'role', 'location', 'timezone', 'language')
        }),
        ('Statut', {
            'fields': ('is_verified', 'last_login_ip', 'last_activity')
        }),
        ('Métadonnées', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone', 'organization', 'role', 'location', 'timezone', 'language')
        }),
    )
    
    inlines = [UserSessionInline, UserActivityInline]

    def full_name(self, obj):
        return obj.get_full_name() or obj.username
    full_name.short_description = 'Nom complet'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'is_active', 'created_at', 'last_activity']
    list_filter = ['is_active', 'created_at', 'last_activity']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['session_key', 'created_at', 'last_activity']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at', 'user']
    search_fields = ['user__username', 'description', 'ip_address']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'email_notifications', 'sms_notifications', 'updated_at']
    list_filter = ['theme', 'email_notifications', 'sms_notifications', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
