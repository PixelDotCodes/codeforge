"""
Topic Repository

Handles data access and SQL operations for the TOPIC table and the
ProblemTopic join table in PostgreSQL.

ERD-confirmed schema:

    TOPIC table:
        topic_id   INTEGER  PRIMARY KEY
        topic_name VARCHAR  NOT NULL

    ProblemTopic table (join / associative entity):
        problem_id INTEGER  PRIMARY KEY, FOREIGN KEY -> PROBLEMS(problem_id)
        topic_id   INTEGER  PRIMARY KEY, FOREIGN KEY -> TOPIC(topic_id)
        Composite PK: (problem_id, topic_id)

AnalyticsService requires:
    - get_all_topics()         -> list[dict]  (topic_id, topic_name)
    - get_all_problem_topics() -> list[dict]  (problem_id, topic_id)
"""

from contextlib import contextmanager
from database.connection import close_connection, get_connection


class TopicRepository:
    """Data Access Layer for Topic and ProblemTopic operations.
    Aligned with the ERD tables: TOPIC and ProblemTopic.
    """

    def __init__(self, connection_provider=None):
        # Allows injection of a custom connection (e.g., a mock) for testing.
        self.connection_provider = connection_provider or get_connection

    def _get_connection(self):
        """Resolve the connection object.
        Returns a tuple (connection, should_close) where *should_close* indicates
        whether the repository created the connection and therefore must close it.
        """
        if callable(self.connection_provider):
            return self.connection_provider(), True
        return self.connection_provider, False

    @contextmanager
    def _get_cursor(self, commit=False):
        conn, should_close = self._get_connection()
        try:
            with conn.cursor() as cur:
                yield cur
            if commit and hasattr(conn, "commit"):
                conn.commit()
        except Exception:
            if hasattr(conn, "rollback"):
                try:
                    conn.rollback()
                except Exception:
                    pass
            raise
        finally:
            if should_close:
                close_connection(conn)

    # ------------------------------------------------------------------
    # TOPIC table operations
    # ------------------------------------------------------------------

    @staticmethod
    def _topic_row_to_dict(row):
        if not row:
            return None
        return {
            "topic_id": row[0],
            "topic_name": row[1],
        }

    def get_all_topics(self):
        """Return all rows from the TOPIC table, ordered by topic_id.

        Returns a list of dicts: [{"topic_id": int, "topic_name": str}, ...]
        Required by AnalyticsService.
        """
        query = """
            SELECT topic_id, topic_name
            FROM TOPIC
            ORDER BY topic_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            return [self._topic_row_to_dict(r) for r in cur.fetchall()]

    def get_topic_by_id(self, topic_id):
        """Return a single TOPIC row as a dict, or None if not found."""
        query = """
            SELECT topic_id, topic_name
            FROM TOPIC
            WHERE topic_id = %s;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (topic_id,))
            return self._topic_row_to_dict(cur.fetchone())

    # ------------------------------------------------------------------
    # ProblemTopic join table operations
    # ------------------------------------------------------------------

    @staticmethod
    def _problem_topic_row_to_dict(row):
        if not row:
            return None
        return {
            "problem_id": row[0],
            "topic_id": row[1],
        }

    def get_all_problem_topics(self):
        """Return all rows from the ProblemTopic join table.

        Returns a list of dicts: [{"problem_id": int, "topic_id": int}, ...]
        Required by AnalyticsService to compute per-topic problem counts.
        """
        query = """
            SELECT problem_id, topic_id
            FROM ProblemTopic
            ORDER BY problem_id ASC, topic_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            return [self._problem_topic_row_to_dict(r) for r in cur.fetchall()]

    def get_topics_for_problem(self, problem_id):
        """Return all ProblemTopic rows for a specific problem."""
        query = """
            SELECT problem_id, topic_id
            FROM ProblemTopic
            WHERE problem_id = %s
            ORDER BY topic_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (problem_id,))
            return [self._problem_topic_row_to_dict(r) for r in cur.fetchall()]

    def get_problems_for_topic(self, topic_id):
        """Return all ProblemTopic rows for a specific topic."""
        query = """
            SELECT problem_id, topic_id
            FROM ProblemTopic
            WHERE topic_id = %s
            ORDER BY problem_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (topic_id,))
            return [self._problem_topic_row_to_dict(r) for r in cur.fetchall()]
