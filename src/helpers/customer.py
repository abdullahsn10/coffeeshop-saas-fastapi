from sqlalchemy.orm import Session
from src import schemas, models
from src.exceptions import ShopsAppException
from fastapi import status


def find_customer(
    db: Session,
    phone_no: str = None,
    customer_id: int = None,
    coffee_shop_id: int = None,
    exclude_customer_ids: list[int] = None,
) -> models.Customer:
    """
    This helper function used to get a customer by phone number/id and shop id.
    *Args:
        db (Session): SQLAlchemy Session object
        phone_no (str): Phone number to get a customer by phone number
        coffee_shop_id (int): Optional argument, to get the customer in this shop
        customer_id (int): the id of the customer
    *Returns:
        the Customer instance if exists, None otherwise.
    """
    if customer_id:
        query = db.query(models.Customer).filter(models.Customer.id == customer_id)
    else:
        query = db.query(models.Customer).filter(models.Customer.phone_no == phone_no)
    if coffee_shop_id:
        query = query.filter(models.Customer.coffee_shop_id == coffee_shop_id)
    if exclude_customer_ids:
        query = query.filter(models.Customer.id.notin_(exclude_customer_ids))
    return query.first()


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


def validate_customer_on_update(
    customer_id: int, coffee_shop_id: int, db: Session, customer_phone_no: str
) -> models.Customer:
    """
    This helper function used to validate the customer before updating.
    *Args:
        customer_id (int): the id of the customer needed to be updated
        coffee_shop_id (int): the id of the coffee shop in which the customer exists
        db (Session): SQLAlchemy Session object
        customer_phone_no (str): the phone number of the customer that must be unique
    *Returns:
        Raise Exceptions in case of violation, return the customer instance otherwise
    """

    found_customer = find_customer(
        db=db, customer_id=customer_id, coffee_shop_id=coffee_shop_id
    )
    if not found_customer:
        raise ShopsAppException(
            message="Customer Not found", status_code=status.HTTP_404_NOT_FOUND
        )

    # validate customer phone number uniqueness
    if find_customer(
        db=db,
        phone_no=customer_phone_no,
        coffee_shop_id=coffee_shop_id,
        exclude_customer_ids=[customer_id],
    ):
        raise ShopsAppException(
            message="Phone number already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return found_customer


def update_customer(
    request: schemas.CustomerPUTRequestBody,
    db: Session,
    coffee_shop_id: int,
    customer_id: int,
) -> schemas.CustomerResponse:
    """
    This helper function used to validate and update user.
    *Args:
        request (UserPUTRequestBody): The user details to update
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who updated the user.
        user_id (int): the id of the user needed to be updated
    *Returns:
        UserPUTAndPATCHResponse: The updated user details.
    """

    customer_instance: models.Customer = validate_customer_on_update(
        customer_id=customer_id,
        db=db,
        coffee_shop_id=coffee_shop_id,
        customer_phone_no=request.phone_no,
    )

    # Update all fields of the customer
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(customer_instance, field, value)

    db.commit()
    db.refresh(customer_instance)
    return schemas.CustomerResponse(
        id=customer_instance.id,
        name=customer_instance.name,
        phone_no=customer_instance.phone_no,
        coffee_shop_id=customer_instance.coffee_shop_id,
    )
