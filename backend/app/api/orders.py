from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreateRequest, OrderResponse
from app.services.order_service import create_order, get_all_orders
from app.core.dependencies import get_db, get_current_user, require_permission
from app.models.order import Order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def place_order(
    data: OrderCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        order = create_order(db, user["user_id"], data.items)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/",
    response_model=list[OrderResponse],
    dependencies=[Depends(require_permission("order:read"))]
)
def list_orders(db: Session = Depends(get_db)):
    return get_all_orders(db)

@router.put(
    "/{order_id}/status",
    dependencies=[Depends(require_permission("order:update"))]
)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)

    return {"message": "Order status updated"}


@router.get(
    "/{order_id}",
    dependencies=[Depends(require_permission("order:read"))]
)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
        "user_email": order.user.email,
        "items": [
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.quantity * item.price
            }
            for item in order.items
        ]
    }

@router.get(
    "/{order_id}",
    dependencies=[Depends(require_permission("order:read"))]
)
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
        "user_email": order.user.email,
        "items": [
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in order.items
        ]
    }

@router.put(
    "/{order_id}/status",
    dependencies=[Depends(require_permission("order:update"))]
)
@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    raise Exception("🔥 THIS ROUTE IS HIT 🔥")
