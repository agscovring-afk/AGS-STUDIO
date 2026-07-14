import sqlite3
from datetime import datetime
from typing import Optional, List
from app.models.project import Project
from app.models.task import Task


class ProjectRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_tables(self):
        with self._conn() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    code TEXT UNIQUE,
                    name TEXT,
                    client_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    actual_end TEXT,
                    status TEXT,
                    budget REAL,
                    description TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS project_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    title TEXT,
                    description TEXT,
                    assignee_id INTEGER,
                    due_date TEXT,
                    priority TEXT,
                    status TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
                )
                """
            )

    def add_project(self, p: Project) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO projects (company_id, code, name, client_id, start_date, end_date, actual_end, status, budget, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (p.company_id, p.code, p.name, p.client_id, p.start_date, p.end_date, p.actual_end, p.status, p.budget, p.description, p.created_at.isoformat(), p.updated_at.isoformat()),
            )
            return cur.lastrowid

    def get_project(self, project_id: int) -> Optional[Project]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
            if not r:
                return None
            return Project(id=r['id'], company_id=r['company_id'], code=r['code'], name=r['name'], client_id=r['client_id'], start_date=r['start_date'], end_date=r['end_date'], actual_end=r['actual_end'], status=r['status'], budget=r['budget'], description=r['description'])

    def add_task(self, t: Task) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO project_tasks (project_id, title, description, assignee_id, due_date, priority, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (t.project_id, t.title, t.description, t.assignee_id, t.due_date, t.priority, t.status, t.created_at.isoformat(), t.updated_at.isoformat()),
            )
            return cur.lastrowid

    def list_tasks(self, project_id: int) -> List[Task]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM project_tasks WHERE project_id = ? ORDER BY id", (project_id,)).fetchall()
            return [Task(id=r['id'], project_id=r['project_id'], title=r['title'], description=r['description'], assignee_id=r['assignee_id'], due_date=r['due_date'], priority=r['priority'], status=r['status']) for r in rows]
