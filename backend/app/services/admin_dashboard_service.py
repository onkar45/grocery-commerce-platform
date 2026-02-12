from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.models.order import Order
from app.models.user import User

def get_dashboard_stats(db: Session):

    total_products = db.query(func.count(Product.id)).scalar()
    total_orders = db.query(func.count(Order.id)).scalar()
    total_users = db.query(func.count(User.id)).scalar()

    total_revenue = (
        db.query(func.sum(Order.total_amount))
        .filter(Order.status == "DELIVERED")
        .scalar()
        or 0
    )

    orders_by_status_raw = (
        db.query(Order.status, func.count(Order.id))
        .group_by(Order.status)
        .all()
    )
    
    # Convert tuples to dictionaries for JSON serialization
    orders_by_status = [
        {"status": status, "count": count}
        for status, count in orders_by_status_raw
    ]

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "total_revenue": float(total_revenue) if total_revenue else 0.0,
        "orders_by_status": orders_by_status,
    }
