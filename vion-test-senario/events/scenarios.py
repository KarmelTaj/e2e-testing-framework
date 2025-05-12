from scenario_tester.scenarios import BaseScenario
from .endpoints import EventEndpoints
from scenario_tester.assertions import Assert
from scenario_tester.services import time


class BaseEventScenario(BaseScenario):
    def is_abstract(self):
        return True

    def create_or_get_event(self, filters):
        """
        Fetch an existing event based on filters. If none exists, create a new event, then fetch it using its unique attributes.
        """
        # Search for existing events
        response_json, status_code = self.call(EventEndpoints.LIST_EVENTS, params=filters)
        Assert.assertEqual(status_code, 200)

        if response_json and response_json["count"] > 0:
            event = response_json["results"][0]  # Return the first matching event
        else:
            # Create a new event
            created_event = self.setup_event()
            unique_filters = {
                "title": created_event["title"],
                "category": created_event["category"]["id"],
                "subcategory": created_event["subcategory"]["id"],
            }
            response_json, status_code = self.call(EventEndpoints.LIST_EVENTS, params=unique_filters)
            Assert.assertEqual(status_code, 200)

            if response_json and response_json["count"] > 0:
                event = response_json["results"][0]  # Fetch the newly created event
            else:
                raise ValueError("Failed to fetch the newly created event.")
        
        return event

    def setup_event(self):
        """
        Performs additional setup for a newly created event.
        """
        # Create a new event
        current_time = time.current_time()
        event_data = {
            "title":f"[Event] {current_time}",
            "public":True,
            "start_at":"2026-01-01T00:00",
            "end_at":"2026-12-31T00:00",
            "preferred_timezone":"CET",
            "online":True,
            "venue_gallery_id":12,
            "team_members":[],
            "category_id":1,
            "link_address": "https://site.com",
            "street":"address",
            "headquarter_as_organizer":True,
            "subcategory_id":4,
            "featured_image_id":2,
            "description":"<p>Description</p>",
            "agenda":None
        }
        event_response_json, status_code = self.call(EventEndpoints.CREATE_EVENT, event_data)
        Assert.assertEqual(status_code, 201)
        event = event_response_json

        # Create a ticket
        ticket_data = {
            "ticket_name_id": 3,
            "available_from": "2025-01-01T00:00",
            "available_to": "2025-12-31T00:00",
            "description": "Description",
        }
        ticket_endpoint = self.format_endpoint(EventEndpoints.CREATE_TICKET, event_slug=event["slug"])
        _, status_code = self.call(ticket_endpoint, ticket_data)
        Assert.assertEqual(status_code, 201)

        # Create booking settings
        booking_data = {
            "billing_salutation": "D",
            "billing_title": "D",
            "billing_phone": "M",
            "billing_company": "O",
            "billing_vat_uid_no": "O",
            "external_link_enabled": False,
            "minimum_age_enabled": True,
            "salutation": "D",
            "title": "O",
            "country": "O",
            "city": "M",
            "street": "M",
            "zip_code": "M",
            "double_room": "D",
            "arrival_before": "D",
            "translation": "D",
            "tshirt_size": "D",
            "order_notes": "D",
            "discipline": "D",
            "disclaimer_liability": False,
            "translation_czech": False,
            "translation_slovenia": False,
            "translation_english": False,
            "credit_card_enabled": True,
            "sofort_enabled": True,
            "event": event["id"],
            "mwst_percentage": 0,
            }
        _, status_code = self.call(EventEndpoints.CREATE_BOOKING_SETTING, booking_data)
        Assert.assertEqual(status_code, 201)

        # Create a confirmation message
        message_data = {
            "event": event["id"],
            "message": "<h1>Thank You!</h1>",
            "receipt": True,
            "ticket": True,
            "program": True,
            "email_receipt": True,
            "email_ticket": True,
            "email_program": True,
        }
        _, status_code = self.call(EventEndpoints.CREATE_MESSAGE, message_data)
        Assert.assertEqual(status_code, 201)

        # Schedule the event
        schedule_data = {
            "publish_start_at":"2025-01-01T00:00",
            "publish_end_at":"2025-12-31T00:00",
            "verified":True
        }
        schedule_endpoint = self.format_endpoint(EventEndpoints.SCHEDULE_EVENT, event_slug=event["slug"])
        _, status_code = self.call(schedule_endpoint, schedule_data)
        Assert.assertEqual(status_code, 200)

        return event

    def get_ticket(self, event):
        tickets_endpoint = self.format_endpoint(EventEndpoints.LIST_TICKETS, event_slug=event["slug"])
        response_json, status_code = self.call(tickets_endpoint)
        Assert.assertEqual(status_code, 200)
        tickets = response_json.get("results", [])
        ticket = next((ticket for ticket in tickets if ticket.get("available")), None)
        if not ticket:
            raise ValueError("Ticket: " + response_json.get("detail"))
        return ticket


