from typing import Tuple, Dict
import requests
from django.utils import timezone
from .endpoints import HTTPMethods, EndPoint
from scenario_tester.models import Scenario
from .credentials import CREDENTIALS
from .utils import get_environment
from threading import Lock


class BaseScenario:
    BASE_URL = None  # Should be overridden by subclasses
    shared_resource_lock = Lock()
    
    def __init__(self, base_url: str):
        self.BASE_URL = base_url.rstrip("/")
        self.headers = {}
        self.scenario = None
        self._step = None
        
    def set_step(self, step: str):
        """
        Setter for the current step
        """
        self._step = step

    def login(self, role: str, login_endpoint: EndPoint) -> Tuple[Dict, int]:
        environment = get_environment(self.BASE_URL) # ("development", "staging", "local")
        credentials = CREDENTIALS.get(environment, {}).get(role, {})
        if not credentials:
            raise ValueError(f"Credentials for role '{role}' in environment '{environment}' are not configured.")

        data = {
            "username": credentials["username"],
            "password": credentials["password"],
        }

        response_json, status_code = self.call(login_endpoint, data)

        if status_code == 200:
            if "access" in response_json:
                self.headers["Authorization"] = f"Bearer {response_json['access']}"
            else:
                raise KeyError("The response does not contain an 'access' token.")
        return response_json, status_code

    def logout(self):
        self.headers.pop("Authorization", None)

    def _create_log(self, level: str, message: str):
        """
        Creates and adds a log to the current scenario.

        Args:
            level: The log level ("debug", "info", "warning", "error").
            message: The log message.
        """
        if not self.scenario:
            raise RuntimeError("No scenario instance is set. Logs cannot be created.")
        log_message = f"({self._step}) {message}" if self._step else message
        self.scenario.logs.create(level=level, text=log_message)
    
    # Methods for logging
    def info(self, message: str):
        self._create_log("info", message)

    def debug(self, message: str):
        self._create_log("debug", message)

    def warning(self, message: str):
        self._create_log("warning", message)
        
    def error(self, message: str):
        self._create_log("error", message)


    def call(self, endpoint: EndPoint, params=None, files=None) -> Tuple[Dict, int]:
        """
        Makes an API call to the given endpoint with optional parameters.
        Returns a tuple (response_content, response_status_code).
        """
        url = f"{self.BASE_URL}{endpoint.url}"
        method = endpoint.method

        try:
            match method:
                case HTTPMethods.GET:
                    response = requests.get(url, headers=self.headers, params=params)
                case HTTPMethods.POST:
                    if files:  # For file uploads
                        response = requests.post(url, headers=self.headers, data=params, files=files)
                    else:
                        response = requests.post(url, headers=self.headers, json=params)
                case HTTPMethods.PUT:
                    response = requests.put(url, headers=self.headers, json=params)
                case HTTPMethods.DELETE:
                    response = requests.delete(url, headers=self.headers, params=params)
                case HTTPMethods.PATCH:
                    response = requests.patch(url, headers=self.headers, json=params)
                case _:
                    raise ValueError(f"Unsupported HTTP method: {method}")

            # Response content type
            content_type = response.headers.get("Content-Type", "")
            
            if "application/json" in content_type:  # JSON response
                try:
                    response_json = response.json() if response.content else None
                except ValueError:
                    raise ValueError(
                        f"Failed to parse JSON response.\n"
                        f"URL: {url}\nMethod: {method}\nStatus Code: {response.status_code}\n"
                        f"Response Content: {response.text}"
                    )
                return response_json, response.status_code
            elif "application/pdf" in content_type:  # PDF response
                return response.content, response.status_code
            else:
                return None, response.status_code

        except requests.exceptions.RequestException as req_err:
            raise RuntimeError(
                f"Request failed with error: {req_err}\nURL: {url}\nMethod: {method}\nParams: {params}"
            )
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred: {e}\nURL: {url}\nMethod: {method}\n"
            )
            
    def execute(self, session):
        """
        Executes the scenario:
        - Creates a `Scenario` instance.
        - Runs the scenario logic by calling `self.run()`.
        - Finalizes the scenario, setting its status based on success or failure.
        """
        with self.shared_resource_lock:
            self.scenario = Scenario.objects.create(
                session=session,
                start_time=timezone.now(),
                scenario_name=self.__class__.__name__,
            )
        try:
            self.run()
            with self.shared_resource_lock:
                self.scenario.status = "passed"
        except AssertionError as assert_err:
            with self.shared_resource_lock:
                self.scenario.status = "failed"
            self.error(f"Failed: {str(assert_err)}")
        except Exception as e:
            with self.shared_resource_lock:
                self.scenario.status = "error"
            self.error(f"Error: {str(e)}")
        finally:
            with self.shared_resource_lock:
                self.scenario.finalize()
    
    def run(self):
        """
        Override in subclasses
        """
        raise NotImplementedError("This method must be overridden in subclasses.")

    def format_endpoint(self, endpoint: EndPoint, **kwargs) -> EndPoint:
        formatted_url = endpoint.url.format(**kwargs)
        return EndPoint(endpoint.method, formatted_url)

    def is_abstract(self) -> bool:
        """
        Classes will be listed in the `find_scenarios` service based on this function.
        """
        return True
