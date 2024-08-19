from sqlalchemy.orm import Session
from src import schemas, models
from src.exceptions.exception import *
from src.helpers import user


def create_coffee_shop(
    request: schemas.CoffeeShopBase, db: Session
) -> models.CoffeeShop:
    """
    This helper function used to create a coffee shop
    *Args:
        request (CoffeeShopBase): contains coffee shop details
        db (Session): database session
    *Returns:
        CoffeeShop: created coffee shop instance
    """
    created_shop_instance: models.CoffeeShop = models.CoffeeShop(
        **request.model_dump(exclude_unset=True)
    )
    db.add(created_shop_instance)
    db.commit()
    db.refresh(created_shop_instance)
    return created_shop_instance


def find_coffee_shop(db: Session, coffee_shop_id: int) -> models.CoffeeShop:
    """
    This helper function used to find a coffee shop by id
    *Args:
        db (Session): database session
        coffee_shop_id (int): coffee shop id
    *Returns:
        The found coffee shop instance
    """
    query = db.query(models.CoffeeShop).filter(models.CoffeeShop.id == coffee_shop_id)
    found_coffee_shop = query.first()
    if not found_coffee_shop:
        raise ShopsAppException(
            message=f"Coffe Shop with id = {coffee_shop_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_coffee_shop


def update_coffee_shop(
    request: schemas.CoffeeShopBase, db: Session, coffee_shop_id: int
) -> schemas.CoffeeShopPUTResponse:
    """
    This helper function used to fully update a coffee shop
    *Args:
        request (CoffeeShopBase): contains coffee shop details
        db (Session): database session
        coffee_shop_id (int): coffee shop id
    *Returns:
        CoffeeShopPUTResponse: updated coffee shop details
    """

    found_coffee_shop: models.CoffeeShop = find_coffee_shop(
        db=db, coffee_shop_id=coffee_shop_id
    )
    # Update all fields of the coffee shop object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(found_coffee_shop, field, value)
    db.commit()
    db.refresh(found_coffee_shop)
    return schemas.CoffeeShopPUTResponse(
        name=found_coffee_shop.name,
        location=found_coffee_shop.location,
        contact_info=found_coffee_shop.contact_info,
    )
