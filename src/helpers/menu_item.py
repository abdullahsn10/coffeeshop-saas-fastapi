from datetime import date
from src import schemas, models
from sqlalchemy.orm import Session
from src.helpers import coffee_shop
from src.exceptions.exception import *


def create_menu_item(
    request: schemas.MenuItemPOSTRequestBody, coffee_shop_id: int, db: Session
) -> models.MenuItem:
    """
    This helper function will be used to create a new menu item.
    *Args:
        request (schemas.MenuItemPOSTRequestBody): the details of the menu item
        coffee_shop_id (int): the id of the coffee shop to create the menu item for
        db (Session): the database session
    *Returns:
        the created menu item
    """
    # check if the shop exists (Additional Logic, only to ensure everything is okay)
    found_shop = coffee_shop.find_coffee_shop(db=db, coffee_shop_id=coffee_shop_id)

    created_menu_item = models.MenuItem(
        name=request.name,
        description=request.description,
        price=request.price,
        coffee_shop_id=coffee_shop_id,
    )
    db.add(created_menu_item)
    db.commit()
    db.refresh(created_menu_item)
    return created_menu_item


def find_menu_item(
    db: Session, menu_item_id: int, coffee_shop_id: Optional[int] = None
) -> models.MenuItem:
    """
    This helper function will be used to find a specific menu item by id.
    *Args:
        db (Session): the database session
        menu_item_id (int): the id of the menu item needed to be found
    *Returns:
    the found menu item or None if it does not exist
    """
    if coffee_shop_id:
        return (
            db.query(models.MenuItem)
            .filter(
                models.MenuItem.id == menu_item_id,
                models.MenuItem.coffee_shop_id == coffee_shop_id,
                models.MenuItem.deleted == False,
            )
            .first()
        )
    return (
        db.query(models.MenuItem)
        .filter(
            models.MenuItem.id == menu_item_id,
            models.MenuItem.deleted == False,
        )
        .first()
    )


def update_menu_item(
    request: schemas.MenuItemPUTRequestBody,
    db: Session,
    menu_item_id: int,
    admin_coffee_shop_id: int,
):
    """
    This helper function will be used to update a specific menu item.
    *Args:
        request (schemas.MenuItemPUTRequestBody): the details of the menu item
        db (Session): the database session
        menu_item_id (int): the id of the menu item to be updated
        admin_coffee_shop_id (int): the id of the coffee shop that the item must belongs to
    *Returns:
        the updated menu item
    """
    found_menu_item: models.MenuItem = find_menu_item(
        db=db, menu_item_id=menu_item_id, coffee_shop_id=admin_coffee_shop_id
    )

    if not found_menu_item:
        raise ShopsAppException(
            message=f"This item with id = {menu_item_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Update all fields of the menu item object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(found_menu_item, field, value)
    db.commit()
    db.refresh(found_menu_item)
    return found_menu_item


def delete_menu_item_by_id(
    db: Session, menu_item_id: int, admin_coffee_shop_id: int
) -> None:
    """
    This helper function will be used to delete a menu item by id.
    *Args:
        db (Session): database session
        menu_item_id (int): the id of the menu item to be deleted
        admin_coffee_shop_id (int): the id of the coffee shop that the item must belongs to
    *Returns:
        None
    """

    # check if the branch belongs to this coffee shop
    found_menu_item: models.MenuItem = find_menu_item(
        db=db, menu_item_id=menu_item_id, coffee_shop_id=admin_coffee_shop_id
    )
    if not found_menu_item:
        raise ShopsAppException(
            message=f"This item with id = {menu_item_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    found_menu_item.deleted = True
    db.commit()
