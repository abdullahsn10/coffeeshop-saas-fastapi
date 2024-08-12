from src import schemas, models
from sqlalchemy.orm import Session
from src.helpers import coffee_shop
from src.exceptions.exception import *


def create_inventory_item(
    request: schemas.InventoryItemPOSTRequestBody, coffee_shop_id: int, db: Session
):
    """
    This helper function will be used to create a new inventory item.
    *Args:
        request (schemas.InventoryItemPOSTRequestBody): the details of the inventory item
        coffee_shop_id (int): the id of the coffee shop that the item belongs to
        db (Session): the database session
    *Returns:
        the created inventory item
    """
    # check if the shop exists (Additional Logic, only to ensure everything is okay)
    if not coffee_shop.find_coffee_shop_by_id(db=db, coffee_shop_id=coffee_shop_id):
        raise ShopsAppException(
            message=f"Coffe Shop with id = {coffee_shop_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # validate prod date and expire date
    if request.prod_date > request.expire_date:
        raise ShopsAppException(
            message=f"Production date cannot be greater than expiration date",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    created_inventory_item = models.InventoryItem(
        name=request.name,
        price=request.price,
        prod_date=request.prod_date,
        expire_date=request.expire_date,
        available_quantity=request.available_quantity,
        coffee_shop_id=coffee_shop_id,
    )
    db.add(created_inventory_item)
    db.commit()
    db.refresh(created_inventory_item)
    return created_inventory_item
