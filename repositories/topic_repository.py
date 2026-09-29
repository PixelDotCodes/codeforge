"""
Topic Repository

Handles data access and SQL operations for the TOPIC table and the
ProblemTopic join table in PostgreSQL.
"""

from contextlib import contextmanager
from database.connection import close_connection, get_connection


class TopicRepository:

    def __init__(self, connection_provider=None):
        self.connection_provider = connection_provider or get_connection

    def _get_connection(self):
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
    def _topic_row_to_dict(row):
        if not row:
            return None
        return {
            "topic_id": row[0],
            "topic_name": row[1],
        }

    def get_all_topics(self):
        query = """
            SELECT topic_id, topic_name
            FROM TOPIC
            ORDER BY topic_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            return [self._topic_row_to_dict(r) for r in cur.fetchall()]



    @staticmethod
    def _problem_topic_row_to_dict(row):
        if not row:
            return None
        return {
            "problem_id": row[0],
            "topic_id": row[1],
        }

    def get_all_problem_topics(self):
        query = """
            SELECT problem_id, topic_id
            FROM ProblemTopic
            ORDER BY problem_id ASC, topic_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            return [self._problem_topic_row_to_dict(r) for r in cur.fetchall()]
