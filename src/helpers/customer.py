from sqlalchemy.orm import Session
from src import schemas, models


def find_customer(
    db: Session, phone_no: str, coffee_shop_id: int = None
) -> models.Customer:
    """
    This helper function used to get a customer by phone number and shop id.
    *Args:
        db (Session): SQLAlchemy Session object
        phone_no (str): Phone number to get a customer by phone number
        coffee_shop_id (int): Optional argument, to get the customer in this shop
    *Returns:
        the Customer instance if exists, None otherwise.
    """
    if coffee_shop_id:
        return (
            db.query(models.Customer)
            .filter(
                models.Customer.phone_no == phone_no,
                models.Customer.coffee_shop_id == coffee_shop_id,
            )
            .first()
        )
    return (
        db.query(models.Customer).filter(models.Customer.phone_no == phone_no).first()
    )


def create_customer(
    request: schemas.CustomerPOSTRequestBody,
    db: Session,
    coffee_shop_id: int,
):
    """
    This helper function used to create a new customer if not exists in a specific shop,
     else returns that customer
    *Args:
        request (schemas.CustomerPOSTRequestBody): contains customer details
    *Returns:
        the Customer instance
    """
    customer_instance = find_customer(
        db, phone_no=request.phone_no, coffee_shop_id=coffee_shop_id
    )
    if not customer_instance:
        customer_instance = models.Customer(
            phone_no=request.phone_no, name=request.name, coffee_shop_id=coffee_shop_id
        )
        db.add(customer_instance)
        db.commit()
        db.refresh(customer_instance)
    return customer_instance
