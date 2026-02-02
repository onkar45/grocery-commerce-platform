from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.user_role import user_roles
from app.utils.password import hash_password, verify_password

def create_user(db: Session, email: str, password: str):
    user = User(
        email=email,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assign_role_to_user(db, user.id, "user")
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def assign_role_to_user(db, user_id: int, role_name: str):
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        # Create the role if it doesn't exist
        role = Role(name=role_name, description=f"Default {role_name} role")
        db.add(role)
        db.commit()
        db.refresh(role)

    # Check if user already has this role
    existing = db.execute(
        user_roles.select().where(
            user_roles.c.user_id == user_id,
            user_roles.c.role_id == role.id
        )
    ).first()
    
    if not existing:
        db.execute(user_roles.insert().values(
            user_id=user_id,
            role_id=role.id
        ))
        db.commit()