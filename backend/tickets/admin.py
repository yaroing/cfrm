"""
Configuration de l'interface d'administration pour les tickets
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Priority, Status, Channel, Ticket, 
    Response, TicketLog, Feedback
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_sensitive', 'requires_escalation', 'escalation_contact', 'created_at']
    list_filter = ['is_sensitive', 'requires_escalation', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'sla_hours', 'color_display']
    list_filter = ['level']
    search_fields = ['name']
    readonly_fields = ['created_at']

    def color_display(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Couleur'


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_final', 'color_display', 'created_at']
    list_filter = ['is_final', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

    def color_display(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Couleur'


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_active', 'created_at']
    list_filter = ['type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    readonly_fields = ['created_at']


class TicketLogInline(admin.TabularInline):
    model = TicketLog
    extra = 0
    readonly_fields = ['created_at', 'action', 'user', 'description']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'category', 'priority', 'status', 
        'channel', 'assigned_to', 'is_psea', 'created_at', 'is_overdue_display'
    ]
    list_filter = [
        'category', 'priority', 'status', 'channel', 'is_psea', 
        'is_anonymous', 'created_at', 'assigned_to'
    ]
    search_fields = ['id', 'title', 'content', 'submitter_name', 'submitter_phone', 'submitter_email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'closed_at', 'days_since_creation']
    inlines = [ResponseInline, TicketLogInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'title', 'content', 'is_anonymous')
        }),
        ('Classification', {
            'fields': ('category', 'priority', 'status')
        }),
        ('Canal et origine', {
            'fields': ('channel', 'external_id')
        }),
        ('Informations du plaignant', {
            'fields': ('submitter_name', 'submitter_phone', 'submitter_email', 'submitter_location'),
            'classes': ('collapse',)
        }),
        ('Assignation', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('SLA et escalade', {
            'fields': ('sla_deadline', 'escalated_at', 'escalated_to'),
            'classes': ('collapse',)
        }),
        ('PSEA', {
            'fields': ('is_psea', 'psea_contact', 'psea_escalated'),
            'classes': ('collapse',)
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('attachments', 'tags', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'closed_at', 'days_since_creation'),
            'classes': ('collapse',)
        }),
    )

    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">⚠ En retard</span>')
        return format_html('<span style="color: green;">✓ Dans les temps</span>')
    is_overdue_display.short_description = 'SLA'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'channel', 'is_internal', 'sent_at', 'created_at']
    list_filter = ['is_internal', 'channel', 'created_at', 'sent_at']
    search_fields = ['ticket__id', 'content', 'author__username']
    readonly_fields = ['created_at']


@admin.register(TicketLog)
class TicketLogAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'action', 'user', 'created_at']
    list_filter = ['action', 'created_at', 'user']
    search_fields = ['ticket__id', 'description', 'user__username']
    readonly_fields = ['created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'satisfaction_rating', 'response_time_rating', 'quality_rating', 'created_at']
    list_filter = ['satisfaction_rating', 'response_time_rating', 'quality_rating', 'created_at']
    search_fields = ['ticket__id', 'comments']
    readonly_fields = ['created_at']
