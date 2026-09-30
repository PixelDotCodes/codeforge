"""
Analytics Service

This module handles the business and aggregation logic for analytics and statistics
in CodeForge. It aggregates raw data from problem and activity records.
"""

from collections import defaultdict
from datetime import date, datetime


class AnalyticsService:
    def __init__(
        self,
        problem_repository=None,
        activity_repository=None,
        topic_repository=None,
    ):

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
        return self.get_total_solved_count()

    def get_difficulty_counts(self):
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
    def get_activity_heatmap_data(self, user_id=None):
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

    def get_practice_consistency(self, user_id=None, as_of_date=None):
        """
        Calculate practice consistency for the current month:
        distinct active practice days in the current month / current day-of-month * 100.
        """
        today = as_of_date or date.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        heatmap_data = self.get_activity_heatmap_data(user_id=user_id) or {}
        active_days = sum(
            1 for d in heatmap_data.keys()
            if d.year == current_year and d.month == current_month
        )

        denominator = current_day
        percentage = (active_days / denominator * 100.0) if denominator > 0 else 0.0

        return {
            "active_days": active_days,
            "denominator": denominator,
            "percentage": percentage,
            "formatted_percentage": f"{round(percentage)}%",
            "display_text": f"{active_days} of {denominator} days active",
        }


    def get_problem_practice_counts(self):
        """
        Return a mapping of problem_id -> practice count.
        Counts only relevant activity records representing problem practice/review
        (activity_type in ('New', 'Revision')).
        All existing problems in problem_repository are included (unpracticed problems have count 0).
        """
        raw_problems = self._get_raw_problems()
        practice_counts = {
            p["problem_id"]: 0
            for p in raw_problems
            if isinstance(p, dict) and "problem_id" in p
        }

        if self.activity_repository and hasattr(self.activity_repository, "get_all_activities"):
            try:
                activities = self.activity_repository.get_all_activities() or []
                for act in activities:
                    if not isinstance(act, dict):
                        continue
                    act_type = act.get("activity_type")
                    if act_type in ("New", "Revision"):
                        prob_id = act.get("problem_id")
                        if prob_id in practice_counts:
                            practice_counts[prob_id] += 1
                        elif prob_id is not None:
                            practice_counts[prob_id] = 1
            except Exception:
                pass

        return practice_counts

    def get_suggested_questions_for_review(self, limit=5):
        """
        Return suggested questions to review based on practice history.

        Priority:
        1. Questions practiced/saved fewer than 5 times.
        2. After those are exhausted, questions practiced/saved fewer than 10 times.
        3. Excluded: questions that have reached 10 or more practice records.

        Returns at most `limit` questions (default 5), ordered by least-practiced first.
        Ties are broken deterministically by problem_id ascending.
        If no eligible questions exist, returns an empty list.
        """
        self._validate_limit(limit)
        raw_problems = self._get_raw_problems()
        if not raw_problems:
            return []

        prob_map = {
            p["problem_id"]: p
            for p in raw_problems
            if isinstance(p, dict) and "problem_id" in p
        }
        counts = self.get_problem_practice_counts()

        group_lt_5 = []
        group_lt_10 = []

        for pid, prob in prob_map.items():
            cnt = counts.get(pid, 0)
            if cnt < 5:
                group_lt_5.append((cnt, pid, prob))
            elif cnt < 10:
                group_lt_10.append((cnt, pid, prob))
            # cnt >= 10 are completely excluded

        # Prefer least-practiced first; ties broken deterministically by problem_id
        group_lt_5.sort(key=lambda x: (x[0], x[1]))
        group_lt_10.sort(key=lambda x: (x[0], x[1]))

        candidates = group_lt_5 + group_lt_10
        selected = candidates[:limit]

        result = []
        for cnt, pid, prob in selected:
            result.append({
                "problem_id": pid,
                "title": prob.get("title", ""),
                "platform": prob.get("platform", ""),
                "platform_question_no": prob.get("platform_question_no") or prob.get("question_number", ""),
                "difficulty": prob.get("difficulty", ""),
                "problem_url": prob.get("problem_url", ""),
                "practice_count": cnt,
            })
        return result

    def get_top_practiced_problem(self):
        """
        Return the most-practiced problem based on actual activity records.
        Returns a dict with problem details and practice_count, or None if no practice data.
        """
        counts = self.get_problem_practice_counts()
        if not counts:
            return None

        practiced = [(pid, cnt) for pid, cnt in counts.items() if cnt > 0]
        if not practiced:
            return None

        practiced.sort(key=lambda x: (-x[1], x[0]))
        top_pid, top_count = practiced[0]

        raw_problems = self._get_raw_problems()
        prob_map = {
            p["problem_id"]: p
            for p in raw_problems
            if isinstance(p, dict) and "problem_id" in p
        }
        prob = prob_map.get(top_pid)
        if not prob and self.problem_repository and hasattr(self.problem_repository, "get_problem_by_id"):
            try:
                prob = self.problem_repository.get_problem_by_id(top_pid)
            except Exception:
                prob = None

        if not prob:
            return None

        return {
            "problem_id": top_pid,
            "title": prob.get("title", ""),
            "platform": prob.get("platform", ""),
            "platform_question_no": prob.get("platform_question_no") or prob.get("question_number", ""),
            "difficulty": prob.get("difficulty", ""),
            "problem_url": prob.get("problem_url", ""),
            "practice_count": top_count,
        }

