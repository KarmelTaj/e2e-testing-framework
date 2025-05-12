from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from .models import Session, Scenario, Log

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'start_time', 'end_time', 'executed_apps', 'view_scenarios_link')
    search_fields = ('id', 'executed_apps',)
    list_filter = ('server', 'start_time', 'end_time', 'executed_apps')
    ordering = ('-start_time',)

    @admin.display(description="View Scenarios")
    def view_scenarios_link(self, obj):
        """
        Generates a link to the Scenario admin page, filtered by the session ID.
        """
        url = reverse('admin:scenario_tester_scenario_changelist')
        query = urlencode({'session__id': obj.id})
        return format_html('<a href="{}?{}">View Scenarios</a>', url, query)


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'scenario_name', 'start_time', 'end_time', 'status', 'session_link', 'view_logs_link')
    search_fields = ('scenario_name', 'session__id')
    list_filter = ('status', 'start_time', 'end_time')
    ordering = ('-start_time',)
    list_editable = ('status',)

    @admin.display(description="Session")
    def session_link(self, obj):
        """
        Generates a link back to the Session admin page.
        """
        url = reverse('admin:scenario_tester_session_changelist')
        query = urlencode({'id': obj.session.id})
        return format_html('<a href="{}?{}">Session {}</a>', url, query, obj.session.id)

    @admin.display(description="View Logs")
    def view_logs_link(self, obj):
        """
        Generates a link to the Log admin page, filtered by the scenario ID.
        """
        url = reverse('admin:scenario_tester_log_changelist')
        query = urlencode({'scenario__id': obj.id})
        return format_html('<a href="{}?{}">View Logs</a>', url, query)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'scenario', 'level', 'text_snippet', 'created_at', 'scenario_link')
    search_fields = ('scenario__scenario_name', 'text')
    list_filter = ('level', 'created_at')
    ordering = ('-created_at',)

    @admin.display(description="Scenario")
    def scenario_link(self, obj):
        """
        Generates a link back to the Scenario admin page.
        """
        url = reverse('admin:scenario_tester_scenario_changelist')
        query = urlencode({'id': obj.scenario.id})
        return format_html('<a href="{}?{}">Scenario {}</a>', url, query, obj.scenario.id)

    @admin.display(description="Log Snippet")
    def text_snippet(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
