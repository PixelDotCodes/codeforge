"""
Activity Repository

Handles data access and SQL operations for the ACTIVITY table in PostgreSQL.
Responsible for executing parameterized queries and mapping database rows
to simple Python dictionaries.

ERD-confirmed schema for ACTIVITY:
    activity_id   INTEGER  PRIMARY KEY
    user_id       INTEGER  NOT NULL  REFERENCES USER(User_id)
    problem_id    INTEGER  NOT NULL  REFERENCES PROBLEMS(problem_id)
    activity_date DATE     NOT NULL
    activity_type VARCHAR  NOT NULL   -- 'New' or 'Revision'
"""

from contextlib import contextmanager
from database.connection import close_connection, get_connection


class ActivityRepository:
    """Data Access Layer for Activity operations.
    Aligned with the ERD table: ACTIVITY.
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

    @staticmethod
    def _row_to_dict(row):
        if not row:
            return None
        return {
            "activity_id": row[0],
            "user_id": row[1],
            "problem_id": row[2],
            "activity_date": row[3],
            "activity_type": row[4],
        }

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def has_activity_for_problem(self, user_id, problem_id):
        """Return True if any ACTIVITY row exists for the given user and problem."""
        query = """
            SELECT 1
            FROM ACTIVITY
            WHERE user_id = %s AND problem_id = %s
            LIMIT 1;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (user_id, problem_id))
            return cur.fetchone() is not None

    def get_activity_by_id(self, activity_id):
        """Return a single activity dict by primary key, or None if not found."""
        query = """
            SELECT activity_id, user_id, problem_id, activity_date, activity_type
            FROM ACTIVITY
            WHERE activity_id = %s;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (activity_id,))
            return self._row_to_dict(cur.fetchone())

    def get_activities_by_user_id(self, user_id):
        """Return all ACTIVITY rows for a given user, ordered by date then id."""
        query = """
            SELECT activity_id, user_id, problem_id, activity_date, activity_type
            FROM ACTIVITY
            WHERE user_id = %s
            ORDER BY activity_date ASC, activity_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (user_id,))
            return [self._row_to_dict(r) for r in cur.fetchall()]

    def get_activities_by_problem_id(self, problem_id):
        """Return all ACTIVITY rows for a given problem, ordered by date then id."""
        query = """
            SELECT activity_id, user_id, problem_id, activity_date, activity_type
            FROM ACTIVITY
            WHERE problem_id = %s
            ORDER BY activity_date ASC, activity_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (problem_id,))
            return [self._row_to_dict(r) for r in cur.fetchall()]

    def get_all_activities(self):
        """Return all ACTIVITY rows ordered by activity_id."""
        query = """
            SELECT activity_id, user_id, problem_id, activity_date, activity_type
            FROM ACTIVITY
            ORDER BY activity_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            return [self._row_to_dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def add_activity(self, user_id, problem_id, activity_date, activity_type):
        """Insert a new ACTIVITY row and return it as a dict."""
        query = """
            INSERT INTO ACTIVITY (user_id, problem_id, activity_date, activity_type)
            VALUES (%s, %s, %s, %s)
            RETURNING activity_id, user_id, problem_id, activity_date, activity_type;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, (user_id, problem_id, activity_date, activity_type))
            return self._row_to_dict(cur.fetchone())

    def delete_activity(self, activity_id):
        """Delete an ACTIVITY row by primary key. Returns True if a row was deleted."""
        query = """
            DELETE FROM ACTIVITY
            WHERE activity_id = %s;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, (activity_id,))
            return cur.rowcount > 0
