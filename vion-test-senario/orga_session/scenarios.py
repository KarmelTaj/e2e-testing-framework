from scenario_tester.scenarios import BaseScenario
from .endpoints import OrgaSessionEndpoints
from scenario_tester.assertions import Assert
from scenario_tester.services import time


class OrgaSessionTestScenario(BaseScenario):
    """
    Test Orga-session
    """

    def run(self):
        # Log in as partner
        self.set_step("Login")
        _, status_code = self.login("partner2", OrgaSessionEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Get Contacts
        self.set_step("Get Contacts and Phones")
        contact_data = {
            "first_name": "Contact 1",
            "last_name": "Last Name",
            "phones": [
                {
                    "title": "Phone 1",
                    "number": "1111111111"
                },
                {
                    "title": "Phone 2",
                    "number": "2222222222"
                }
            ]
        }
        # Contact 1
        contact_1, status_code = self.call(OrgaSessionEndpoints.CREATE_CONTACT, contact_data)
        Assert.assertEqual(status_code, 201)
        # Contact 2
        contact_data["first_name"] = "Contact 2"
        contact_2, status_code = self.call(OrgaSessionEndpoints.CREATE_CONTACT, contact_data)
        Assert.assertEqual(status_code, 201)
        # Contact 3
        contact_data["first_name"] = "Contact 3"
        contact_3, status_code = self.call(OrgaSessionEndpoints.CREATE_CONTACT, contact_data)
        Assert.assertEqual(status_code, 201)
        
        # Contact 4
        contact_data["first_name"] = "Contact 4"
        new_phone = {"title": "Phone 3", "number": "3333333333"}
        contact_data["phones"].append(new_phone)
        contact_4, status_code = self.call(OrgaSessionEndpoints.CREATE_CONTACT, contact_data)
        Assert.assertEqual(status_code, 201)

        Assert.assertIn("phones", contact_1)
        Assert.assertIn("phones", contact_2)
        Assert.assertIn("phones", contact_3)
        Assert.assertIn("phones", contact_4)

        # Contact 1 Phones
        contact_1_phone_1 = contact_1["phones"][0]
        # Contact 2 Phones
        contact_2_phone_1 = contact_2["phones"][0]
        contact_2_phone_2 = contact_2["phones"][1]
        # Contact 3 Phones
        contact_3_phone_1 = contact_3["phones"][0]
        # Contact 4 Phones
        contact_4_phone_1 = contact_4["phones"][0]
        contact_4_phone_2 = contact_4["phones"][1]
        contact_4_phone_3 = contact_4["phones"][2]

        Assert.assertNotNull(contact_1_phone_1)
        Assert.assertNotNull(contact_2_phone_1)
        Assert.assertNotNull(contact_2_phone_2)
        Assert.assertNotNull(contact_3_phone_1)
        Assert.assertNotNull(contact_4_phone_1)
        Assert.assertNotNull(contact_4_phone_2)
        Assert.assertNotNull(contact_4_phone_3)

        # Create Orga-session
        self.set_step("Create Orga-session Fail test")
        orga_session_data = {
            "planned_duration": 30,
            "goal": "A",
            "suggested_calls": 5,
            "calls": [
                {
                    "contact": contact_1["id"],
                    "result": "N",  # Not Performed
                    "contact_phone_id": contact_1_phone_1["id"],
                },
                {
                    "contact": contact_2["id"],
                    "result": "A",  # Appointment Fixed
                    "contact_phone_id": contact_2_phone_1["id"],
                },
                {
                    "contact": contact_2["id"],
                    "result": "I",  # Not Interested
                    "contact_phone_id": contact_2_phone_2["id"],
                },
                {
                    "contact": contact_3["id"],
                    "result": "R",  # Not Reached
                    "contact_phone_id": contact_3_phone_1["id"],
                },
                {
                    "contact": contact_4["id"],
                    "result": "C",  # Call Later
                    "contact_phone_id": contact_3_phone_1["id"],  # Wrong Phone
                },
                {
                    "contact": contact_4["id"],
                    "result": "A",  # Appointment Fixed
                    "contact_phone_id": contact_4_phone_2["id"],
                },
                {
                    "contact": contact_4["id"],
                    "result": "A",  # Appointment Fixed
                    "contact_phone_id": contact_4_phone_3["id"],
                },
            ],
        }
        # Test with wrong phone owner
        _, status_code = self.call(
            OrgaSessionEndpoints.CREATE_ORGA_SESSION, params=orga_session_data)
        Assert.assertEqual(status_code, 400)

        # Test with correct phone owner
        self.set_step("Create Orga-session")
        # Correct Phone
        orga_session_data["calls"][4]["contact_phone_id"] = contact_4_phone_1["id"]
        orga_session, status_code = self.call(
            OrgaSessionEndpoints.CREATE_ORGA_SESSION, params=orga_session_data)
        Assert.assertIn("id", orga_session)
        Assert.assertIn("calls", orga_session)

        # Get calls and contacts IDs
        self.set_step("Get Calls info")
        calls_list = orga_session["calls"]
        call_ids_and_contact_ids = [(call["id"], call["contact"])
                                    for call in calls_list if call["result"] == "A"]
        Assert.assertEqual(len(call_ids_and_contact_ids), 3)

        # Get Statistics with Goal Not Achieved
        self.set_step("Get Orga-session statistics Goal Not Achieved")
        orga_session_id = orga_session["id"]

        orga_session_statistics_endpoint = self.format_endpoint(
            OrgaSessionEndpoints.GET_ORGA_SESSION_STATISTICS, id=orga_session_id)
        orga_session_statistics, status_code = self.call(
            orga_session_statistics_endpoint)
        Assert.assertEqual(status_code, 200)
        Assert.assertNotNull(orga_session_statistics)
        Assert.assertEqual(orga_session_statistics["total_calls"], 7)
        Assert.assertEqual(
            orga_session_statistics["total_calls_carried_out"], 6)
        Assert.assertEqual(orga_session_statistics["total_calls_reached"], 5)
        Assert.assertEqual(
            orga_session_statistics["total_calls_not_reached"], 1)
        Assert.assertEqual(
            orga_session_statistics["total_calls_appointment_fixed"], 3)
        Assert.assertEqual(
            orga_session_statistics["total_calls_not_interest"], 1)
        Assert.assertEqual(
            orga_session_statistics["orga_session"]["goal_achieved"], False)

        # Create Appointment
        self.set_step("Add Appointment")
        # Recruiting
        appointment_data = {
            "type": "R",
            "start_time": "00:00",
            "end_time": "00:01",
            "date": "2025-01-16",
            "location": "UK",
            "appointment_invitations": [
                {
                    "contact_id": call_ids_and_contact_ids[0][1],
                    "call_id": call_ids_and_contact_ids[0][0],
                    "must_send_sms": False,
                    "must_send_email": False,
                }
            ],
        }
        _, status_code = self.call(
            OrgaSessionEndpoints.CREATE_APPOINTMENTS, appointment_data)
        Assert.assertEqual(status_code, 201)

        # Consultation
        appointment_data = {
            "type": "C",
            "start_time": "00:00",
            "end_time": "00:01",
            "date": "2025-01-16",
            "location": "UK",
            "appointment_invitations": [
                {
                    "contact_id": call_ids_and_contact_ids[1][1],
                    "call_id": call_ids_and_contact_ids[1][0],
                    "must_send_sms": False,
                    "must_send_email": False,
                }
            ],
        }
        appointment_res, status_code = self.call(
            OrgaSessionEndpoints.CREATE_APPOINTMENTS, appointment_data)
        Assert.assertEqual(status_code, 201)

        # Get Statistics with Goal Achieved
        self.set_step("Get Orga-session statistics Goal Achieved")
        orga_session_statistics, status_code = self.call(
            orga_session_statistics_endpoint)
        Assert.assertEqual(status_code, 200)
        Assert.assertNotNull(orga_session_statistics)
        Assert.assertEqual(
            orga_session_statistics["orga_session"]["goal_achieved"], True)
        Assert.assertEqual(orga_session_statistics["total_invitations"], 2)
        Assert.assertEqual(
            orga_session_statistics["total_invitations_recruiting"], 1)
        Assert.assertEqual(
            orga_session_statistics["total_invitations_consultation"], 1)
        
        # Delete All Created Contacts'
        self.set_step("Delete Contacts")
        delete_contact_1_endpoint = self.format_endpoint(OrgaSessionEndpoints.DELETE_CONTACT, slug=contact_1["slug"])
        delete_contact_2_endpoint = self.format_endpoint(OrgaSessionEndpoints.DELETE_CONTACT, slug=contact_2["slug"])
        delete_contact_3_endpoint = self.format_endpoint(OrgaSessionEndpoints.DELETE_CONTACT, slug=contact_3["slug"])
        delete_contact_4_endpoint = self.format_endpoint(OrgaSessionEndpoints.DELETE_CONTACT, slug=contact_4["slug"])

        _, status_code = self.call(delete_contact_1_endpoint)
        Assert.assertEqual(status_code, 204)
        _, status_code = self.call(delete_contact_2_endpoint)
        Assert.assertEqual(status_code, 204)
        _, status_code = self.call(delete_contact_3_endpoint)
        Assert.assertEqual(status_code, 204)
        _, status_code = self.call(delete_contact_4_endpoint)
        Assert.assertEqual(status_code, 204)
    
        # Delete Orga-session
        self.set_step("Delete Orga-session")
        delete_orga_session_endpoint = self.format_endpoint(
            OrgaSessionEndpoints.DELETE_ORGA_SESSION, id=orga_session_id)
        _, status_code = self.call(delete_orga_session_endpoint)
        Assert.assertEqual(status_code, 204)

        # Check if there is no Orga-session
        get_orga_session_endpoint = self.format_endpoint(
            OrgaSessionEndpoints.GET_ORGA_SESSION, id=orga_session_id)
        _, status_code = self.call(get_orga_session_endpoint)
        Assert.assertEqual(status_code, 404)
