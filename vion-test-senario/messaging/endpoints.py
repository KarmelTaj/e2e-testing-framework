from scenario_tester.endpoints import EndPoint, HTTPMethods

class MessagingEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    GET_PROFILE = EndPoint(HTTPMethods.GET, "/auths/profile/")
    SEND_PRIVATE_MESSAGE = EndPoint(HTTPMethods.POST, "/messaging/private/send/")
    DELETE_PRIVATE_MESSAGE = EndPoint(HTTPMethods.DELETE, "/messaging/message/{id}/")
    