from django.utils.translation import gettext_lazy as _
from test_api_vion.exceptions import BadRequestException, GeneralAPIException

class URLValidationException(BadRequestException):
    default_detail = _("Correct Base URL is required.")
    default_code = "invalid-url"
    
class ScenarioWithNotAppException(BadRequestException):
    default_detail = _("The 'scenario_name' parameter requires an 'app_name' to be provided.")
    default_code = "invalid-scenario"
    
class UnexpectedErrorException(GeneralAPIException):
    default_detail = _("An unexpected error occurred")
    default_code = "unexpected-error"