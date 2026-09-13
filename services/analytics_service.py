"""
Analytics Service

This module handles the business and aggregation logic for analytics and statistics
in CodeForge. It aggregates raw data from the problem, topic, and activity
repositories into clean, graph/report-ready Python data structures.

The service layer acts as a bridge between repositories and visualization/GUI layers:
- Business and aggregation logic only.
- No SQL or direct PostgreSQL access.
- No Tkinter or GUI logic.
- No Matplotlib or chart rendering.
- No direct database connection handling.
"""

from collections import defaultdict
from datetime import date, datetime


class AnalyticsService:
    """
    Business logic layer for analytics and reporting operations.

    Expected Repository Interfaces:

    ProblemRepository:
        - get_all_problems() -> list[dict]
          Returns list of problem dicts, each typically containing:
          {
              "problem_id": int,
              "platform": str,
              "question_number": int,
              "title": str,
              "difficulty": str,  # "Easy", "Medium", "Hard"
              "problem_url": str
          }

    TopicRepository:
        - get_all_topics() -> list[dict]
          Returns list of topic dicts:
          [{"topic_id": int, "topic_name": str}, ...]
        - get_all_problem_topics() -> list[dict]
          Returns list of join records (PROBLEMS <-> ProblemTopic <-> TOPIC):
          [{"problem_id": int, "topic_id": int}, ...]

    ActivityRepository:
        - get_all_activities() -> list[dict]
          Returns list of activity dicts:
          [
              {
                  "activity_id": int,
                  "user_id": int,
                  "problem_id": int,
                  "activity_date": date | str | datetime,
                  "activity_type": str  # "New" | "Revision"
              }, ...
          ]
        - get_activities_by_user_id(user_id: int) -> list[dict]
    """

    def __init__(
        self,
        problem_repository=None,
        activity_repository=None,
        topic_repository=None,
    ):
        # Flexible positional arg handling:
        # Detect if caller passed (problem_repo, topic_repo, activity_repo)
        if (
            activity_repository is not None
            and hasattr(activity_repository, "get_all_topics")
            and not hasattr(activity_repository, "get_all_activities")
        ):
            actual_topic_repo = activity_repository
            actual_activity_repo = topic_repository
            activity_repository = actual_activity_repo
            topic_repository = actual_topic_repo

        self.problem_repository = problem_repository
        self.activity_repository = activity_repository
        self.topic_repository = topic_repository

    # -------------------------------------------------------------------------
    # Validation helpers
    # -------------------------------------------------------------------------

    def _validate_positive_int(self, value, field_name):
        if value is None:
            raise ValueError(f"{field_name} cannot be empty")

        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer")

        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")

    def _validate_limit(self, limit):
        if limit is not None:
            self._validate_positive_int(limit, "Limit")

    def _validate_user_id(self, user_id):
        self._validate_positive_int(user_id, "User ID")

    def _parse_date(self, value):
        if value is None or isinstance(value, bool):
            return None

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return None
            try:
                return datetime.strptime(cleaned, "%Y-%m-%d").date()
            except ValueError:
                try:
                    return date.fromisoformat(cleaned)
                except ValueError:
                    return None

        return None

    # -------------------------------------------------------------------------
    # Problem Statistics
    # -------------------------------------------------------------------------

    def _get_raw_problems(self):
        if not self.problem_repository:
            return []
        if hasattr(self.problem_repository, "get_all_problems"):
            try:
                problems = self.problem_repository.get_all_problems()
                if not problems or not isinstance(problems, list):
                    return []
                return problems
            except Exception:
                return []
        return []

    def get_total_solved_count(self):
        """Return total number of solved problems."""
        return len(self._get_raw_problems())

    def get_total_problems(self):
        """Alias for get_total_solved_count."""
        return self.get_total_solved_count()

    def get_difficulty_counts(self):
        """
        Return the count of solved problems grouped by difficulty.
        Always returns a dictionary with 'Easy', 'Medium', 'Hard' keys.
        """
        counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        for problem in self._get_raw_problems():
            if not isinstance(problem, dict):
                continue
            difficulty = problem.get("difficulty")
            if isinstance(difficulty, str):
                normalized = difficulty.strip().capitalize()
                if normalized in counts:
                    counts[normalized] += 1
        return counts

    def get_easy_count(self):
        """Return total number of solved Easy problems."""
        return self.get_difficulty_counts()["Easy"]

    def get_medium_count(self):
        """Return total number of solved Medium problems."""
        return self.get_difficulty_counts()["Medium"]

    def get_hard_count(self):
        """Return total number of solved Hard problems."""
        return self.get_difficulty_counts()["Hard"]

    def get_platform_counts(self):
        """
        Return problem counts grouped by platform.
        Example: {"LeetCode": 12, "Codeforces": 5}
        """
        counts = defaultdict(int)
        for problem in self._get_raw_problems():
            if not isinstance(problem, dict):
                continue
            platform = problem.get("platform")
            if isinstance(platform, str):
                platform = platform.strip()
                if platform:
                    counts[platform] += 1
        return dict(counts)

    def get_difficulty_counts_by_platform(self):
        """
        Return difficulty counts grouped by platform where supported by repository data.
        Example:
        {
            "LeetCode": {"Easy": 6, "Medium": 4, "Hard": 2},
            "Codeforces": {"Easy": 1, "Medium": 2, "Hard": 1}
        }
        """
        result = {}
        for problem in self._get_raw_problems():
            if not isinstance(problem, dict):
                continue
            platform = problem.get("platform")
            if not isinstance(platform, str):
                continue
            platform = platform.strip()
            if not platform:
                continue

            if platform not in result:
                result[platform] = {"Easy": 0, "Medium": 0, "Hard": 0}

            difficulty = problem.get("difficulty")
            if isinstance(difficulty, str):
                normalized = difficulty.strip().capitalize()
                if normalized in result[platform]:
                    result[platform][normalized] += 1

        return result

    def get_platform_difficulty_counts(self):
        """Alias for get_difficulty_counts_by_platform."""
        return self.get_difficulty_counts_by_platform()

    def get_problem_statistics(self):
        """
        Return a consolidated dictionary of all problem statistics.
        """
        diff_counts = self.get_difficulty_counts()
        return {
            "total_solved": self.get_total_solved_count(),
            "easy": diff_counts["Easy"],
            "medium": diff_counts["Medium"],
            "hard": diff_counts["Hard"],
            "difficulty_counts": diff_counts,
            "platform_counts": self.get_platform_counts(),
            "platform_difficulty_counts": self.get_difficulty_counts_by_platform(),
        }

    # -------------------------------------------------------------------------
    # Topic / Pattern Statistics
    # -------------------------------------------------------------------------

    def _get_raw_topics(self):
        repo = self.topic_repository or self.problem_repository
        if not repo:
            return []
        if hasattr(repo, "get_all_topics"):
            try:
                topics = repo.get_all_topics()
                if not topics or not isinstance(topics, list):
                    return []
                return topics
            except Exception:
                return []
        return []

    def _get_raw_problem_topics(self):
        repo = self.topic_repository or self.problem_repository
        if not repo:
            return []
        for method_name in ("get_all_problem_topics", "get_problem_topics"):
            if hasattr(repo, method_name):
                try:
                    records = getattr(repo, method_name)()
                    if records and isinstance(records, list):
                        return records
                except Exception:
                    return []
        return []

    def get_topic_problem_counts(self):
        """
        Return problem counts per topic using the schema relationship:
        PROBLEMS <-> ProblemTopic <-> TOPIC.

        Returns a dictionary mapping topic name to problem count, sorted by
        count descending, and then alphabetically by topic name on ties.
        Example:
        {
            "Arrays": 12,
            "HashMap": 9,
            "Graphs": 4,
            "Sliding Window": 2
        }
        """
        raw_topics = self._get_raw_topics()
        raw_problem_topics = self._get_raw_problem_topics()

        id_to_name = {}
        topic_problems = defaultdict(set)

        # Register existing topics from TOPIC table
        for item in raw_topics:
            if not isinstance(item, dict):
                continue
            topic_id = item.get("topic_id", item.get("id"))
            topic_name = item.get("topic_name", item.get("name"))
            if isinstance(topic_name, str):
                topic_name = topic_name.strip()
                if topic_name:
                    if topic_id is not None:
                        id_to_name[topic_id] = topic_name
                    if topic_name not in topic_problems:
                        topic_problems[topic_name] = set()

        # Map ProblemTopic join records to topics
        for pt in raw_problem_topics:
            if not isinstance(pt, dict):
                continue
            prob_id = pt.get("problem_id")
            topic_id = pt.get("topic_id")
            topic_name = pt.get("topic_name")

            resolved_name = None
            if topic_id in id_to_name:
                resolved_name = id_to_name[topic_id]
            elif isinstance(topic_name, str) and topic_name.strip():
                resolved_name = topic_name.strip()

            if resolved_name and prob_id is not None:
                topic_problems[resolved_name].add(prob_id)

        # Fallback: if no dedicated join table records exist, inspect problem dicts
        if not topic_problems:
            for prob in self._get_raw_problems():
                if not isinstance(prob, dict):
                    continue
                prob_id = prob.get("problem_id")
                topics = prob.get("topics") or prob.get("topic_names")
                if isinstance(topics, (list, tuple, set)):
                    for t in topics:
                        if isinstance(t, str):
                            t = t.strip()
                            if t and prob_id is not None:
                                topic_problems[t].add(prob_id)

        # Sort by count descending, ties broken alphabetically
        sorted_topics = sorted(
            topic_problems.keys(),
            key=lambda name: (-len(topic_problems[name]), name)
        )

        return {name: len(topic_problems[name]) for name in sorted_topics}

    def get_topic_counts(self):
        """Alias for get_topic_problem_counts."""
        return self.get_topic_problem_counts()

    def get_most_practiced_topics(self, limit=None):
        """
        Return the most practiced topics and their problem counts.
        Ties are broken deterministically by topic name in alphabetical order.
        If limit is specified, returns at most limit items.
        """
        self._validate_limit(limit)
        all_counts = self.get_topic_problem_counts()
        if limit is not None:
            return dict(list(all_counts.items())[:limit])
        return dict(all_counts)

    def get_least_practiced_topics(self, limit=None):
        """
        Return the least practiced topics and their problem counts.
        Ties are broken deterministically by topic name in alphabetical order.
        If limit is specified, returns at most limit items.
        """
        self._validate_limit(limit)
        all_counts = self.get_topic_problem_counts()
        if not all_counts:
            return {}

        # Sort by count ascending, then topic name ascending
        sorted_items = sorted(all_counts.items(), key=lambda item: (item[1], item[0]))
        if limit is not None:
            sorted_items = sorted_items[:limit]
        return dict(sorted_items)

    # -------------------------------------------------------------------------
    # Revision Recommendations
    # -------------------------------------------------------------------------

    def get_revision_recommendations(self, limit=None):
        """
        Identify least-practiced topics and return them as revision recommendations.
        Deterministic order: least-practiced first, alphabetical on ties.
        Returns a list of topic names.
        """
        least_practiced = self.get_least_practiced_topics(limit=limit)
        return list(least_practiced.keys())

    def recommend_least_practiced_topics(self, limit=None):
        """Alias for get_revision_recommendations."""
        return self.get_revision_recommendations(limit=limit)

    def get_revision_recommendations_with_counts(self, limit=None):
        """
        Return revision recommendations mapped to their practice counts.
        """
        return self.get_least_practiced_topics(limit=limit)

    # -------------------------------------------------------------------------
    # Activity Data
    # -------------------------------------------------------------------------

    def get_activity_heatmap_data(self, user_id=None):
        """
        Prepare date -> activity count mapping from ACTIVITY records.
        This data is prepared for the GUI/Matplotlib to draw the coding activity heatmap.
        Does not generate the heatmap itself.
        Returns a dictionary mapping date -> count, sorted by date ascending.
        Example:
        {
            date(2026, 9, 10): 3,
            date(2026, 9, 11): 1,
            date(2026, 9, 12): 5
        }
        """
        if not self.activity_repository:
            return {}

        activities = []
        if user_id is not None:
            self._validate_user_id(user_id)
            if hasattr(self.activity_repository, "get_activities_by_user_id"):
                try:
                    activities = self.activity_repository.get_activities_by_user_id(user_id) or []
                except Exception:
                    activities = []
            elif hasattr(self.activity_repository, "get_all_activities"):
                try:
                    all_acts = self.activity_repository.get_all_activities() or []
                    activities = [a for a in all_acts if isinstance(a, dict) and a.get("user_id") == user_id]
                except Exception:
                    activities = []
        else:
            if hasattr(self.activity_repository, "get_all_activities"):
                try:
                    activities = self.activity_repository.get_all_activities() or []
                except Exception:
                    activities = []

        counts = defaultdict(int)
        for act in activities:
            if not isinstance(act, dict):
                continue
            raw_date = act.get("activity_date")
            parsed_date = self._parse_date(raw_date)
            if parsed_date is not None:
                counts[parsed_date] += 1

        sorted_dates = sorted(counts.keys())
        return {d: counts[d] for d in sorted_dates}

    def get_activity_counts_by_date(self, user_id=None):
        """Alias for get_activity_heatmap_data."""
        return self.get_activity_heatmap_data(user_id=user_id)

    def get_daily_activity_counts(self, user_id=None):
        """Alias for get_activity_heatmap_data."""
        return self.get_activity_heatmap_data(user_id=user_id)
