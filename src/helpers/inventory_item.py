from datetime import date

from src import schemas, models
from sqlalchemy.orm import Session
from src.helpers import coffee_shop
from src.exceptions.exception import *


def _validate_prod_and_expire_date_in_item(
    prod_date: date,
    expire_date: date,
) -> None:
    """
    This helper function will be used to validate the production and
    expiration date.
    *Args:
        prod_date (int): The prod date.
        expire_date (int): The expiration date.
    *Returns:
        raise ShopsAppException if there is any violation
    """
    if prod_date > expire_date:
        raise ShopsAppException(
            message=f"Production date cannot be greater than expiration date",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def create_inventory_item(
    request: schemas.InventoryItemPOSTRequestBody, coffee_shop_id: int, db: Session
) -> models.InventoryItem:
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
    found_shop = coffee_shop._find_coffee_shop(db=db, coffee_shop_id=coffee_shop_id)

    # validate prod date and expire date
    _validate_prod_and_expire_date_in_item(
        prod_date=request.prod_date,
        expire_date=request.expire_date,
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


def _find_inventory_item(
    db: Session, inventory_item_id: int, coffee_shop_id: Optional[int] = None
) -> models.InventoryItem:
    """
    This helper function will be used to find a specific inventory item by id and
    the shop id.
    *Args:
        db (Session): the database session
        inventory_item_id (int): the id of the inventory item needed to be found
        coffee_shop_id (int): the id of the coffee shop that the item belongs to
    *Returns:
        the found inventory item or None if it does not exist
    """
    query = db.query(models.InventoryItem).filter(
        models.InventoryItem.id == inventory_item_id,
        models.InventoryItem.deleted == False,
    )
    if coffee_shop_id:
        query = query.filter(models.InventoryItem.coffee_shop_id == coffee_shop_id)

    found_inventory_item = query.first()
    if not found_inventory_item:
        raise ShopsAppException(
            message=f"This item with id = {inventory_item_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_inventory_item


def find_all_inventory_items(
    coffee_shop_id: int, db: Session
) -> list[models.InventoryItem]:
    """
    This helper function will be used to find all inventory items in a specific coffee shop.
    *Args:
        coffee_shop_id (int): the id of the coffee shop
        db (Session): the database session
    *Returns:
        the found inventory items
    """
    query = db.query(models.InventoryItem).filter(
        models.InventoryItem.deleted == False,
        models.InventoryItem.coffee_shop_id == coffee_shop_id,
    )
    return query.all()


def update_inventory_item(
    request: schemas.InventoryItemPUTRequestBody,
    db: Session,
    inventory_item_id: int,
    admin_coffee_shop_id: int,
) -> models.InventoryItem:
    """
    This helper function will be used to update a specific inventory item.
    *Args:
        request (schemas.InventoryItemPUTRequestBody): the details of the inventory item
        db (Session): the database session
        inventory_item_id (int): the id of the inventory item to be updated
        admin_coffee_shop_id (int): the id of the coffee shop that the item must belongs to
    *Returns:
        the updated inventory item
    """
    found_inventory_item: models.InventoryItem = _find_inventory_item(
        db=db,
        inventory_item_id=inventory_item_id,
        coffee_shop_id=admin_coffee_shop_id,
    )
    # validate prod and expire date
    _validate_prod_and_expire_date_in_item(
        prod_date=request.prod_date,
        expire_date=request.expire_date,
    )

    # Update all fields of the inventory item object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(found_inventory_item, field, value)
    db.commit()
    db.refresh(found_inventory_item)
    return found_inventory_item


def delete_inventory_item(
    db: Session, inventory_item_id: int, admin_coffee_shop_id: int
) -> None:
    """
    This helper function will be used to delete an inventory item by id.
    *Args:
        db (Session): database session
        inventory_item_id (int): the id of the inventory item to be deleted
        admin_coffee_shop_id (int): the id of the coffee shop that the item must belongs to
    *Returns:
        None
    """

    # check if the branch belongs to this coffee shop
    found_inventory_item: models.InventoryItem = _find_inventory_item(
        db=db,
        inventory_item_id=inventory_item_id,
        coffee_shop_id=admin_coffee_shop_id,
    )

    found_inventory_item.deleted = True
    db.commit()
