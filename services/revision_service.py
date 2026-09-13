"""
Revision Service

This module handles the business logic related to problem revisions.
It validates revision data, enforces business rules, and coordinates
with the Revision Repository for persistence.

The service layer acts as a bridge between the GUI and the repository,
so the GUI does not directly interact with the database.
"""

from datetime import date, datetime


class RevisionService:
    """
    Business logic layer for Revision operations.

    Expected RevisionRepository interface:
        - problem_exists(problem_id) -> bool
        - add_revision(problem_id, revision_date, revision_type) -> dict
        - get_revision_by_id(revision_id) -> dict | None
        - get_revisions_by_problem_id(problem_id) -> list[dict]
        - get_all_revisions() -> list[dict]
        - update_revision(revision_id, revision_date=None, revision_type=None) -> dict | None
        - delete_revision(revision_id) -> bool
    """

    def __init__(self, revision_repository):
        self.revision_repository = revision_repository

    def _validate_positive_int(self, value, field_name):
        if value is None:
            raise ValueError(f"{field_name} cannot be empty")

        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer")

        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")

    def _validate_revision_id(self, revision_id):
        self._validate_positive_int(revision_id, "Revision ID")

    def _validate_problem_id(self, problem_id):
        self._validate_positive_int(problem_id, "Problem ID")

    def _validate_revision_date(self, revision_date):
        if revision_date is None:
            raise ValueError("Revision date cannot be empty")

        if isinstance(revision_date, bool):
            raise ValueError("Invalid revision date")

        if isinstance(revision_date, datetime):
            return revision_date.date()

        if isinstance(revision_date, date):
            return revision_date

        if isinstance(revision_date, str):
            cleaned = revision_date.strip()
            if not cleaned:
                raise ValueError("Revision date cannot be empty")
            try:
                parsed_dt = datetime.strptime(cleaned, "%Y-%m-%d")
                return parsed_dt.date()
            except ValueError:
                raise ValueError("Invalid revision date, must be in YYYY-MM-DD format")

        raise ValueError("Invalid revision date")

    def _validate_revision_type(self, revision_type):
        if revision_type is None:
            raise ValueError("Revision type cannot be empty")

        if not isinstance(revision_type, str):
            raise ValueError("Revision type must be a string")

        cleaned = revision_type.strip()
        if not cleaned:
            raise ValueError("Revision type cannot be empty")

        return cleaned

    def add_revision(self, problem_id, revision_date, revision_type):
        self._validate_problem_id(problem_id)
        valid_date = self._validate_revision_date(revision_date)
        valid_type = self._validate_revision_type(revision_type)

        if not self.revision_repository.problem_exists(problem_id):
            raise ValueError("Problem does not exist")

        return self.revision_repository.add_revision(
            problem_id,
            valid_date,
            valid_type
        )

    def get_revision_by_id(self, revision_id):
        self._validate_revision_id(revision_id)
        return self.revision_repository.get_revision_by_id(revision_id)

    def get_revisions_by_problem_id(self, problem_id):
        self._validate_problem_id(problem_id)
        return self.revision_repository.get_revisions_by_problem_id(problem_id)

    def get_all_revisions(self):
        return self.revision_repository.get_all_revisions()

    def update_revision(
        self,
        revision_id,
        revision_date=None,
        revision_type=None
    ):
        self._validate_revision_id(revision_id)

        if revision_date is None and revision_type is None:
            raise ValueError("At least one field must be provided for update")

        valid_date = None
        if revision_date is not None:
            valid_date = self._validate_revision_date(revision_date)

        valid_type = None
        if revision_type is not None:
            valid_type = self._validate_revision_type(revision_type)

        return self.revision_repository.update_revision(
            revision_id,
            revision_date=valid_date,
            revision_type=valid_type
        )

    def delete_revision(self, revision_id):
        self._validate_revision_id(revision_id)
        return self.revision_repository.delete_revision(revision_id)
