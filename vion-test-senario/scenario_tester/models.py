from django.db import models
from django.utils import timezone

class Session(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    executed_apps = models.CharField(max_length=255, blank=True, default="")
    server = models.CharField(max_length=50, blank=True, default="")

    def finalize(self):
        self.end_time = timezone.now()
        self.save()

    def __str__(self):
        return f"Session {self.id} - {self.start_time}"
    
class Scenario(models.Model):
    STATUS_CHOICES = [
        ('unknown', 'Unknown'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Error'),
    ]
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="scenarios")
    scenario_name = models.CharField(max_length=255, default='UnknownScenario')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="unknown")

    def finalize(self):
        self.end_time = timezone.now()
        self.save()

    @property
    def description(self):
        """
        Retrieves the `__doc__` string of the scenario class that matches `scenario_name`.
        Uses the ScenarioService.find_scenarios method to find scenario classes.
        """
        from scenario_tester.services import ScenarioService

        scenarios = {cls.__name__: cls for cls in ScenarioService.find_scenarios()}
        scenario_class = scenarios.get(self.scenario_name)
        return scenario_class.__doc__.strip() if scenario_class and scenario_class.__doc__ else "No description available."

    def __str__(self):
        return f"ID: {self.id}, Scenario {self.scenario_name} - {self.status}"


class Log(models.Model):
    class LogLevel(models.TextChoices):
        INFO = "info", "Info"
        WARNING = "warning", "Warning"
        ERROR = "error", "Error"
        DEBUG = "debug", "Debug"

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="logs")
    level = models.CharField(max_length=10, choices=LogLevel.choices, default=LogLevel.INFO)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level.upper()}: {self.text[:50]} (Scenario ID: {self.scenario.id} )"
