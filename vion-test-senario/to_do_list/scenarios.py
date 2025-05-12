from scenario_tester.scenarios import BaseScenario
from scenario_tester.assertions import Assert
from scenario_tester.services import time
from scenario_tester.endpoints import EndPoint
from .endpoints import ToDoListEndpoints
from threading import Lock

SCENARIO_LOCK = Lock()

# To Do List Base Scenario
class BaseToDoListScenario(BaseScenario):

    def is_abstract(self):
        return True

    def login_user(self, username):
        self.set_step("Login")
        _, status_code = self.login(username, ToDoListEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)

    def generate_unique_title(self, endpoint: EndPoint):
        self.set_step("Unique Title")
        base_title = f"[To Do List] {time.current_time()}"
        get_list_by_title = {"text": base_title}
        suffix_counter = 0
        while True:
            list_by_title, status_code = self.call(
                endpoint, params=get_list_by_title
            )
            Assert.assertEqual(status_code, 200)
            if list_by_title and list_by_title["count"] > 0:
                self.warning(
                    f"Duplicate To Do List found with text: '{
                        get_list_by_title['text']}'"
                )
                suffix_counter += 1
                get_list_by_title["text"] = f"{base_title} ({suffix_counter})"
            else:
                break
        return get_list_by_title["text"]

    def create_series(self, **kwargs):
        pass

    def get_series_items(self, title, item_counts, endpoint: EndPoint):
        self.set_step("Get Series Items")
        params = {"text": title}
        items, status_code = self.call(endpoint, params=params)
        Assert.assertEqual(status_code, 200)
        Assert.assertEqual(items["count"], item_counts)
        return items["results"]

    def delete_series(self, slug, endpoint: EndPoint):
        endpoint = self.format_endpoint(endpoint, slug=slug)
        _, status_code = self.call(endpoint)
        Assert.assertEqual(status_code, 204)

    def get_series_items_for_team(self, title, item_counts, **kwargs):
        # Get series items for a team
        self.set_step("Get Series Items for Team")
        get_list_by_title = {"text": title}

        # Add any additional kwargs to the request parameters
        get_list_by_title.update(kwargs)

        to_do_list_series_items, status_code = self.call(
            ToDoListEndpoints.GET_TO_DO_LIST_BY_TITLE_FOR_TEAM, params=get_list_by_title
        )
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("count", to_do_list_series_items)
        Assert.assertEqual(to_do_list_series_items["count"], item_counts)
        Assert.assertIn("results", to_do_list_series_items)
        return to_do_list_series_items["results"]

# Partner Base Scenario
class PartnerBaseScenario(BaseToDoListScenario):
    """
    Base class for Partner To-Do List Scenarios
    """

    generate_unique_title_endpoint = ToDoListEndpoints.GET_TO_DO_LIST_BY_TITLE
    delete_endpoint = ToDoListEndpoints.DELETE_TO_DO_LIST

    def is_abstract(self):
        return True

    def create_series(
        self,
        title,
        frequency,
        start_date,
        end_date,
        frequency_coefficient=1,
        link="external_link",
        criteria="my_self",
        external_link="https://somelink.com",
    ):
        # Create a To Do List with the unique title
        self.set_step("Create Series")
        to_do_list_data = {
            "frequency": frequency,
            "frequency_coefficient": frequency_coefficient,
            "link": link,
            "title": title,
            "start_date": start_date,
            "criteria": criteria,
        }
        if end_date:
            to_do_list_data["end_date"] = end_date
        if external_link and link == "external_link":
            to_do_list_data["external_link"] = external_link

        to_do_list_series, status_code = self.call(
            ToDoListEndpoints.CREATE_TO_DO_LIST, to_do_list_data
        )
        Assert.assertEqual(status_code, 201)
        Assert.assertIn("title", to_do_list_series)
        return to_do_list_series

    def generate_unique_title(self):
        return super().generate_unique_title(self.generate_unique_title_endpoint)

    def get_series_items(self, title, item_counts):
        return super().get_series_items(title, item_counts, self.generate_unique_title_endpoint)

    def delete_series(self, slug):
        return super().delete_series(slug, self.delete_endpoint)

    def finish_task(self, task_id, comment="Comment"):
        finish_task_data = {"todo_item": f"{task_id}", "comment": comment}
        _, status_code = self.call(
            ToDoListEndpoints.FINISH_TASK, params=finish_task_data
        )
        Assert.assertEqual(status_code, 201)

    def update_series(
        self,
        slug,
        title,
        frequency,
        start_date,
        end_date,
        frequency_coefficient=1,
        link="external_link",
        criteria="my_self",
        external_link="https://somelink.com",
    ):
        # Update
        self.set_step("Update Series")
        to_do_list_data = {
            "frequency": frequency,
            "frequency_coefficient": frequency_coefficient,
            "link": link,
            "title": title,
            "start_date": start_date,
            "criteria": criteria,
        }
        if end_date is not None:
            to_do_list_data["end_date"] = end_date
        if external_link is not None and to_do_list_data["link"] == "external_link":
            to_do_list_data["external_link"] = external_link

        update_series_endpoint = self.format_endpoint(
            ToDoListEndpoints.UPDATE_TO_DO_LIST, slug=slug
        )
        to_do_list_series, status_code = self.call(
            update_series_endpoint, to_do_list_data
        )
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("title", to_do_list_series)
        return to_do_list_series

