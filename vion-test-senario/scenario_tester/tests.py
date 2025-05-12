from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import Session
from .serializers import SessionSerializer

class SessionDetailViewTests(TestCase):
    def setUp(self):
        self.session = Session.objects.create(
            server="Test Server",
            executed_apps="Test App",
            start_time="2025-01-21T08:23:58.939193Z",
            end_time="2025-01-21T08:24:08.998305Z",
        )
        self.url = reverse("session-detail", kwargs={"pk": self.session.id})
    
    def test_get_session_details(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        expected_data = SessionSerializer(self.session).data
        self.assertEqual(res.data, expected_data)
    
    def test_get_session_details_invalid_id(self):
        url = reverse("session-detail", kwargs={"pk": 999})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

class TestAllScenariosViewTests(TestCase):
    def setUp(self):
        self.url = reverse("test-all-scenarios")
        self.valid_data = {
            "base_url": "Local",
            "app_name": "gallery",
            "scenario_name": "CreateGallery"
        }
        self.invalid_data = {
            "base_url": "",
            "app_name": "gallery",
            "scenario_name": "CreateGallery"
        }
    
    def test_valid_data(self):
        res = self.client.get(self.url, self.valid_data)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_missing_base_url(self):
        res = self.client.get(self.url, self.invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"].code, "invalid-url")

    def test_invalid_base_url(self):
        invalid_data = self.valid_data.copy()
        invalid_data["base_url"] = "InvalidBaseUrl"
        res = self.client.get(self.url, invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"].code, "invalid-url")

    def test_scenario_name_without_app_name(self):
        invalid_data = self.valid_data.copy()
        invalid_data["app_name"] = ""
        res = self.client.get(self.url, invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"].code, "invalid-scenario")
        