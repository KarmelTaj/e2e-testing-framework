from .endpoints import SalesEndpoints
from scenario_tester.scenarios import BaseScenario
from scenario_tester.assertions import Assert
from scenario_tester.services import time


class SalesTestScenario(BaseScenario):
    def run(self):
        # Log in as partner
        _, status_code = self.login("partner1", SalesEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

        # Start the form
        form_response, status_code = self.call(
            SalesEndpoints.PRIVACY_POLICY, {})
        Assert.assertEqual(status_code, 201)

        Assert.assertIn("slug", form_response)
        form_slug = form_response["slug"]

        # Fill contact details
        current_time = time.current_time()
        contact_detaild_data = {
            "contact_details": {
                "first_name": "[Sales]",
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

        # Household bill
        household_bill_data = {
            "household_bill": {
                "income_wage_salaries": "2000",
                "income_rental_agreement": "50",
                "income_remuneration": "500",
                "income_children_benefit": "1000",
                "expense_rental_costs": "500",
                "expense_bill": "100",
                "expense_household": "200",
                "expense_vehicle": "60",
                "expense_loan": "200",
                "expense_leasing": "150",
                "expense_insurance": "40",
                "expense_save_up": "500",
                "custom_household_incomes": [{"amount": "100", "title": "Some Other income"}, {"amount": "250", "title": "Another income"}],
                "custom_household_expenses": [{"amount": "200", "title": "Other Expenses"}, {"amount": "350", "title": "Some other Expenses"}]
            }
        }

        household_bill_endpoint = self.format_endpoint(
            SalesEndpoints.HOUSEHOLD_BILL, slug=form_slug)
        _, status_code = self.call(
            household_bill_endpoint, household_bill_data)
        Assert.assertEqual(status_code, 200)

        # Assets and Liability
        asset_data = {
            "assets_liability": {
                "saving_account_amount": 2000,
                "saving_account_ongoing_amount": 200,
                "saving_account_duration": 5,
                "home_saving_amount": 60000,
                "home_saving_ongoing_amount": 25000,
                "home_saving_duration": 30,
                "life_insurance_amount": 1000,
                "life_insurance_ongoing_amount": 500,
                "life_insurance_duration": 4,
                "investment_fund_amount": 5000,
                "investment_fund_ongoing_amount": 0,
                "investment_fund_duration": 0,
                "precious_metal_amount": 4000,
                "precious_metal_ongoing_amount": 400,
                "precious_metal_duration": 2,
                "real_state_amount": 10000,
                "real_state_ongoing_amount": 2500,
                "real_state_duration": 6,
                "credit_amount": 20000,
                "credit_ongoing_amount": 15000,
                "credit_duration": 7,
                "loan_amount": 24000,
                "loan_ongoing_amount": 16000,
                "loan_duration": 18,
                "custom_assets": [{"amount": 500, "ongoing_amount": 5, "title": "Other Asset"}, {"amount": 700, "ongoing_amount": 600, "duration": "12", "title": "Some other Asset"}],
                "custom_credits_loans": [{"amount": 4000, "ongoing_amount": 500, "duration": "6", "title": "Other Credit"}, {"amount": 18000, "ongoing_amount": 8000, "duration": "36", "title": "Other Loan"}]
            }
        }

        assets_endpoint = self.format_endpoint(
            SalesEndpoints.ASSET_LIABILITY, slug=form_slug)
        _, status_code = self.call(assets_endpoint, asset_data)
        Assert.assertEqual(status_code, 200)

        # Saving money
        saving_money_data = {
            "saving_money": {
                "saving_money_points": [{"point": "Fun, Game"}, {"point": "Some other concept"}, {"point": "Another concept"}],
                "risk_level": "2",
                "time_horizon": "2",
                "monthly_invest": 200,
                "one_time_invest": 10000
            }
        }

        saving_money_endpoint = self.format_endpoint(
            SalesEndpoints.SAVING_MONEY, slug=form_slug)
        _, status_code = self.call(saving_money_endpoint, saving_money_data)
        Assert.assertEqual(status_code, 200)

        # Feedback
        feedback_data = {
            "feedback": {
                "like_conversation": "4",
                "best_part": "Nice UI",
                "interviewed_before": True,
                "is_interview_valuable": True,
                "willing_to_share": True
            }
        }

        feedback_endpoint = self.format_endpoint(
            SalesEndpoints.FEEDBACK, slug=form_slug)
        _, status_code = self.call(feedback_endpoint, feedback_data)
        Assert.assertEqual(status_code, 200)

        # --------------------Edit Each Tab--------------------

        # Contact Details
        contact_detaild_data = {
            "contact_details": {
                "first_name": "[Sales]",
                "last_name": f"{current_time}",
                "country": "DK",  # Changed
                "city": "City",
                "street": "Address",
                "post_code": "111112",  # Changed
                "birth_date": "1969-11-01",  # Changed
                "email": "some@email.com",
                "phone": "+986664512",
                "job": "My Job",
                "employer": "Employer",
                "child_number": "3",  # Changed
                "child_age": "16,15,11"  # Changed
            },
        }
        _, status_code = self.call(
            contact_detaild_endpoint, contact_detaild_data)
        Assert.assertEqual(status_code, 200)

        # Goals
        goals_data = {
            "goals": {
                "building_house": "2",  # Changed
                "secure_retirement": "1",  # Changed
                "wealth_creation": "1",
                "financial_independence": "2",
                "secure_asset": "1",  # Changed
                "dream_goal": "1",
                "financial_education": "3",  # Changed
                "secure_income": "3",
                # Changed
                "custom_goals": [{"question": "Other Goals", "answer": "3"}, {"question": "Some other goals", "answer": "2"}, {"question": "even some other goals", "answer": "2"}],
            }
        }
        _, status_code = self.call(goals_endpoint, goals_data)
        Assert.assertEqual(status_code, 200)

        # Household bill
        household_bill_data = {
            "household_bill": {
                "income_wage_salaries": "2050",  # Changed
                "income_rental_agreement": "50",
                "income_remuneration": "500",
                "income_children_benefit": "1000",
                "expense_rental_costs": "500",
                "expense_bill": "200",  # Changed
                "expense_household": "200",
                "expense_vehicle": "65",  # Changed
                "expense_loan": "200",
                "expense_leasing": "150",
                "expense_insurance": "400",  # Changed
                "expense_save_up": "550",  # Changed
                # Changed
                "custom_household_incomes": [{"amount": "110", "title": "Some Other income"}, {"amount": "250", "title": "Another income"}, {"amount": "350", "title": "Even Another income"}],
                "custom_household_expenses": [{"amount": "200", "title": "Other Expenses"}, {"amount": "350", "title": "Some other Expenses"}]
            }
        }
        _, status_code = self.call(
            household_bill_endpoint, household_bill_data)
        Assert.assertEqual(status_code, 200)

        # Assets and Liability
        asset_data = {
            "assets_liability": {
                "saving_account_amount": 2500,  # Changed
                "saving_account_ongoing_amount": 300,  # Changed
                "saving_account_duration": 5,
                "home_saving_amount": 61000,  # Changed
                "home_saving_ongoing_amount": 25000,
                "home_saving_duration": 31,  # Changed
                "life_insurance_amount": 1000,
                "life_insurance_ongoing_amount": 500,
                "life_insurance_duration": 5,  # Changed
                "investment_fund_amount": 5000,
                "investment_fund_ongoing_amount": 0,
                "investment_fund_duration": 0,
                "precious_metal_amount": 4020,  # Changed
                "precious_metal_ongoing_amount": 400,
                "precious_metal_duration": 33,  # Changed
                "real_state_amount": 10000,
                "real_state_ongoing_amount": 2500,
                "real_state_duration": 6,
                "credit_amount": 22000,  # Changed
                "credit_ongoing_amount": 15000,
                "credit_duration": 7,
                "loan_amount": 24000,
                "loan_ongoing_amount": 17000,  # Changed
                "loan_duration": 18,
                "custom_assets": [{"amount": 500, "ongoing_amount": 5, "title": "Other Asset"}, {"amount": 700, "ongoing_amount": 600, "duration": "12", "title": "Some other Asset"}, {"amount": 800, "ongoing_amount": 550, "duration": "1", "title": "Even Some other Asset"}],  # Changed
                "custom_credits_loans": [{"amount": 4000, "ongoing_amount": 500, "duration": "6", "title": "Other Credit"}, {"amount": 18000, "ongoing_amount": 8000, "duration": "36", "title": "Other Loan"}]
            }
        }
        _, status_code = self.call(assets_endpoint, asset_data)
        Assert.assertEqual(status_code, 200)

        # Saving money
        saving_money_data = {
            "saving_money": {
                # Changed
                "saving_money_points": [{"point": "Fun, Game"}, {"point": "Some other concept"}, {"point": "Some other concept"}, {"point": "Even some other concept"}],
                "risk_level": "4",  # Changed
                "time_horizon": "3",  # Changed
                "monthly_invest": 250,  # Changed
                "one_time_invest": 10001,  # Changed
            }
        }
        _, status_code = self.call(saving_money_endpoint, saving_money_data)
        Assert.assertEqual(status_code, 200)

        # Feedback
        feedback_data = {
            "feedback": {
                "like_conversation": "5",  # Changed
                "best_part": "Nice UI :D",  # Changed
                "interviewed_before": False,  # Changed
                "is_interview_valuable": True,
                "willing_to_share": True
            }
        }
        _, status_code = self.call(feedback_endpoint, feedback_data)
        Assert.assertEqual(status_code, 200)

        # --------------------Editing Completed--------------------

        # --------------------Failed Call Tests--------------------

        # Test invalid Contact Details
        invalid_contact_details = [
            {"field": "country", "data": {"country": ""}, "expected_status": 400},
            {"field": "zip_code", "data": {"post_code": "invalid"}, "expected_status": 400}, # Needs validation
            {"field": "birth_date", "data": {"birth_date": "01-01-1969"}, "expected_status": 400},
            {"field": "email", "data": {"email": "invalid_email"}, "expected_status": 400},
            {"field": "phone", "data": {"phone": "not_a_phone"}, "expected_status": 400}, # Needs validation
            {"field": "children_age", "data": {"child_number": "3", "child_age": "12,14"}, "expected_status": 400},
        ]

        for test in invalid_contact_details:
            data = {"contact_details": {**contact_detaild_data["contact_details"], **test["data"]}}
            _, status_code = self.call(contact_detaild_endpoint, data)
            Assert.assertEqual(status_code, test["expected_status"], f"Failed test for {test['field']}. Expected {status_code}, but got {test["expected_status"]}")

        # Test invalid Goals
        invalid_goals = [
            {"field": "building_house", "data": {"building_house": "invalid"}, "expected_status": 400},
            {"field": "secure_retirement", "data": {"secure_retirement": "invalid"}, "expected_status": 400},
            {"field": "wealth_creation", "data": {"wealth_creation": "invalid"}, "expected_status": 400},
        ]

        for test in invalid_goals:
            data = {"goals": {**goals_data["goals"], **test["data"]}}
            _, status_code = self.call(goals_endpoint, data)
            Assert.assertEqual(status_code, test["expected_status"], f"Failed test for {test['field']}. Expected {status_code}, but got {test["expected_status"]}")

        # Test invalid Household Bills
        invalid_household_bills = [
            {"field": "income_wage_salaries", "data": {"income_wage_salaries": "invalid"}, "expected_status": 400},
            {"field": "expense_bill", "data": {"expense_bill": "invalid"}, "expected_status": 400},
            {"field": "expense_save_up", "data": {"expense_save_up": "invalid"}, "expected_status": 400},
        ]

        for test in invalid_household_bills:
            data = {"household_bill": {**household_bill_data["household_bill"], **test["data"]}}
            _, status_code = self.call(household_bill_endpoint, data)
            Assert.assertEqual(status_code, test["expected_status"], f"Failed test for {test['field']}. Expected {status_code}, but got {test["expected_status"]}")

        # Test invalid Assets and Liability
        invalid_assets_liability = [
            {"field": "saving_account_amount", "data": {"saving_account_amount": "invalid"}, "expected_status": 400},
            {"field": "home_saving_amount", "data": {"home_saving_amount": "invalid"}, "expected_status": 400},
        ]

        for test in invalid_assets_liability:
            data = {"assets_liability": {**asset_data["assets_liability"], **test["data"]}}
            _, status_code = self.call(assets_endpoint, data)
            Assert.assertEqual(status_code, test["expected_status"], f"Failed test for {test['field']}. Expected {status_code}, but got {test["expected_status"]}")

        # Test invalid Saving Money
        invalid_saving_money = [
            {"field": "risk_level", "data": {"risk_level": 6}, "expected_status": 400},
            {"field": "time_horizon", "data": {"time_horizon": 0}, "expected_status": 400},
            {"field": "monthly_invest", "data": {"monthly_invest": "invalid"}, "expected_status": 400},
            {"field": "one_time_invest", "data": {"one_time_invest": "invalid"}, "expected_status": 400},
        ]

        for test in invalid_saving_money:
            data = {"saving_money": {**saving_money_data["saving_money"], **test["data"]}}
            _, status_code = self.call(saving_money_endpoint, data)
            Assert.assertEqual(status_code, test["expected_status"], f"Failed test for {test['field']}. Expected {status_code}, but got {test["expected_status"]}")

        # --------------------End of Failed Tests--------------------
        
        # Finalize
        finalize_endpoint = self.format_endpoint(
            SalesEndpoints.FINALIZE, slug=form_slug)
        _, status_code = self.call(finalize_endpoint, {})
        Assert.assertEqual(status_code, 200)
        
        # Fetch Summary
        form_summary_endpoint = self.format_endpoint(SalesEndpoints.GET_FORM, slug=form_slug)
        form_summary, status_code = self.call(form_summary_endpoint)
        Assert.assertEqual(status_code, 200)

        # Validate Household Bill in Summary
        expected_household_bill = household_bill_data["household_bill"]
        actual_household_bill = form_summary["household_bill"]
        for key, value in expected_household_bill.items():
            Assert.assertIn(key, actual_household_bill, msg=f"No {key} in household_bill field")
            if key in ["custom_household_incomes", "custom_household_expenses"]:
                for exp, act in zip(value, actual_household_bill[key]):
                    Assert.assertEqual(float(exp["amount"]), float(act["amount"]), msg=f"Mismatch in {key} amount. Expected {exp['amount']}, but got {act['amount']}")
                    Assert.assertEqual(exp["title"], act["title"], msg=f"Mismatch in {key} title. Expected {exp['title']}, but got {act['title']}")
            else:
                # Convert both to floats for numerical comparison if they are numbers
                expected_value = float(value) if isinstance(value, str) and value.replace('.', '', 1).isdigit() else value
                actual_value = float(actual_household_bill[key]) if isinstance(actual_household_bill[key], str) and actual_household_bill[key].replace('.', '', 1).isdigit() else actual_household_bill[key]
                Assert.assertEqual(expected_value, actual_value, msg=f"Mismatch in {key}. Expected {expected_value}, but got {actual_value}")

        # Validate Assets and Liability in Summary
        expected_assets = asset_data["assets_liability"]
        actual_assets = form_summary["assets_liability"]
        for key, value in expected_assets.items():
            Assert.assertIn(key, actual_assets, msg=f"No {key} in assets_liability field")
            if key in ["custom_assets", "custom_credits_loans"]:
                for exp, act in zip(value, actual_assets[key]):
                    Assert.assertEqual(float(exp["amount"]), float(act["amount"]), msg=f"Mismatch in {key} amount. Expected {exp['amount']}, but got {act['amount']}")
                    Assert.assertEqual(exp["title"], act["title"], msg=f"Mismatch in {key} title. Expected {exp['title']}, but got {act['title']}")
            else:
                # Convert both to floats for numerical comparison if they are numbers
                expected_value = float(value) if isinstance(value, str) and value.replace('.', '', 1).isdigit() else value
                actual_value = float(actual_assets[key]) if isinstance(actual_assets[key], str) and actual_assets[key].replace('.', '', 1).isdigit() else actual_assets[key]
                Assert.assertEqual(expected_value, actual_value, msg=f"Mismatch in {key}. Expected {expected_value}, but got {actual_value}")


        # Download PDF
        pdf_endpoint = self.format_endpoint(SalesEndpoints.PDF, slug=form_slug)
        _, status_code = self.call(pdf_endpoint)
        Assert.assertEqual(status_code, 200)

        # Delete Form
        delete_form = self.format_endpoint(SalesEndpoints.DELETE_FORM, slug=form_slug)
        _, status_code = self.call(delete_form)
        Assert.assertEqual(status_code, 204)
