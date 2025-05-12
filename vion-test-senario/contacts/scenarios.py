from scenario_tester.scenarios import BaseScenario
from .endpoints import ContactsEndpoints
from scenario_tester.assertions import Assert
from scenario_tester.services import time

class ContactsTestScenario(BaseScenario):
    """
    Create and test Contact module
    """
    def run(self):
        # Log in as partner
        self.set_step("Step 1: Login")
        _, status_code = self.login("partner1", ContactsEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Create Contact
        self.set_step("Step 2: Create Contact")
        contact_data = self.setup_contact()
        contact, status_code = self.call(ContactsEndpoints.CREATE_CONTACT, contact_data)
        Assert.assertEqual(status_code, 201)
        Assert.assertIn("id", contact)
        Assert.assertIn("slug", contact)

        # Update Contact
        self.set_step("Step 3: Update Contact")
        contact_slug = contact["slug"]
        update_fields_data = {
            "message_type": "F",
            "country": "DE",
            "city": "City",
            "potential": 5,
        }
        updated_data = self.update_contact_data(contact_data.copy(), update_fields_data)
        update_contact_endpoint = self.format_endpoint(ContactsEndpoints.UPDATE_CONTACT, contact_slug=contact_slug)
        _, status_code = self.call(update_contact_endpoint, updated_data)
        Assert.assertEqual(status_code, 200)

        # Bad data tests with invalid values
        self.set_step("Step 4: Bad Data tests")
        bad_data_tests = [
            {"country": "InvalidCountry"},
            {"emails": [{"type": "Work", "email": "invalid-email"}]},
            {"is_business_partner": "not-a-boolean"},
            {"is_customer": "invalid-boolean"},
            {"is_prospect_customer": None},
            {"is_prospect_partner": 123},
            {"message_type": "InvalidType"},
            {"phones": [{"type": "40_OTHER", "number": "invalid-phone"}]},
            {"zip_code": "invalid-zip"},
        ]

        for bad_data in bad_data_tests:
            update_data = self.update_contact_data(updated_data.copy(), bad_data)
            _, status_code = self.call(update_contact_endpoint, update_data)
            Assert.assertEqual(status_code, 400, f"Mismatch in {bad_data.keys()}. Expected 400, but got {status_code}")
            updated_data = update_data

        # Delete Contact
        self.set_step("Step 5: Delete Contact")
        delete_contact_endpoint = self.format_endpoint(ContactsEndpoints.DELETE_CONTACT, contact_slug=contact_slug)
        _, status_code = self.call(delete_contact_endpoint)
        Assert.assertEqual(status_code, 204)

    def setup_contact(self) -> dict:
        """
        Initialize default contact data for creation.
        """
        return {
            "message_type": "I",
            "is_prospect_customer": True,
            "is_prospect_partner": True,
            "is_customer": False,
            "is_business_partner": True,
            "potential": None,
            "country": "AE",
            "first_name": "[Contact]",
            "last_name": f"{time.current_time()}",
            "phones": [
                {"type": "40_OTHER", "number": "+684685", "error": False},
                {"type": "40_OTHER", "number": "+6151651668", "error": False},
                {"type": "40_OTHER", "number": "+4688165168", "error": False}
            ],
            "emails": [
                {"type": "Other", "email": "1th@email.com", "error": False},
                {"type": "Work", "email": "2th@email.com"},
                {"type": "Private", "email": "3th@email.com", "error": False}
            ],
            "street": "Street",
            "zip_code": "11111",
            "city": "awdawd",
            "source": "Rc",
            "interests": [
                {"title": "Interest 1"},
                {"title": "Interest 2"},
                {"title": "Interest 3"},
                {"title": "Interest 4"}
            ],
            "note": "Some Note"
        }

    def update_contact_data(self, base_data: dict, updates: dict) -> dict:
        """
        Update base contact data with values from the updates dictionary.
        """
        if base_data is None:
            raise ValueError("Base data cannot be None")
        for key, value in updates.items():
            if key in base_data:
                base_data[key] = value
        return base_data