# Backoffice Base Scenario
class BackOfficeBaseScenario(BaseToDoListScenario):
    """
    Base class for BackOffice To-Do List Scenarios
    """

    generate_unique_title_endpoint = ToDoListEndpoints.GET_TO_DO_LIST_BY_TITLE_BACKOFFICE
    delete_endpoint = ToDoListEndpoints.DELETE_TO_DO_LIST_BACKOFFICE

    def is_abstract(self):
        return True

    def create_series(
        self,
        title,
        frequency,
        start_date,
        end_date,
        todo_assignments,
        frequency_coefficient=1,
        link="external_link",
        external_link="https://somelink.com",
    ):
        # Create a To Do List with the unique title
        self.set_step("Create Series")
        to_do_list_data = {
            "frequency": frequency,
            "frequency_coefficient": frequency_coefficient,
            "link": link,
            "title": title,
            "start_date": start_date,
            "todo_assignments": todo_assignments,
        }
        if end_date:
            to_do_list_data["end_date"] = end_date
        if external_link and link == "external_link":
            to_do_list_data["external_link"] = external_link

        to_do_list_series, status_code = self.call(
            ToDoListEndpoints.CREATE_TO_DO_LIST_BACKOFFICE, to_do_list_data
        )
        Assert.assertEqual(status_code, 201)
        Assert.assertIn("title", to_do_list_series)
        return to_do_list_series

    def generate_unique_title(self):
        return super().generate_unique_title(self.generate_unique_title_endpoint)

    def get_series_items(self, title, item_counts):
        return super().get_series_items(title, item_counts, self.generate_unique_title_endpoint)

    def delete_series(self, slug):
        return super().delete_series(slug, self.delete_endpoint)

    def get_user_type_and_level(self):
        self.set_step("Get Details from profile")
        profile_data, status_code = self.call(ToDoListEndpoints.GET_PROFLE)
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("career_level", profile_data)
        Assert.assertIn("partner_type", profile_data)
        # Career Level type: INT             Partner type: STRING
        return profile_data["career_level"], profile_data["partner_type"]

    def create_todo_assignments_list_data(self, career_levels=None, partner_types=None) -> dict:
        """
        Create a list of dictionaries with combinations of career levels and partner types.

        Args:
            career_levels (list[int])
            partner_types (list[str])

        Returns:
            list[dict]: List of dictionaries with `career_level_key` and `partner_type_key`.
        """

        self.set_step("Create assignments list")
        assignments_list = []

        # Add entries for each career level
        if career_levels:
            for level in career_levels:
                assignments_list.append(
                    {"partner_type_key": None, "career_level_key": level})

        # Add entries for each partner type
        if partner_types:
            for partner in partner_types:
                assignments_list.append(
                    {"partner_type_key": partner, "career_level_key": None})

        return assignments_list

