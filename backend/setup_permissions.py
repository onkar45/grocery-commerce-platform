#!/usr/bin/env python3
"""Setup basic permissions for testing"""

from app.db.session import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import role_permissions

def setup_basic_permissions():
    db = SessionLocal()
    try:
        # Create basic permissions if they don't exist
        permissions_data = [
            {"name": "read_users", "module": "users"},
            {"name": "read_products", "module": "products"},
        ]
        
        created_permissions = {}
        for perm_data in permissions_data:
            permission = db.query(Permission).filter(
                Permission.name == perm_data["name"],
                Permission.module == perm_data["module"]
            ).first()
            
            if not permission:
                permission = Permission(**perm_data)
                db.add(permission)
                db.flush()
                print(f"Created permission: {perm_data['name']}")
            
            created_permissions[perm_data["name"]] = permission
        
        # Get or create the "user" role
        user_role = db.query(Role).filter(Role.name == "user").first()
        if not user_role:
            user_role = Role(name="user", description="Regular user")
            db.add(user_role)
            db.flush()
            print("Created 'user' role")
        
        # Assign permissions to the user role
        for perm_name in ["read_users", "read_products"]:
            if perm_name in created_permissions:
                # Check if permission is already assigned
                existing = db.execute(
                    role_permissions.select().where(
                        role_permissions.c.role_id == user_role.id,
                        role_permissions.c.permission_id == created_permissions[perm_name].id
                    )
                ).first()
                
                if not existing:
                    db.execute(role_permissions.insert().values(
                        role_id=user_role.id,
                        permission_id=created_permissions[perm_name].id
                    ))
                    print(f"Assigned '{perm_name}' permission to 'user' role")
        
        db.commit()
        print("Setup completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_basic_permissions()