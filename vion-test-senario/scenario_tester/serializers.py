from rest_framework import serializers
from scenario_tester.models import Session, Scenario, Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['level', 'text', 'created_at']


class ScenarioSerializer(serializers.ModelSerializer):
    logs = LogSerializer(many=True, read_only=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = Scenario
        fields = ['id', 'scenario_name', 'description', 'start_time', 'end_time', 'status', 'logs']

    def get_description(self, obj):
        return obj.description
    
    # Will not show 'logs' field if there is none
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.logs.exists():
            representation.pop('logs', None)
        return representation


class SessionSerializer(serializers.ModelSerializer):
    scenarios = ScenarioSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'server', 'executed_apps', 'start_time', 'end_time', 'scenarios']
