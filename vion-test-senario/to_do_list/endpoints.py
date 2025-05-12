from scenario_tester.endpoints import EndPoint, HTTPMethods

class ToDoListEndpoints:
    # ------------------- Partner -------------------
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    CREATE_TO_DO_LIST = EndPoint(HTTPMethods.POST, "/todo/series/partner/")
    GET_TO_DO_LIST_BY_TITLE = EndPoint(HTTPMethods.GET, "/todo/items/manage/partner/")
    GET_TO_DO_LIST_BY_TITLE_FOR_TEAM = EndPoint(HTTPMethods.GET, "/todo/items/partner/")
    DELETE_TO_DO_LIST = EndPoint(HTTPMethods.DELETE, "/todo/series/partner/{slug}/")
    UPDATE_TO_DO_LIST = EndPoint(HTTPMethods.PUT, "/todo/series/partner/{slug}/")
    FINISH_TASK = EndPoint(HTTPMethods.POST, "/todo/logs/partner")

    # ------------------- Backoffice -------------------
    GET_PROFLE = EndPoint(HTTPMethods.GET, "/auths/profile/")
    CREATE_TO_DO_LIST_BACKOFFICE = EndPoint(HTTPMethods.POST, "/todo/series/backoffice/")
    GET_TO_DO_LIST_BY_TITLE_BACKOFFICE = EndPoint(HTTPMethods.GET, "/todo/items/manage/backoffice/")
    UPDATE_TO_DO_LIST_BACKOFFICE = EndPoint(HTTPMethods.PUT, "/todo/series/backoffice/{slug}/")
    DELETE_TO_DO_LIST_BACKOFFICE = EndPoint(HTTPMethods.DELETE, "/todo/series/backoffice/{slug}/")
    