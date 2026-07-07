def test_project_and_tasks(tmp_path):
    from app.repositories.project_repository import ProjectRepository
    from app.controllers.project_controller import ProjectController

    db_file = tmp_path / "projects.db"
    repo = ProjectRepository(str(db_file))
    controller = ProjectController(repo)
    controller.init_db()

    pid = controller.create_project(company_id=1, code="PRO-00001", name="Project X", client_id=1, status="planned", budget=10000.0)
    assert pid == 1
    tid1 = controller.create_task(project_id=pid, title="Task A", description="First task", assignee_id=1, due_date="2026-08-01")
    tid2 = controller.create_task(project_id=pid, title="Task B", description="Second task", assignee_id=2, due_date="2026-08-05")
    tasks = controller.list_tasks(pid)
    assert len(tasks) == 2
    assert tasks[0].title == "Task A"
