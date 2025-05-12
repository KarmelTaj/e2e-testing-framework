from scenario_tester.endpoints import EndPoint, HTTPMethods

class OrgaSessionEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    
    CREATE_CONTACT = EndPoint(HTTPMethods.POST, "/network/contacts/")
    GET_CONTACTS_LIST = EndPoint(HTTPMethods.GET, "/network/contacts/")
    DELETE_CONTACT = EndPoint(HTTPMethods.DELETE, "/network/contacts/{slug}/")
    
    CREATE_ORGA_SESSION = EndPoint(HTTPMethods.POST, "/network/orga-session/")
    GET_ORGA_SESSION = EndPoint(HTTPMethods.GET, "/network/orga-session/{id}/")
    DELETE_ORGA_SESSION = EndPoint(HTTPMethods.DELETE, "/network/orga-session/{id}/")
    GET_ORGA_SESSION_STATISTICS = EndPoint(HTTPMethods.GET, "/network/orga-sessions-statistics/{id}/")
    
    CREATE_APPOINTMENTS = EndPoint(HTTPMethods.POST, "/appointments/appointment/")