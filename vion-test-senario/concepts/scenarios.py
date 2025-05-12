from .endpoints import ConceptsEndpoints
from sales.endpoints import SalesEndpoints
from scenario_tester.scenarios import BaseScenario
from scenario_tester.assertions import Assert
from scenario_tester.services import time


class ConceptTestScenario(BaseScenario):
    def run(self):
        # Log in as partner
        self.set_step("Step 1: Login")
        _, status_code = self.login("partner1", ConceptsEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Define the form-data payload
        self.set_step("Step 2: Create a new Concept")
        current_time = time.current_time()
        concept_data = {
            "title": "",
            "photo": "2",
            "title_input": f"[Concepts] {current_time}",
            "wizard_step": "2",
        }
        concept_response, status_code = self.call(
            ConceptsEndpoints.CONCEPT, concept_data)
        Assert.assertEqual(status_code, 201)
        concept_slug = concept_response["slug"]

        # ---------------------Wishes and Goals---------------------
        # Start the form
        self.set_step("Step 3: Create a new Wish and Goals")
        form_response, status_code = self.call(
            SalesEndpoints.PRIVACY_POLICY, {})
        Assert.assertEqual(status_code, 201)

        Assert.assertIn("slug", form_response)
        form_slug = form_response["slug"]

        # Fill contact details
        current_time = time.current_time()
        contact_detaild_data = {
            "contact_details": {
                "first_name": "[Concept]",
                "last_name": f"{current_time}",
                "country": "DE",
                "city": "City",
                "street": "Address",
                "post_code": "11111",
                "birth_date": "1969-01-01",
                "email": "some@email.com",
                "phone": "+986664512",
                "job": "My Job",
                "employer": "Employer",
                "child_number": "2",
                "child_age": "16,15"
            },
        }
        contact_detaild_endpoint = self.format_endpoint(
            SalesEndpoints.CONTACT_DETAILS, slug=form_slug)
        _, status_code = self.call(
            contact_detaild_endpoint, contact_detaild_data)
        Assert.assertEqual(status_code, 200)

        # Fill Goals
        goals_data = {
            "goals": {
                "building_house": "1",
                "secure_retirement": "3",
                "wealth_creation": "1",
                "financial_independence": "2",
                "secure_asset": "3",
                "dream_goal": "1",
                "financial_education": "2",
                "secure_income": "3",
                "custom_goals": [{"question": "Other Goals", "answer": "3"}, {"question": "Some other goals", "answer": "2"}],
            }
        }
        goals_endpoint = self.format_endpoint(
            SalesEndpoints.GOALS, slug=form_slug)
        _, status_code = self.call(goals_endpoint, goals_data)
        Assert.assertEqual(status_code, 200)

        # Saving money (Part 1)
        saving_money_data = {
            "saving_money": {
                "risk_level": "2",
                "time_horizon": "1",
            }
        }
        saving_money_endpoint = self.format_endpoint(
            SalesEndpoints.SAVING_MONEY, slug=form_slug)
        _, status_code = self.call(saving_money_endpoint, saving_money_data)
        Assert.assertEqual(status_code, 200)

        # Saving money (Part 2)
        saving_money_data = {
            "saving_money": {
                "risk_level": "2",
                "time_horizon": 3,
            }
        }
        saving_money_endpoint = self.format_endpoint(
            SalesEndpoints.SAVING_MONEY, slug=form_slug)
        _, status_code = self.call(saving_money_endpoint, saving_money_data)
        Assert.assertEqual(status_code, 200)
        # ---------------------Wishes and Goals---------------------

        # Portfolio
        self.set_step("Step 4: Portfolio Tab")
        update_concept_data = {
            "customer_id": form_response["id"],
            "wizard_step": "3",
        }
        update_concept_endpoint = self.format_endpoint(
            ConceptsEndpoints.UPDATE_CONCEPT, concept_slug=concept_slug)
        concept_response, status_code = self.call(
            update_concept_endpoint, update_concept_data)
        Assert.assertEqual(status_code, 200)

        # ---------------------Proposals---------------------
        # --------------------1th Proposal---------------------
        # Initial Investment
        self.set_step("1th Proposal")
        initial_investment_data = {
            "initial_monthly_investment": 120,
            "initial_one_time_investment": 500
        }
        initial_investment_endpoint = self.format_endpoint(
            ConceptsEndpoints.RECOMMENDATIONS, concept_slug=concept_slug)
        concept_response, status_code = self.call(
            initial_investment_endpoint, initial_investment_data)
        Assert.assertEqual(status_code, 201)

        # Proposal
        recommendations_id = concept_response["recommendations"][0]["id"]
        proposal_data = {
            "initial_monthly_investment": 120,
            "initial_one_time_investment": 500,
            "product_recommendations": [
                {"product_id": 1, "monthly_investment": 6,
                    "one_time_investment": 25},
                {"product_id": 2, "monthly_investment": 6,
                    "one_time_investment": 25},
                {"product_id": 3, "monthly_investment": 6},
                {"product_id": 4, "monthly_investment": 6,
                    "one_time_investment": 25},
                {"product_id": 5, "monthly_investment": 8},
                {"product_id": 6, "monthly_investment": 4},
                {"product_id": 7, "one_time_investment": 25},
                {"product_id": 8, "monthly_investment": 12,
                    "one_time_investment": 150},
                {"product_id": 9, "monthly_investment": 2},
                {"product_id": 10, "monthly_investment": 10},
                {"product_id": 11, "monthly_investment": 6},
                {"product_id": 15, "monthly_investment": 1,
                    "one_time_investment": 25},
                {"product_id": 13, "monthly_investment": 11,
                    "one_time_investment": 25},
                {"product_id": 95, "monthly_investment": 9,
                    "one_time_investment": 25},
                {"product_id": 18, "monthly_investment": 3,
                    "one_time_investment": 50},
                {"product_id": 57, "monthly_investment": 8,
                    "one_time_investment": 25},
                {"product_id": 56, "monthly_investment": 4,
                    "one_time_investment": 25},
                {"product_id": 86, "monthly_investment": 7,
                    "one_time_investment": 25},
                {"product_id": 72, "monthly_investment": 5,
                    "one_time_investment": 25},
                {"product_id": 52, "monthly_investment": 6, "one_time_investment": 25}
            ]
        }
        updated_recommendations_endpoint = self.format_endpoint(
            ConceptsEndpoints.RECOMMENDATIONS_UPDATE, concept_slug=concept_slug, id=recommendations_id)
        _, status_code = self.call(
            updated_recommendations_endpoint, proposal_data)
        Assert.assertEqual(status_code, 200)

        # --------------------2th Proposal---------------------
        # Initial Investment
        self.set_step("2th Proposal")
        initial_investment_data = {
            "initial_monthly_investment": 500,
            "initial_one_time_investment": 1500
        }
        concept_response, status_code = self.call(
            initial_investment_endpoint, initial_investment_data)
        Assert.assertEqual(status_code, 201)

        # proposal
        recommendations_id = concept_response["recommendations"][1]["id"]
        proposal_data = {
            "initial_monthly_investment": 500,
            "initial_one_time_investment": 1500,
            "product_recommendations": [
                {"product_id": 1, "monthly_investment": 411},
                {"product_id": 2, "monthly_investment": 50},
                {"product_id": 5, "monthly_investment": 100},
                {"product_id": 6, "one_time_investment": 2000}
            ]
        }
        updated_recommendations_endpoint = self.format_endpoint(
            ConceptsEndpoints.RECOMMENDATIONS_UPDATE, concept_slug=concept_slug, id=recommendations_id)
        _, status_code = self.call(
            updated_recommendations_endpoint, proposal_data)
        Assert.assertEqual(status_code, 200)

        # --------------------3th Proposal---------------------
        # Initial Investment
        self.set_step("3th Proposal")
        initial_investment_data = {
            "initial_monthly_investment": 0,
            "initial_one_time_investment": 2500
        }
        concept_response, status_code = self.call(
            initial_investment_endpoint, initial_investment_data)
        Assert.assertEqual(status_code, 201)

        # proposal
        recommendations_id = concept_response["recommendations"][2]["id"]
        proposal_data = {
            "initial_monthly_investment": 0,
            "initial_one_time_investment": 2500,
            "product_recommendations": [
                {"product_id": 1, "monthly_investment": 200},
                {"product_id": 2, "one_time_investment": 1000},
                {"product_id": 9, "one_time_investment": 50},
                {"product_id": 8, "one_time_investment": 50},
                {"product_id": 7, "one_time_investment": 50},
                {"product_id": 6, "one_time_investment": 50},
                {"product_id": 11, "one_time_investment": 50},
                {"product_id": 15, "one_time_investment": 50},
                {"product_id": 14, "one_time_investment": 50},
                {"product_id": 13, "one_time_investment": 500},
                {"product_id": 12, "one_time_investment": 700}
            ]
        }
        updated_recommendations_endpoint = self.format_endpoint(
            ConceptsEndpoints.RECOMMENDATIONS_UPDATE, concept_slug=concept_slug, id=recommendations_id)
        _, status_code = self.call(
            updated_recommendations_endpoint, proposal_data)
        Assert.assertEqual(status_code, 200)
        # ------------------End Of Proposals--------------------

        # Finalize
        self.set_step("Step 5: Finalize the Concept")
        finalize_data = {
            "finalized": "true",
            "wizard_step": "4",
        }
        concept_response, status_code = self.call(
            update_concept_endpoint, finalize_data)
        Assert.assertEqual(status_code, 200)

        # PDF File
        self.set_step("Step 6: PDF File")
        pdf_data = {
            "conversation_date": "2024-12-13",
            "preferred_language": "en",
        }
        generate_pdf_endpoint = self.format_endpoint(
            ConceptsEndpoints.GENERATE_PDF, concept_slug=concept_slug)
        pdf_generator_response, status_code = self.call(
            generate_pdf_endpoint, pdf_data)
        file_url = pdf_generator_response["file"]
        Assert.assertEqual(status_code, 201)
        Assert.assertIn("file", pdf_generator_response)
        Assert.assertNotNull(file_url)

        # Change status
        self.set_step("Step 7: Change Status")
        update_concept_data = {
            "status": "I"
        }
        concept_response, status_code = self.call(
            update_concept_endpoint, update_concept_data)
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("status", concept_response)
        Assert.assertEqual("I", concept_response["status"])

        # Delete Concept
        self.set_step("Step 8: Delete Concept")
        delete_concept_endpoint = self.format_endpoint(
            ConceptsEndpoints.DELETE_CONCEPT, concept_slug=concept_slug)
        _, status_code = self.call(delete_concept_endpoint)
        Assert.assertEqual(status_code, 204)

        # Check if the Concept is there
        self.set_step("Step 9: Find deleted concept")
        get_concept_endpoint = self.format_endpoint(
            ConceptsEndpoints.GET_CONCEPT, concept_slug=concept_slug)
        _, status_code = self.call(get_concept_endpoint)
        Assert.assertEqual(status_code, 404)
