from scenario_tester.endpoints import EndPoint, HTTPMethods

class SalesEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    PRIVACY_POLICY = EndPoint(HTTPMethods.POST, "/wishes_and_goals/")
    CONTACT_DETAILS = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/contact-details/{slug}/")
    GOALS = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/goals/{slug}/")
    HOUSEHOLD_BILL = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/household-bill/{slug}/")
    ASSET_LIABILITY = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/asset-liability/{slug}/")
    SAVING_MONEY = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/saving-money/{slug}/")
    FEEDBACK = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/feedback/{slug}/")
    FINALIZE = EndPoint(HTTPMethods.PUT, "/wishes_and_goals/finalize/{slug}/")
    PDF = EndPoint(HTTPMethods.GET, "/wishes_and_goals/download-summary-pdf/{slug}/")
    DELETE_FORM = EndPoint(HTTPMethods.DELETE, "/wishes_and_goals/{slug}/")
    GET_FORM = EndPoint(HTTPMethods.GET, "/wishes_and_goals/{slug}/")