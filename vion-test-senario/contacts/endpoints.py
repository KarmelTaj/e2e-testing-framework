from scenario_tester.endpoints import EndPoint, HTTPMethods

class ContactsEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    LIST_CONTACTS = EndPoint(HTTPMethods.GET, "/network/contacts/")
    CREATE_CONTACT = EndPoint(HTTPMethods.POST, "/network/contacts/")
    GET_CONTACT = EndPoint(HTTPMethods.GET, "/network/contacts/{contact_slug}/")
    UPDATE_CONTACT = EndPoint(HTTPMethods.PATCH, "/network/contacts/{contact_slug}/")
    DELETE_CONTACT = EndPoint(HTTPMethods.DELETE, "/network/contacts/{contact_slug}/")
    