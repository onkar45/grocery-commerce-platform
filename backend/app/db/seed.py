from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
from app.models.user_role import user_roles
from app.models.role_permission import role_permissions
from app.utils.password import hash_password

def seed():
    db: Session = SessionLocal()

    # ---------- ROLES ----------
    roles = ["super_admin", "admin", "user"]
    role_objects = {}

    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"{role_name} role")
            db.add(role)
            db.commit()
            db.refresh(role)
        role_objects[role_name] = role

    # ---------- PERMISSIONS ----------
    permissions = [
        ("user:read", "user"),
        ("user:create", "user"),
        ("product:create", "product"),
        ("product:update", "product"),
        ("product:delete", "product"),
        ("order:read", "order"),
        ("order:update", "order"),
        ("role:manage", "rbac"),
        ("permission:manage", "rbac"),
    ]

    permission_objects = []

    for name, module in permissions:
        perm = db.query(Permission).filter(Permission.name == name).first()
        if not perm:
            perm = Permission(name=name, module=module)
            db.add(perm)
            db.commit()
            db.refresh(perm)
        permission_objects.append(perm)

    # ---------- ASSIGN ALL PERMISSIONS TO SUPER ADMIN ----------
    super_admin_role = role_objects["super_admin"]

    for perm in permission_objects:
        exists = db.execute(
            role_permissions.select().where(
                (role_permissions.c.role_id == super_admin_role.id) &
                (role_permissions.c.permission_id == perm.id)
            )
        ).first()

        if not exists:
            db.execute(
                role_permissions.insert().values(
                    role_id=super_admin_role.id,
                    permission_id=perm.id
                )
            )

    db.commit()

    # ---------- CREATE SUPER ADMIN USER ----------
    email = "superadmin@grocery.com"
    password = "Admin@123"

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            password_hash=hash_password(password),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        db.execute(
            user_roles.insert().values(
                user_id=user.id,
                role_id=super_admin_role.id
            )
        )
        db.commit()

    db.close()
    print("✅ Super Admin, Roles & Permissions seeded successfully")

if __name__ == "__main__":
    seed()
