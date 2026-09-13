"""
Problem Repository

Handles data access and SQL operations for the PROBLEMS table in PostgreSQL.
Responsible for executing parameterized queries and mapping database rows
to simple Python dictionaries.
"""

from contextlib import contextmanager
from database.connection import close_connection, get_connection


class ProblemRepository:
    """Data Access Layer for Problem operations.
    Aligned with the ERD table: PROBLEMS.
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
    def _get_cursor(self, commit: bool = False):
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
            "problem_id": row[0],
            "platform": row[1],
            "platform_question_no": row[2],
            "title": row[3],
            "difficulty": row[4],
            "problem_url": row[5],
        }

    # ---------------------------------------------------------------------
    # CRUD operations
    # ---------------------------------------------------------------------
    def add_problem(self, platform, question_number, title, difficulty, problem_url):
        query = """
            INSERT INTO PROBLEMS (platform, platform_question_no, title, difficulty, problem_url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING problem_id, platform, platform_question_no, title, difficulty, problem_url;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, (platform, question_number, title, difficulty, problem_url))
            row = cur.fetchone()
            return self._row_to_dict(row)

    def get_problem_by_id(self, problem_id):
        query = """
            SELECT problem_id, platform, platform_question_no, title, difficulty, problem_url
            FROM PROBLEMS
            WHERE problem_id = %s;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (problem_id,))
            return self._row_to_dict(cur.fetchone())

    def get_all_problems(self):
        query = """
            SELECT problem_id, platform, platform_question_no, title, difficulty, problem_url
            FROM PROBLEMS
            ORDER BY problem_id ASC;
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [self._row_to_dict(r) for r in rows]

    def update_problem(
        self,
        problem_id,
        platform=None,
        question_number=None,
        title=None,
        difficulty=None,
        problem_url=None,
    ):
        updates = []
        params = []
        if platform is not None:
            updates.append("platform = %s")
            params.append(platform)
        if question_number is not None:
            updates.append("platform_question_no = %s")
            params.append(question_number)
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if difficulty is not None:
            updates.append("difficulty = %s")
            params.append(difficulty)
        if problem_url is not None:
            updates.append("problem_url = %s")
            params.append(problem_url)
        if not updates:
            # Nothing to update – just return the existing record.
            return self.get_problem_by_id(problem_id)
        params.append(problem_id)
        query = f"""
            UPDATE PROBLEMS
            SET {', '.join(updates)}
            WHERE problem_id = %s
            RETURNING problem_id, platform, platform_question_no, title, difficulty, problem_url;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, tuple(params))
            return self._row_to_dict(cur.fetchone())

    def delete_problem(self, problem_id):
        query = """
            DELETE FROM PROBLEMS
            WHERE problem_id = %s;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, (problem_id,))
            return cur.rowcount > 0

    def get_problem_by_platform_and_question_number(self, platform, question_number):
        query = """
            SELECT problem_id, platform, platform_question_no, title, difficulty, problem_url
            FROM PROBLEMS
            WHERE platform = %s AND platform_question_no = %s;
        """
        with self._get_cursor() as cur:
            cur.execute(query, (platform, question_number))
            return self._row_to_dict(cur.fetchone())
