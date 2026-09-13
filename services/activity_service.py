"""
Activity Service

This module handles the business logic related to user problem activities.
It tracks problem solving attempts (both initial solves and revisions),
determines the appropriate activity type ("New" vs "Revision"), automatically
records the activity date, and interfaces with the Activity Repository for
data access and persistence.

The service layer acts as a bridge between the GUI and the repository,
so the GUI does not directly interact with the database.
"""

from datetime import date


class ActivityService:
    """
    Business logic layer for Activity operations.

    Expected ActivityRepository interface:
        - has_activity_for_problem(user_id, problem_id) -> bool
        - add_activity(user_id, problem_id, activity_date, activity_type) -> dict
        - get_activity_by_id(activity_id) -> dict | None
        - get_activities_by_user_id(user_id) -> list[dict]
        - get_activities_by_problem_id(problem_id) -> list[dict]
        - get_all_activities() -> list[dict]
        - delete_activity(activity_id) -> bool
    """

    def __init__(self, activity_repository):
        self.activity_repository = activity_repository

    def _validate_positive_int(self, value, field_name):
        if value is None:
            raise ValueError(f"{field_name} cannot be empty")

        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer")

        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")

    def _validate_user_id(self, user_id):
        self._validate_positive_int(user_id, "User ID")

    def _validate_problem_id(self, problem_id):
        self._validate_positive_int(problem_id, "Problem ID")

    def _validate_activity_id(self, activity_id):
        self._validate_positive_int(activity_id, "Activity ID")

    def record_problem_activity(self, user_id, problem_id):
        self._validate_user_id(user_id)
        self._validate_problem_id(problem_id)

        has_previous = self.activity_repository.has_activity_for_problem(user_id, problem_id)
        activity_type = "Revision" if has_previous else "New"
        activity_date = date.today()

        return self.activity_repository.add_activity(
            user_id,
            problem_id,
            activity_date,
            activity_type
        )

    def get_activity_by_id(self, activity_id):
        self._validate_activity_id(activity_id)
        return self.activity_repository.get_activity_by_id(activity_id)

    def get_activities_by_user_id(self, user_id):
        self._validate_user_id(user_id)
        return self.activity_repository.get_activities_by_user_id(user_id)

    def get_activities_by_problem_id(self, problem_id):
        self._validate_problem_id(problem_id)
        return self.activity_repository.get_activities_by_problem_id(problem_id)

    def get_all_activities(self):
        return self.activity_repository.get_all_activities()

    def delete_activity(self, activity_id):
        self._validate_activity_id(activity_id)
        return self.activity_repository.delete_activity(activity_id)
