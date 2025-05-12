from scenario_tester.endpoints import EndPoint, HTTPMethods

class GalleryEndpoints:
    LOGIN = EndPoint(HTTPMethods.POST, "/auths/token/")
    GALLERY_DETAILS = EndPoint(HTTPMethods.POST, "/gallery/gallery/")
    FILECENTER_PHOTO = EndPoint(HTTPMethods.POST, "/filecenter/photo/")
    MEDIA_GALLERY = EndPoint(HTTPMethods.POST, "/gallery/media/")
    GET_MEDIA = EndPoint(HTTPMethods.GET, "/gallery/gallery-and-media/{gallery_slug}")
    DELETE_MEDIA = EndPoint(HTTPMethods.DELETE, "/gallery/gallery/{gallery_slug}")
    SET_COVER_IMAGE = EndPoint(HTTPMethods.PATCH, "/gallery/media/{id}/set-as-gallery-cover/")
    PIN_TO_DASHBOARD = EndPoint(HTTPMethods.PATCH, "/gallery/media/{id}/pin-to-dashboard/")