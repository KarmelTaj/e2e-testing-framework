from django.conf import settings
from drf_yasg import openapi
from drf_yasg.openapi import IN_QUERY, TYPE_STRING

def get_environment(base_url: str) -> str:
    if base_url == settings.VION_DEVELOP_URL:
        return "development"
    elif base_url == settings.VION_STAGIN_URL:
        return "staging"
    elif base_url == settings.VION_LOCAL_URL:
        return "local"
    else:
        raise ValueError("Unknown base_url provided.")


def create_swagger_param(name, description, required, param_type=TYPE_STRING, in_=IN_QUERY, enum=None):
    """
    Utility function to create a Swagger parameter.
    """
    return openapi.Parameter(
        name=name,
        in_=in_,
        description=description,
        type=param_type,
        required=required,
        enum=enum,
    )