class SimpleEventRegistrationScenario(BaseEventScenario):
    """
    Gets an event with the given filters and if there is none, creates one. Registers to that event with a partner user and gets the PDF
    """
    def is_abstract(self):
        return False

    def run(self):
        # Login as backoffice user
        _, status_code = self.login("backoffice", EventEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Create or get event
        filters = {
            "title": "[Event]",       
            "verified": True,
            "category": 1, # Business opening
            "online": True,
        }
        event = self.create_or_get_event(filters)
        Assert.assertIn("id", event)
        Assert.assertIn("slug", event)
        Assert.assertIn("category", event)
        Assert.assertIn("title", event)
        Assert.assertIn("public", event)
        Assert.assertIn("start_at", event)
        Assert.assertIn("end_at", event)
        Assert.assertIn("online", event)
        Assert.assertIn("verified", event)
        Assert.assertIn("verified_display", event)
        Assert.assertIn("preferred_timezone", event)
        Assert.assertGreaterThan(event["end_at"], event["start_at"])

        # Get ticket for event
        ticket = self.get_ticket(event)
        
        Assert.assertIn("id", ticket)
        Assert.assertIn("slug", ticket)
        Assert.assertIn("name", ticket)
        Assert.assertIn("available_from", ticket)
        Assert.assertIn("available_to", ticket)
        Assert.assertIn("visible", ticket)
        Assert.assertIn("available", ticket)
        Assert.assertIn("gross_price", ticket)
        Assert.assertLessThan(ticket["available_from"], ticket["available_to"])
        Assert.assertEqual(ticket["available"], True)

        # Log in as partner user
        self.logout()
        _, status_code = self.login("partner1", EventEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Register attendee
        registration_data = {
            "first_name": "New Participant",
            "last_name": "New Participant last name",
            "phone": "+989976645234",
            "email": "some@email.com",
            "country": "AU",
            "city": "london",
            "street": "address",
            "zip_code": "11123",
            "directorate_no_number": "101",
            "partner_id": "103",
            "invited_by": "Sina Nazemi",
            "birthdate": "1987-01-01",
            "event_id": event["id"],
            "registration_type": "guest",
            "ticket_id": ticket["id"],
        }
        registration, status_code = self.call(EventEndpoints.REGISTER_ATTENDEE, registration_data)
        
        Assert.assertEqual(status_code, 201)
        Assert.assertIn("id", registration)
        Assert.assertIn("slug", registration)
        Assert.assertIn("event", registration)
        Assert.assertIn("ticket", registration)
        Assert.assertIn("registration_type", registration)

        # Fetch PDF
        pdf_endpoint = self.format_endpoint(EventEndpoints.FETCH_PDF_URL, registration_slug=registration["slug"])
        pdf, status_code = self.call(pdf_endpoint)
        
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("ticket", pdf)
