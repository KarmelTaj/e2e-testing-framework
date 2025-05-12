from scenario_tester.endpoints import EndPoint, HTTPMethods

class ConceptsEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    CONCEPT = EndPoint(HTTPMethods.POST, "/concepts/")
    UPDATE_CONCEPT = EndPoint(HTTPMethods.PATCH, "/concepts/{concept_slug}/")
    DELETE_CONCEPT = EndPoint(HTTPMethods.DELETE, "/concepts/{concept_slug}/")
    GET_CONCEPT = EndPoint(HTTPMethods.GET, "/concepts/{concept_slug}/")
    RECOMMENDATIONS = EndPoint(HTTPMethods.POST, "/concepts/{concept_slug}/recommendations/")
    RECOMMENDATIONS_UPDATE = EndPoint(HTTPMethods.PUT, "/concepts/{concept_slug}/recommendations/{id}/")
    GENERATE_PDF = EndPoint(HTTPMethods.POST, "/concepts/{concept_slug}/generate/")
    