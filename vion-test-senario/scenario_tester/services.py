import os
import importlib
import inspect
import random

from django.apps import apps
from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import redirect
from django.urls import reverse

from .exceptions import URLValidationException
from .exceptions import ScenarioWithNotAppException
from .exceptions import UnexpectedErrorException
from .models import Session, Scenario
from .scenarios import BaseScenario

from functools import lru_cache
from queue import Queue
from threading import Thread
from datetime import datetime

class ScenarioService:
    """
    Service to discover and execute all scenarios in the project.
    """

    @staticmethod
    @lru_cache
    def find_scenarios(app_name: str = None, scenario_name: str = None) -> list:
        """
        Finds all subclasses inheriting from BaseScenario across the project or within a specific app.
        Optionally filters by scenario name when app_name is provided.

        Args:
            app_name (str, optional): The name of the app to filter scenarios by.
            scenario_name (str, optional): The name of the specific scenario to find.

        Returns:
            list: A list of scenario classes (or a single class if scenario_name is specified).
        """

        if scenario_name and not app_name:
            raise ValueError("scenario_name parameter requires an app_name to be provided.")

        scenario_classes = []

        app_configs = ([apps.get_app_config(app_name)] if app_name else apps.get_app_configs())
        for app in app_configs:
            try:
                # Import the 'scenarios' module from each app
                scenarios_module = importlib.import_module(f"{app.name}.scenarios")

                for name, obj in inspect.getmembers(scenarios_module, inspect.isclass):
                    # Check if the class is a subclass of BaseScenario
                    if issubclass(obj, BaseScenario) and obj != BaseScenario:
                        # Detect if `is_abstract` was overridden
                        parrent_class = obj.__bases__[0]
                        base_method = parrent_class.is_abstract
                        obj_method = obj.is_abstract

                        if base_method == obj_method or not obj_method(obj):
                            if scenario_name and name != scenario_name:
                                continue
                            scenario_classes.append(obj)
            except ModuleNotFoundError:
                if app_name:  # If a specific app was requested and it failed
                    raise ModuleNotFoundError(f"App '{app_name}' does not have a 'scenarios' module.")
                continue

        if scenario_name and not scenario_classes:
            raise ValueError(f"Scenario '{scenario_name}' not found in app '{app_name}'.")

        return scenario_classes

    @staticmethod
    def _run_scenario(base_url, scenario_class, session):
        """
        Runs a single scenario and updates its status in the database.

        Args:
            scenario_class: The scenario class to be executed.
            session: The current session object.
            base_url: The base URL for the scenario.
        """

        try:
            instance = scenario_class(base_url)
            instance.execute(session)
        except Exception as e:
            scenario = Scenario.objects.filter(session=session, scenario_name=scenario_class.__name__).first()
            if scenario:
                scenario.status = "error"
                scenario.save()
      
    @staticmethod
    def _execute_scenarios_one_by_one(scenarios, base_url, base_url_key):
        """
        Creates a session, executes all scenarios or a specific scenario, and finalizes the session.

        Args:
            base_url (str): The base URL to be used for scenario execution.
            base_url_key (str): The key representing the server environment (e.g., "Development").
            app_name (str, optional): The name of the app containing the scenarios to execute.
            scenario_name (str, optional): The name of a specific scenario to execute.
        """

        session = Session.objects.create(start_time=now(), server=base_url_key)

        # Collect the names of apps whose scenarios were executed
        executed_apps = set()

        for scenario_class in scenarios:
            ScenarioService._run_scenario(base_url, scenario_class, session)
            app_label = scenario_class.__module__.split('.')[0]
            executed_apps.add(app_label)

        # Update the executed_apps field in the session
        session.executed_apps = ", ".join(sorted(executed_apps))
        session.finalize()
        
    @staticmethod
    def _execute_scenarios_thread(scenarios, base_url, base_url_key):
        """
        Executes all scenarios using a queue and threads.

        Args:
            base_url (str): The base URL to be used for scenario execution.
            base_url_key (str): The key representing the server environment (e.g., "Development").
            app_name (str, optional): The name of the app containing the scenarios to execute.
            scenario_name (str, optional): The name of a specific scenario to execute.
        """

        # Create Session
        session = Session.objects.create(start_time=now(), server=base_url_key)

        task_queue = Queue()
        for scenario_class in scenarios:
            task_queue.put(scenario_class)

        # Track executed apps
        executed_apps = set()

        # Worker function
        def worker():
            while not task_queue.empty():
                scenario_class = task_queue.get()
                try:
                    ScenarioService._run_scenario(base_url, scenario_class, session)
                    app_label = scenario_class.__module__.split('.')[0]
                    executed_apps.add(app_label)
                finally:
                    task_queue.task_done()

        num_workers = settings.THREAD_WORKERS
        threads = []
        for _ in range(num_workers):
            thread = Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Wait for all tasks to complete
        task_queue.join()

        # Wait for threads to finish
        for thread in threads:
            thread.join()

        # Finilize
        session.executed_apps = ", ".join(sorted(executed_apps))
        session.finalize()
    
    @staticmethod
    def execute_scenarios(base_url, base_url_key, app_name=None, scenario_name=None):
        scenarios = ScenarioService.find_scenarios(app_name, scenario_name)
        
        if len(scenarios) >= settings.THREAD_WORKERS:
            # Randomize the order of the scenarios so all the scenarios which are using 'Lock', wont be next to eachother
            # random.shuffle(scenarios)
            return ScenarioService._execute_scenarios_thread(scenarios, base_url, base_url_key)
        else:
            return ScenarioService._execute_scenarios_one_by_one(scenarios, base_url, base_url_key)
        
    @staticmethod
    def get_includable_apps() -> list:
        """
        Returns a list of app names created using `manage.py startapp`.
        Excludes:
        - Built-in Django apps (e.g., `django.contrib.*`)
        - Third-party apps (e.g., `rest_framework`, `drf_yasg`)
        """

        # Ensure project_root is a string
        project_root = str(settings.BASE_DIR)

        includable_apps = []
        for app in settings.INSTALLED_APPS:
            try:
                app_module = importlib.import_module(app)
                app_path = os.path.dirname(app_module.__file__)
                app_path = str(app_path)
                # Check if the app is inside the project root
                if app_path.startswith(project_root):
                    includable_apps.append(app)
            except (ImportError, AttributeError):
                continue

        # Exclude Django and third-party apps
        excluded_prefixes = ("django.", "rest_framework", "drf_yasg")
        excluded_apps = {
            settings.ROOT_URLCONF.split('.')[0],  # Main app
            "scenario_tester",
        }

        return [
            app
            for app in includable_apps
            if not app.startswith(excluded_prefixes) and app not in excluded_apps
        ]


