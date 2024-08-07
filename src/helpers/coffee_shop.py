from sqlalchemy.orm import Session
from src import schemas, models
from src.exceptions.exception import *
from src.helpers import user


def create(request: schemas.CoffeeShopBase, db: Session) -> models.CoffeeShop:
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


def find_by_id(db: Session, id: int) -> models.CoffeeShop:
    """
    This helper function used to find a coffee shop by id
    :param db: db session
    :param id: the id of the coffee shop needed to be found
    :return: the coffee shop instance if the coffee shop was found, None otherwise
    """
    return db.query(models.CoffeeShop).filter(models.CoffeeShop.id == id).first()


def update(
    request: schemas.CoffeeShopBase, db: Session, id: int, user_coffe_shop_id: int
) -> models.CoffeeShop:
    """
    This helper function used to fully update a coffee shop
    :param request: coffee shop details
    :param db: db session
    :param id: the coffee shop id needed to be updated
    :param user_coffe_shop_id: the coffee shop in which user belongs it
    :return: the updated coffee shop instance if the coffee shop was found,
    or raise Exception if the coffee shop was not found or if the user not authorized
    to update this coffee shop
    """

    found_coffee_shop: models.CoffeeShop = find_by_id(db=db, id=id)
    if not found_coffee_shop:
        raise ShopsAppException(f"Coffee shop with id {id} could not be found")

    if user_coffe_shop_id != found_coffee_shop.id:
        raise ShopsAppUnAuthorizedException(
            f"You are not authorized to update this coffee shop"
        )

    # Update all fields of the coffee shop object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(found_coffee_shop, field, value)
    db.commit()
    db.refresh(found_coffee_shop)
    return found_coffee_shop
