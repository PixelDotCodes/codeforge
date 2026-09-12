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

    def validate_problem_data(
        self,
        platform,
        question_number,
        title,
        difficulty,
        problem_url
    ):
        if not platform:
            raise ValueError("Platform cannot be empty")

        if question_number is None:
            raise ValueError("Question number cannot be empty")

        if not isinstance(question_number, int):
            raise ValueError("Question number must be an integer")

        if question_number <= 0:
            raise ValueError("Question number must be greater than 0")

        if not title:
            raise ValueError("Title cannot be empty")

        if not difficulty:
            raise ValueError("Difficulty cannot be empty")

        if difficulty not in ["Easy", "Medium", "Hard"]:
            raise ValueError("Invalid difficulty")

        if not problem_url:
            raise ValueError("Problem URL cannot be empty")

    def add_problem(self, platform, question_number, title, difficulty, problem_url):
        self.validate_problem_data(
            platform,
            question_number,
            title,
            difficulty,
            problem_url
        )

        pass  #will be updated when the package repositories is made


    