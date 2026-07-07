from datetime import datetime
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.services.auth import hash_password, verify_password


class UserController:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    def create_role(self, name: str, description: str = "") -> int:
        role = Role(name=name, description=description)
        return self.repo.add_role(role)

    def create_permission(self, name: str, description: str = "") -> int:
        p = Permission(name=name, description=description)
        return self.repo.add_permission(p)

    def assign_permission_to_role(self, role_id: int, permission_id: int):
        self.repo.assign_permission(role_id, permission_id)

    def create_user(self, username: str, email: str, password: str, company_id: int = None, role_id: int = None) -> int:
        pw_hash = hash_password(password)
        user = User(company_id=company_id, username=username, email=email, password_hash=pw_hash, role_id=role_id)
        return self.repo.add_user(user)

    def authenticate(self, username: str, password: str) -> bool:
        user = self.repo.get_user_by_username(username)
        if not user or not user.is_active:
            return False
        return verify_password(user.password_hash, password)