# ------------------------ Partner Scenarios ------------------------
class ToDoListTestScenario(PartnerBaseScenario):
    """
    Tets To-Do-List with no frequency
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency=None,
                frequency_coefficient="1",
                start_date="2025-01-01",
                end_date=None,
                link="events",
            )
            series_items = self.get_series_items(series["title"], 1)
            self.finish_task(series_items[0]["id"])
            self.delete_series(series["slug"])


class ToDoListDailyTestScenario(PartnerBaseScenario):
    """
    Tets Daily field for To-Do-List
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="daily",
                frequency_coefficient="2",
                start_date="2024-12-29",
                end_date="2025-01-11",
            )
            series_items = self.get_series_items(series["title"], 7)
            self.finish_task(series_items[0]["id"])
            self.finish_task(series_items[-1]["id"])
            self.delete_series(series["slug"])


class ToDoListWeeklyTestScenario(PartnerBaseScenario):
    """
    Tets Weekly field for To-Do-List
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
            )
            series_items = self.get_series_items(series["title"], 3)
            self.finish_task(series_items[0]["id"])
            self.finish_task(series_items[-1]["id"])
            self.delete_series(series["slug"])


class ToDoListMonthlyTestScenario(PartnerBaseScenario):
    """
    Tets Monthly field for To-Do-List
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="monthly",
                frequency_coefficient="6",
                start_date="2025-01-01",
                end_date="2030-01-01",
            )
            series_items = self.get_series_items(series["title"], 11)
            self.finish_task(series_items[0]["id"])
            self.finish_task(series_items[-1]["id"])
            self.delete_series(series["slug"])


class ToDoListYearlyTestScenario(PartnerBaseScenario):
    """
    Tets Yearly field for To-Do-List
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="yearly",
                frequency_coefficient="3",
                start_date="2025-01-01",
                end_date="2035-02-01",
            )
            series_items = self.get_series_items(series["title"], 4)
            self.finish_task(series_items[0]["id"])
            self.finish_task(series_items[-1]["id"])
            self.delete_series(series["slug"])


class ToDoListUpdateTestScenario(PartnerBaseScenario):
    """
    Tets Update for To-Do-List
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="monthly",
                frequency_coefficient="6",
                start_date="2025-01-01",
                end_date="2030-01-01",
            )
            series_items = self.get_series_items(series["title"], 11)
            self.finish_task(series_items[0]["id"])
            self.finish_task(series_items[-1]["id"])

            # Update
            self.update_series(
                slug=series["slug"],
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
            )

            self.delete_series(series["slug"])


class ToDoListMyTeamTestScenario(PartnerBaseScenario):
    """
    Tets To-Do-List for My Team
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="monthly",
                frequency_coefficient="6",
                start_date="2025-01-01",
                end_date="2030-01-01",
                criteria="my_team"
            )
            self.get_series_items(series["title"], 11)
            self.get_series_items_for_team(series["title"], 0, origin="my_tasks")
            self.get_series_items_for_team(
                series["title"], 11, origin="my_team_tasks")

            # Check for the team member
            self.logout()
            self.login_user("partner2")
            self.get_series_items_for_team(series["title"], 11)

            # Delete
            self.logout()
            self.login_user("partner1")
            self.delete_series(series["slug"])


class ToDoListMeAndMyTeamTestScenario(PartnerBaseScenario):
    """
    Tets To-Do-List for Me and My Team
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")
            unique_title = self.generate_unique_title()
            series = self.create_series(
                title=unique_title,
                frequency="monthly",
                frequency_coefficient="6",
                start_date="2025-01-01",
                end_date="2030-01-01",
                criteria="my_team_and_my_self"
            )
            self.get_series_items(series["title"], 11)
            self.get_series_items_for_team(series["title"], 11, origin="my_tasks")
            self.get_series_items_for_team(
                series["title"], 11, origin="my_team_tasks")

            # Check for the team member
            self.logout()
            self.login_user("partner2")
            self.get_series_items_for_team(series["title"], 11)

            # Delete
            self.logout()
            self.login_user("partner1")
            self.delete_series(series["slug"])


