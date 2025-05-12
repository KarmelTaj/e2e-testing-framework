from scenario_tester.endpoints import EndPoint, HTTPMethods

class EventEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    CREATE_EVENT = EndPoint(HTTPMethods.POST, "/events/event/")
    SCHEDULE_EVENT = EndPoint(HTTPMethods.PUT, "/events/{event_slug}/schedule/")
    CREATE_TICKET = EndPoint(HTTPMethods.POST, "/ticket/{event_slug}/")
    CREATE_BOOKING_SETTING = EndPoint(HTTPMethods.POST, "/events/booking-setting/")
    CREATE_MESSAGE = EndPoint(HTTPMethods.POST, "/events/confirm-message/")
    REGISTER_ATTENDEE = EndPoint(HTTPMethods.POST, "/events/attendee/registration/")
    FETCH_PDF_URL = EndPoint(HTTPMethods.GET, "/events/attendees/{registration_slug}/files")
    LIST_EVENTS = EndPoint(HTTPMethods.GET, "/events/list/")
    LIST_TICKETS = EndPoint(HTTPMethods.GET, "/ticket/{event_slug}")