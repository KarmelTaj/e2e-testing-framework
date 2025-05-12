from django.urls import re_path
from django.utils.decorators import method_decorator
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Scenario Tester",
        default_version='v1',
        description="Test Scenarios description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_urlpatterns = [
    re_path('swagger/', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
   ]

def swagger_http(http_method, desc, **kwargs):
    return swagger_msg(desc=desc, operation=http_method, **kwargs)

def swagger_msg(desc, serializer_class=None, responses=None, operation=None, additional_responses=None, **kwargs):
    if not responses:
        responses = {} if serializer_class is None else {200: serializer_class()}

    if additional_responses:
        responses.update(additional_responses)

    manual_parameters = kwargs.pop("manual_parameters", [])
    schema = swagger_auto_schema(
        operation_description=desc, responses=responses, manual_parameters=manual_parameters, **kwargs
    )
    return schema if operation is None else method_decorator(name=operation, decorator=schema)
