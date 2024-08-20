from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from src import schemas, models


def list_customers_orders(
    db: Session, coffee_shop_id: int, order_by: str = None, sort: str = None
) -> list[schemas.CustomerOrderReport]:
    """
    This helper function lists all customers along with their total orders or total paid amount
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter customers
        order_by (str): field to order by
        sort (str): sort order
    *Returns:
        list[schemas.CustomerOrderReport]: list of customers along with their total orders or total paid amount
    """
    query = (
        db.query(
            models.Customer.id,
            func.array_agg(models.Customer.name)[1].label("name"),
            func.array_agg(models.Customer.phone_no)[1].label("phone_no"),
            func.coalesce(func.count(func.distinct(models.Order.id)), 0).label(
                "total_orders"
            ),
            func.coalesce(
                func.sum(models.OrderItem.quantity * models.MenuItem.price), 0
            ).label("total_paid"),
        )
        .select_from(models.Customer)
        .outerjoin(models.Order, models.Customer.id == models.Order.customer_id)
        .outerjoin(models.OrderItem, models.Order.id == models.OrderItem.order_id)
        .outerjoin(models.MenuItem, models.OrderItem.item_id == models.MenuItem.id)
        .filter(models.Customer.coffee_shop_id == coffee_shop_id)
        .group_by(models.Customer.id)
    )

    if order_by:
        if sort == "desc":
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)  # default asc

    return query.all()
