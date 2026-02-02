from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.user_role import user_roles
from app.utils.password import hash_password

def create_admin_user(db: Session, email: str, password: str, role_name: str):
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

    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError("Role not found")

    db.execute(
        user_roles.insert().values(
            user_id=user.id,
            role_id=role.id
        )
    )
    db.commit()

    return user
