"""
Problem Service

This module handles the business logic related to coding problems.
It receives problem data from the GUI, validates the data, applies
any required business rules, and then passes valid data to the
Problem Repository for database operations.

The service layer acts as a bridge between the GUI and the repository,
so the GUI does not directly interact with the database.
"""

class ProblemService:

    def __init__(self, problem_repository):
        self.problem_repository = problem_repository

    def _validate_positive_int(self, value, field_name):
        if value is None:
            raise ValueError(f"{field_name} cannot be empty")

        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer")

        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")

    def _validate_string_field(self, value, field_name):
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError(f"{field_name} cannot be empty")
        return value

    def _validate_difficulty(self, difficulty):
        difficulty = self._validate_string_field(difficulty, "Difficulty")
        if difficulty not in ["Easy", "Medium", "Hard"]:
            raise ValueError("Invalid difficulty")
        return difficulty

    def _validate_problem_id(self, problem_id):
        self._validate_positive_int(problem_id, "Problem ID")

    def validate_problem_data(
        self,
        platform,
        question_number,
        title,
        difficulty,
        problem_url
    ):
        self._validate_string_field(platform, "Platform")
        self._validate_positive_int(question_number, "Question number")
        self._validate_string_field(title, "Title")
        self._validate_difficulty(difficulty)
        self._validate_string_field(problem_url, "Problem URL")

    def add_problem(self, platform, question_number, title, difficulty, problem_url):
        if isinstance(platform, str):
            platform = platform.strip()
        if isinstance(title, str):
            title = title.strip()
        if isinstance(difficulty, str):
            difficulty = difficulty.strip()
        if isinstance(problem_url, str):
            problem_url = problem_url.strip()

        self.validate_problem_data(
            platform,
            question_number,
            title,
            difficulty,
            problem_url
        )

        return self.problem_repository.add_problem(
            platform,
            question_number,
            title,
            difficulty,
            problem_url
        )

    def get_problem_by_id(self, problem_id):
        self._validate_problem_id(problem_id)
        return self.problem_repository.get_problem_by_id(problem_id)

    def get_all_problems(self):
        return self.problem_repository.get_all_problems()

    def update_problem(
        self,
        problem_id,
        platform=None,
        question_number=None,
        title=None,
        difficulty=None,
        problem_url=None
    ):
        self._validate_problem_id(problem_id)

        if (
            platform is None
            and question_number is None
            and title is None
            and difficulty is None
            and problem_url is None
        ):
            raise ValueError("At least one field must be provided for update")

        if platform is not None:
            platform = self._validate_string_field(platform, "Platform")

        if question_number is not None:
            self._validate_positive_int(question_number, "Question number")

        if title is not None:
            title = self._validate_string_field(title, "Title")

        if difficulty is not None:
            difficulty = self._validate_difficulty(difficulty)

        if problem_url is not None:
            problem_url = self._validate_string_field(problem_url, "Problem URL")

        return self.problem_repository.update_problem(
            problem_id,
            platform=platform,
            question_number=question_number,
            title=title,
            difficulty=difficulty,
            problem_url=problem_url
        )

    def delete_problem(self, problem_id):
        self._validate_problem_id(problem_id)
        return self.problem_repository.delete_problem(problem_id)



    