from fastapi import FastAPI
from app.api import auth, users,admins,categories,products, public, inventory, orders, payments, refunds, order_status, admin_orders, admin_order_detail, audit_logs, admin_dashboard
from app.db.session import engine
from app.db.base import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Enterprise Grocery Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admins.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(public.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(refunds.router)
app.include_router(order_status.router)
app.include_router(admin_orders.router)
app.include_router(admin_order_detail.router)
app.include_router(audit_logs.router)
app.include_router(admin_dashboard.router)


@app.on_event("startup")
def create_tables():
    # Import models here to ensure they're registered with Base
    from app.models import user, role, permission, user_role, role_permission, category, product, inventory, order, order_item, payment, refund, audit_log
    Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "Auth system running"}
