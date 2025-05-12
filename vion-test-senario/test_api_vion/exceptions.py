from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class GeneralAPIException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("General API exception has happened.")
    default_code = "general-api-exception"
    
class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The request had some problem.")
    default_code = "bad-request-exception"