class time:
    @staticmethod
    def current_time(format="%Y-%m-%d %H:%M:%S") -> str:
        return datetime.now().strftime(format)
    
    
class TestAllScenariosService:
    ENVIRONMENT_URLS = {
            "Development": settings.VION_DEVELOP_URL,
            "Staging": settings.VION_STAGIN_URL,
            "Local": settings.VION_LOCAL_URL, 
        }

    def _params_validation(self, base_url_key, app_name=None, scenario_name=None) -> str:
        self._validate_base_url(base_url_key)
        base_url = self._get_environmental_urls(base_url_key, self.ENVIRONMENT_URLS)
        self._validate_base_url(base_url)
        self._validate_scenario_and_app(app_name, scenario_name)
        return base_url
        
    
    def _get_environmental_urls(self, base_url_key, environment_urls) -> str:
        return environment_urls.get(base_url_key)
    
    def get_environmental_keys(self) -> str:
        return self.ENVIRONMENT_URLS.keys()
    
    def _validate_base_url(self, base_url_key):
        if not base_url_key:
            raise URLValidationException()
        
    def _validate_scenario_and_app(self, app_name, scenario_name):
        if scenario_name and not app_name:
            raise ScenarioWithNotAppException()
        
    def execute_scenarios(self, base_url_key, app_name=None, scenario_name=None):
        base_url = self._params_validation(base_url_key, app_name, scenario_name)
        try:
            ScenarioService.execute_scenarios(base_url, base_url_key, app_name=app_name, scenario_name=scenario_name)
            session = self._get_created_session()
            redirect_url = self._redirect_to_session_detail_url(session.id)
            return redirect(redirect_url)
        except Exception as e:
            print(e)
            raise UnexpectedErrorException()
    
    def _get_created_session(self):
        return Session.objects.latest("id")
    
    def _redirect_to_session_detail_url(self, session_id):
        return reverse("session-detail", kwargs={"pk": session_id})
    
    
test_all_scenarios_service = TestAllScenariosService()