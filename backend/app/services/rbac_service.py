from sqlalchemy.orm import Session
from sqlalchemy import select, join
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import user_roles
from app.models.role_permission import role_permissions

def get_user_roles(db: Session, user_id: int):
    """Get all roles for a user"""
    return (
        db.query(Role)
        .join(user_roles, Role.id == user_roles.c.role_id)
        .filter(user_roles.c.user_id == user_id)
        .all()
    )

def get_user_permissions(db: Session, user_id: int):
    """Get all permissions for a user through their roles"""
    return (
        db.query(Permission.name)
        .join(role_permissions, Permission.id == role_permissions.c.permission_id)
        .join(user_roles, role_permissions.c.role_id == user_roles.c.role_id)
        .filter(user_roles.c.user_id == user_id)
        .all()
    )
