"""
Revision Repository

Handles data access and SQL operations for the REVISION table in PostgreSQL.
Responsible for executing parameterized queries and mapping database rows
to simple Python dictionaries.
"""

from contextlib import contextmanager
from database.connection import close_connection, get_connection


class RevisionRepository:
    """
    Data Access Layer for Revision operations.
    Aligned with the ERD table: REVISION.
    """

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
    def _row_to_dict(row):
        if not row:
            return None
        return {
            "revision_id": row[0],
            "problem_id": row[1],
            "revision_date": row[2],
            "revision_type": row[3],
        }

    def problem_exists(self, problem_id):
        query = """
            SELECT 1
            FROM PROBLEMS
            WHERE problem_id = %s;
        """
        with self._get_cursor(commit=False) as cur:
            cur.execute(query, (problem_id,))
            return cur.fetchone() is not None

    def add_revision(self, problem_id, revision_date, revision_type):
        query = """
            INSERT INTO REVISION (problem_id, revision_date, revision_type)
            VALUES (%s, %s, %s)
            RETURNING revision_id, problem_id, revision_date, revision_type;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, (problem_id, revision_date, revision_type))
            row = cur.fetchone()
            return self._row_to_dict(row)

    def get_revision_by_id(self, revision_id):
        query = """
            SELECT revision_id, problem_id, revision_date, revision_type
            FROM REVISION
            WHERE revision_id = %s;
        """
        with self._get_cursor(commit=False) as cur:
            cur.execute(query, (revision_id,))
            row = cur.fetchone()
            return self._row_to_dict(row)

    def get_revisions_by_problem_id(self, problem_id):
        query = """
            SELECT revision_id, problem_id, revision_date, revision_type
            FROM REVISION
            WHERE problem_id = %s
            ORDER BY revision_date ASC, revision_id ASC;
        """
        with self._get_cursor(commit=False) as cur:
            cur.execute(query, (problem_id,))
            rows = cur.fetchall()
            return [self._row_to_dict(r) for r in rows]

    def get_all_revisions(self):
        query = """
            SELECT revision_id, problem_id, revision_date, revision_type
            FROM REVISION
            ORDER BY revision_id ASC;
        """
        with self._get_cursor(commit=False) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [self._row_to_dict(r) for r in rows]

    def update_revision(self, revision_id, revision_date=None, revision_type=None):
        updates = []
        params = []

        if revision_date is not None:
            updates.append("revision_date = %s")
            params.append(revision_date)
        if revision_type is not None:
            updates.append("revision_type = %s")
            params.append(revision_type)

        if not updates:
            return self.get_revision_by_id(revision_id)

        params.append(revision_id)
        query = f"""
            UPDATE REVISION
            SET {", ".join(updates)}
            WHERE revision_id = %s
            RETURNING revision_id, problem_id, revision_date, revision_type;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return self._row_to_dict(row)

    def delete_revision(self, revision_id):
        query = """
            DELETE FROM REVISION
            WHERE revision_id = %s;
        """
        with self._get_cursor(commit=True) as cur:
            cur.execute(query, (revision_id,))
            return cur.rowcount > 0
