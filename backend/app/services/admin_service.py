from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.user_role import user_roles
from app.utils.password import hash_password
from app.services.audit_service import log_action

def create_admin_user(db: Session, email: str, password: str, role_name: str, actor_id):
    if role_name not in ["admin", "staff"]:
        raise ValueError("Invalid admin role")

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("User already exists")

    user = User(
        email=email,
        password_hash=hash_password(password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # assign role logic here...

    log_action(
        db=db,
        actor_id=actor_id,
        action="ADMIN_CREATE",
        resource="USER",
        resource_id=user.id,
        message=f"Admin created with role: {role_name}"
    )

    return user
