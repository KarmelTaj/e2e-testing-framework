from rest_framework.views import APIView
from rest_framework import generics

from .services import ScenarioService, test_all_scenarios_service
from .utils import create_swagger_param
from .models import Session
from .serializers import SessionSerializer

from test_api_vion.swagger import swagger_http


app_name_manual_param = create_swagger_param(
    name="app_name",
    description="Filter scenarios by app name (e.g., 'gallery'). Leave blank to execute all scenarios.",
    required=False,
    enum=ScenarioService.get_includable_apps(),
)

base_url_manual_param = create_swagger_param(
    name="base_url",
    description="Select the base URL for the scenarios.",
    required=True,
    enum=list(test_all_scenarios_service.get_environmental_keys()),  # ("Development", "Staging", "Local")
)

scenario_name_manual_param = create_swagger_param(
    name="scenario_name",
    description=(
        "Filter scenarios by scenario name within the specified app. "
        "Requires 'app_name' to be provided. Leave blank to execute all scenarios in the app."
    ),
    required=False,
)


class SessionDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific session
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


@swagger_http(
    "get",
    "Executes all scenarios, filters by app name, or filters by a specific scenario name within an app",
    manual_parameters=[base_url_manual_param, app_name_manual_param, scenario_name_manual_param],
)
class TestAllScenariosView(APIView):
    def get(self, request):
        app_name = request.query_params.get("app_name", None)
        scenario_name = request.query_params.get("scenario_name", None)
        base_url_key = request.query_params.get("base_url")

        return test_all_scenarios_service.execute_scenarios(base_url_key, app_name=app_name, scenario_name=scenario_name)