"""
Topic Service

This module handles the business logic related to coding topics and
associations between problems and topics.
It interfaces with TopicRepository for data access and persistence.

The service layer acts as a bridge between the GUI and the repository,
so the GUI does not directly interact with the database.
"""


class TopicService:
    """Business logic layer for Topic and ProblemTopic operations."""

    def __init__(self, topic_repository):
        self.topic_repository = topic_repository

    def get_all_topics(self):
        """Return all available topics from the database."""
        if not self.topic_repository or not hasattr(self.topic_repository, "get_all_topics"):
            return []
        try:
            return self.topic_repository.get_all_topics() or []
        except Exception:
            return []

    def get_topic_by_id(self, topic_id):
        """Return a single topic by ID."""
        if not self.topic_repository or not topic_id:
            return None
        try:
            return self.topic_repository.get_topic_by_id(topic_id)
        except Exception:
            return None

    def get_topic_by_name(self, topic_name):
        """Return a single topic by name (case-insensitive)."""
        if not self.topic_repository or not topic_name:
            return None
        try:
            return self.topic_repository.get_topic_by_name(topic_name)
        except Exception:
            return None

    def assign_topic_to_problem(self, problem_id, topic_id):
        """Link a problem to an existing topic."""
        if not self.topic_repository or not problem_id or not topic_id:
            return False
        try:
            return self.topic_repository.add_problem_topic(problem_id, topic_id)
        except Exception:
            return False

    def get_topics_for_problem(self, problem_id):
        """Return all topic associations for a specific problem."""
        if not self.topic_repository or not problem_id:
            return []
        try:
            return self.topic_repository.get_topics_for_problem(problem_id) or []
        except Exception:
            return []

    def get_topic_names_for_problem(self, problem_id):
        """Return list of topic names associated with a problem."""
        if not self.topic_repository or not problem_id:
            return []
        if hasattr(self.topic_repository, "get_topic_names_for_problem"):
            try:
                return self.topic_repository.get_topic_names_for_problem(problem_id) or []
            except Exception:
                return []
        return []

    def create_topic(self, topic_name):
        """Create a new topic in the TOPIC table via the repository.

        Returns the created topic dict {topic_id, topic_name}, or None on failure.
        Raises ValueError for invalid input.
        """
        if not self.topic_repository:
            return None
        if not topic_name or not isinstance(topic_name, str) or not topic_name.strip():
            raise ValueError("topic_name must be a non-empty string.")
        if hasattr(self.topic_repository, "create_topic"):
            return self.topic_repository.create_topic(topic_name)
        return None