class ToDoListBadDataTestScenario(PartnerBaseScenario):
    """
    Test bad data for To-Do-List
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("partner1")

            # List of bad data cases
            bad_data_cases = [
                {"frequency": "invalid_frequency", "frequency_coefficient": "1",
                    "start_date": "2025-01-01", "end_date": "2025-01-10"},
                {"frequency": "daily", "frequency_coefficient": "-1",
                    "start_date": "2025-01-01", "end_date": "2025-01-10"},
                {"frequency": "daily", "frequency_coefficient": "2", "start_date": "2025-01-10",
                    "end_date": "2025-01-01"},  # End date before start date
                {"frequency": "weekly", "frequency_coefficient": "1",
                    "start_date": "invalid_date", "end_date": "2025-02-01"},
                {"frequency": "monthly", "frequency_coefficient": "abc",
                    "start_date": "2025-01-01", "end_date": "2025-12-01"},
                {"frequency": "monthly", "frequency_coefficient": "0",
                    "start_date": "2025-01-01", "end_date": "2025-12-01"},
                {"frequency": "monthly", "start_date": "2025-01-01",
                    "end_date": "2025-12-01"},
            ]

            for index, bad_data in enumerate(bad_data_cases, start=1):
                self.set_step(f"Bad Data Case {index}")
                to_do_list_data = {
                    "title": self.generate_unique_title(),
                    "frequency": bad_data["frequency"],
                    "start_date": bad_data["start_date"],
                    "end_date": bad_data["end_date"],
                    "link": "external_link",
                    "criteria": "my_self",
                    "external_link": "https://somelink.com",
                }
                if "frequency_coefficient" in bad_data:
                    to_do_list_data["frequency_coefficient"] = bad_data["frequency_coefficient"]
                _, status_code = self.call(
                    ToDoListEndpoints.CREATE_TO_DO_LIST, to_do_list_data)
                Assert.assertEqual(status_code, 400, f"Failed test for {index}. Expected 400 but got {status_code}")
# ----------------------- End of Partner Scenarios -----------------------


# # ------------------------ Backoffice Scenarios ------------------------
class ToDoListBackOfficeCareerLevelTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Career Level field
    """

    def run(self):
        with SCENARIO_LOCK:
            # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()

            career_levels = [career_level]
            todo_assignments = self.create_todo_assignments_list_data(
                career_levels=career_levels)

            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 3)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficePartnerTypeTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Partner type field 
    """

    def run(self):
        with SCENARIO_LOCK:
            # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()
            career_levels = [career_level]
            partner_types = [partner_type]
            todo_assignments = self.create_todo_assignments_list_data(
                partner_types=partner_types)
            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 3)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficePartnerAndCareerLevelTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Partner type field 
    """

    def run(self):
        with SCENARIO_LOCK:
            # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()
            career_levels = [career_level]
            partner_types = [partner_type]
            todo_assignments = self.create_todo_assignments_list_data(
                career_levels, partner_types)
            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 3)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficeMultipleCareerLevelTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Partner type field 
    """

    def run(self):
        with SCENARIO_LOCK:
        # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()
            career_levels = [career_level, 1, 2]
            todo_assignments = self.create_todo_assignments_list_data(
                career_levels=career_levels)
            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 3)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficeMultiplePartnerTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Partner type field 
    """

    def run(self):
        with SCENARIO_LOCK:
            # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()
            partner_types = [partner_type, "2"]
            todo_assignments = self.create_todo_assignments_list_data(
                partner_types=partner_types)

            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 3)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficeMultiplePartnerAndCareerLevelTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Partner type field 
    """

    def run(self):
        with SCENARIO_LOCK:
            # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()
            career_levels = [career_level, 1, 2]
            partner_types = [partner_type, "2"]
            todo_assignments = self.create_todo_assignments_list_data(
                career_levels, partner_types)

            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 3)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficeNotInTheListTestScenario(BackOfficeBaseScenario):
    """
    Tets To-Do-List Backoffice Partner type field 
    """

    def run(self):
        with SCENARIO_LOCK:
            # Extract career_level and partner_type of a Partner
            self.login_user("partner1")
            career_level, partner_type = self.get_user_type_and_level()

            # Log in as Backoffice and Create a To-do List
            self.logout()
            self.login_user("backoffice")

            unique_title = self.generate_unique_title()
            career_levels = [1, 2, 3, 4, 5, 6, 7, 8]
            partner_types = ["2", "3"]

            if career_level in career_levels:
                career_levels.remove(career_level)
            if partner_type in partner_types:
                partner_types.remove(partner_type)

            todo_assignments = self.create_todo_assignments_list_data(
                career_levels, partner_types)

            series = self.create_series(
                title=unique_title,
                frequency="weekly",
                frequency_coefficient="2",
                start_date="2025-01-01",
                end_date="2025-02-01",
                todo_assignments=todo_assignments,
            )
            self.get_series_items(series["title"], 3)

            # Log in as Partner to see if the list is there
            self.logout()
            self.login_user("partner1")
            self.get_series_items_for_team(series["title"], 0)

            # Log in as backoffice to Delete the series
            self.logout()
            self.login_user("backoffice")
            self.delete_series(series["slug"])


class ToDoListBackOfficeBadDataTestScenario(BackOfficeBaseScenario):
    """
    Test bad data for BackOffice To-Do-List with non-empty assignments
    """

    def run(self):
        with SCENARIO_LOCK:
            self.login_user("backoffice")

            career_levels = [1, 2, 8]
            partner_types = ["2"]
            valid_assignments = self.create_todo_assignments_list_data(career_levels, partner_types)

            # Bad data cases
            bad_data_cases = [
                {"frequency": "invalid_frequency", "frequency_coefficient": "1",
                    "start_date": "2025-01-01", "end_date": "2025-01-10", "todo_assignments": valid_assignments},
                {"frequency": "daily", "frequency_coefficient": "-1",
                    "start_date": "2025-01-01", "end_date": "2025-01-10", "todo_assignments": valid_assignments},
                {"frequency": "daily", "frequency_coefficient": "2", "start_date": "2025-01-10",
                    "end_date": "2025-01-01", "todo_assignments": valid_assignments},  # End date before start date
                {"frequency": "weekly", "frequency_coefficient": "1",
                    "start_date": "invalid_date", "end_date": "2025-02-01", "todo_assignments": valid_assignments},
                {"frequency": "monthly", "frequency_coefficient": "abc",
                    "start_date": "2025-01-01", "end_date": "2025-12-01", "todo_assignments": valid_assignments},
                {"frequency": "monthly", "frequency_coefficient": "0",
                    "start_date": "2025-01-01", "end_date": "2025-12-01", "todo_assignments": valid_assignments},
            ]

            for index, bad_data in enumerate(bad_data_cases, start=1):
                self.set_step(f"Bad Data Case {index}")
                to_do_list_data = {
                    "title": self.generate_unique_title(),
                    "frequency": bad_data["frequency"],
                    "frequency_coefficient": bad_data["frequency_coefficient"],
                    "start_date": bad_data["start_date"],
                    "end_date": bad_data["end_date"],
                    "link": "external_link",
                    "todo_assignments": bad_data["todo_assignments"],
                    "external_link": "https://somelink.com",
                }

                _, status_code = self.call(
                    ToDoListEndpoints.CREATE_TO_DO_LIST_BACKOFFICE, to_do_list_data
                )
                Assert.assertEqual(status_code, 400, f"Failed test for Case {index}. Expected 400 but got {status_code}")
