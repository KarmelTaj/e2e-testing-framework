from scenario_tester.scenarios import BaseScenario
from scenario_tester.assertions import Assert
from scenario_tester.services import time
from .endpoints import GalleryEndpoints
import os
from django.apps import apps


class CreateGallery(BaseScenario):
    def run(self):
        # Login as backoffice user
        _, status_code = self.login("backoffice", GalleryEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Create gallery details
        current_time = time.current_time()
        gallery_details_data = {
            "section": "event",
            "title": f"[Gallery] {current_time}",
            "show_on_community": True,
            "marked_as_venue": False,
            "event_title": "event title",
            "venue": "place",
            "start_at": "2024-01-01T00:00:00+03:30",
            "end_at": "2026-01-01T00:00:00+03:30",
        }
        gallery_response, status_code = self.call(GalleryEndpoints.GALLERY_DETAILS, gallery_details_data)
        Assert.assertEqual(status_code, 201)
        
        # Upload and add images to gallery
        image_paths = [
            "brainstorm.jpg",
            "coffee-time.jpg",
            "planning.jpg",
            "work-setup.jpg",
            "work-team.jpg",
        ]
        uploaded_images_uuids = self.upload_images(image_paths)
        # Save the image IDs to a list if we wanted to set one as Cover Image
        image_IDs = self.add_media_to_gallery(gallery_response["id"], uploaded_images_uuids, media_type="image")
        
        # Set an image as Cover Image
        cover_image_id = image_IDs[1]
        cover_image_endpoint = self.format_endpoint(GalleryEndpoints.SET_COVER_IMAGE, id=cover_image_id)
        _, status_code = self.call(cover_image_endpoint, {})
        Assert.assertEqual(status_code, 200)
        
        # Pin an image to dashboard
        pin_image_endpoint = self.format_endpoint(GalleryEndpoints.PIN_TO_DASHBOARD, id=image_IDs[0])
        pin_response, status_code = self.call(pin_image_endpoint, self.pin_to_dashboard_data(True))
        Assert.assertEqual(status_code, 200)
        
        # Add videos to gallery
        video_paths = [
            r"https://www.youtube.com/watch?app=desktop&v=28TwDsxpRvQ",
            r"https://www.youtube.com/watch?app=desktop&v=tJe-YdQo4lc",
            r"https://www.youtube.com/watch?v=9CAz_vvsK9M",
        ]
        self.add_media_to_gallery(gallery_response["id"], video_paths, media_type="video")
        
        # Log in as partner
        self.logout()
        _, status_code = self.login("partner1", GalleryEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)
        
        media_endpoint = self.format_endpoint(GalleryEndpoints.GET_MEDIA, gallery_slug=gallery_response["slug"])
        gallery_response, status_code = self.call(media_endpoint)
        Assert.assertEqual(status_code, 200)
        
        # Check if the cover image matches
        Assert.assertIn("id", gallery_response["featured_image"])
        Assert.assertEqual(gallery_response["featured_image"]["id"], cover_image_id)
        
        # Log in as backoffice to delete the gallery
        self.logout()
        _, status_code = self.login("backoffice", GalleryEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)
        
        delete_media_endpoint = self.format_endpoint(GalleryEndpoints.DELETE_MEDIA, gallery_slug=gallery_response["slug"])
        _, status_code = self.call(delete_media_endpoint)
        Assert.assertEqual(status_code, 204)
        
        # Log in as partner to see if any gallery exists
        self.logout()
        _, status_code = self.login("partner1", GalleryEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        _, status_code = self.call(media_endpoint)
        Assert.assertEqual(status_code, 404)

    def upload_images(self, image_names: list) -> list:
        """
        Uploads a list of images from the gallery/photos folder and returns the UUIDs.
        """
        uploaded_images = []
        photos_dir = os.path.join(apps.get_app_config("gallery").path, "photos")
        
        for image_name in image_names:
            image_path = os.path.join(photos_dir, image_name)
            try:
                with open(image_path, "rb") as file:
                    files = {"file": file}
                    response, status_code = self.call(GalleryEndpoints.FILECENTER_PHOTO, params=None, files=files)
                    Assert.assertEqual(status_code, 201)
                    uploaded_images.append(response["uuid"])
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {image_path}")
            except Exception as e:
                raise Exception(f"An error occurred while uploading the image: {e}")
        return uploaded_images

    def add_media_to_gallery(self, gallery_id: int, media_items: list, media_type: str):
        """
        Associates media items (images or videos) with the gallery.

        Args:
            gallery_id: ID of the gallery.
            media_items: List of media items (UUIDs for images or URLs for videos).
            media_type: Type of media ("image" or "video").
        """
        media_payload = []
        if media_type == "image":
            media_payload = [
                {
                    "title": "Add image title",
                    "alternative_text": "Add image Alt title",
                    "type": "image",
                    "gallery_id": gallery_id,
                    "image_file": item,
                }
                for item in media_items
            ]
        elif media_type == "video":
            media_payload = [
                {
                    "title": "YT Title",
                    "alternative_text": "Alt YT Text",
                    "type": "video",
                    "gallery_id": gallery_id,
                    "video_url": item,
                }
                for item in media_items
            ]
        else:
            raise ValueError("Unsupported media type. Use 'image' or 'video'.")

        json_response, status_code = self.call(GalleryEndpoints.MEDIA_GALLERY, media_payload)
        Assert.assertEqual(status_code, 201)
        if media_type == "image": 
            media_IDs = [media["id"] for media in json_response]
            return media_IDs

    def pin_to_dashboard_data(self, is_pinned: bool) -> dict:
        """
        Creates the data needed for pinning an image to the dashboard.
        """
        return {"pin_to_dashboard": str(is_pinned)}
