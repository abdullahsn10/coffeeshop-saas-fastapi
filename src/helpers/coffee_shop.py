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


def find_coffee_shop_by_id(db: Session, coffee_shop_id: int) -> models.CoffeeShop:
    """
    This helper function used to find a coffee shop by id
    *Args:
        db (Session): database session
        coffee_shop_id (int): coffee shop id
    *Returns:
        The found coffee shop instance
    """
    return (
        db.query(models.CoffeeShop)
        .filter(models.CoffeeShop.id == coffee_shop_id)
        .first()
    )


def update_coffee_shop(
    request: schemas.CoffeeShopBase, db: Session, coffee_shop_id: int
) -> models.CoffeeShop:
    """
    This helper function used to fully update a coffee shop
    *Args:
        request (CoffeeShopBase): contains coffee shop details
        db (Session): database session
        coffee_shop_id (int): coffee shop id
    *Returns:
        The updated coffee shop instance
    """

    found_coffee_shop: models.CoffeeShop = find_coffee_shop_by_id(
        db=db, coffee_shop_id=coffee_shop_id
    )
    if not found_coffee_shop:
        raise ShopsAppException(
            message=f"Coffee shop with id {coffee_shop_id} could not be found",
            status_code=status.HTTP_404_NOT_FOUND,
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


def is_shop_has_this_branch(coffee_shop_id: int, branch_id: int, db: Session) -> bool:
    """
    This helper function used to check if a coffee shop has a specific branch
    *Args:
        coffee_shop_id (int): coffee shop id
        branch_id (int): branch id
        db (Session): database session
    *Returns:
        bool: True if the coffee shop has the branch, False otherwise
    """
    return (
        db.query(models.Branch)
        .filter(
            models.Branch.id == branch_id,
            models.Branch.deleted == False,
            models.Branch.coffee_shop_id == coffee_shop_id,
        )
        .first()
        is not None
    )


def get_all_branches_in_the_shop(
    coffee_shop_id: int, db: Session
) -> list[models.Branch]:
    """
    This helper function used to get all branches of a coffee shop
    *Args:
        id (int): coffee shop id
        db (Session): database session
    *Returns:
        list[Branch]: List of branches
    """
    return (
        db.query(models.Branch)
        .filter(
            models.Branch.coffee_shop_id == coffee_shop_id,
            models.Branch.deleted == False,
        )
        .all()
    )


def get_all_admins_in_the_shop(coffee_shop_id: int, db: Session) -> list[models.User]:
    """
    This helper function used to get all admins of a coffee shop
    *Args:
        id (int): coffee shop id
        db (Session): database session
    *Returns:
        list[User]: List of admins
    """
    return (
        db.query(models.User)
        .filter(
            models.User.branch_id == models.Branch.id,
            models.Branch.coffee_shop_id == coffee_shop_id,
            models.User.role == models.UserRole.ADMIN,
            models.User.deleted == False,
        )
        .all()
    )


def get_all_inventory_items_in_the_shop(
    db: Session, coffee_shop_id: int
) -> list[models.InventoryItem]:
    """
    This helper function used to get all inventory items of a coffee shop
    *Args:
        coffee_shop_id (int): the id of the coffee shop needed to retrieve inventory items from
        db (Session): database session
    *Returns:
        a list of inventory items
    """
    return (
        db.query(models.InventoryItem)
        .filter(
            models.InventoryItem.coffee_shop_id == coffee_shop_id,
            models.InventoryItem.deleted == False,
        )
        .all()
    )


def get_all_menu_items_in_the_shop(
    db: Session, coffee_shop_id: int
) -> list[models.MenuItem]:
    """
    This helper function used to get all menu items of a coffee shop
    *Args:
        coffee_shop_id (int): the id of the coffee shop needed to retrieve menu items from
        db (Session): database session
    *Returns:
        a list of menu items
    """
    return (
        db.query(models.MenuItem)
        .filter(
            models.MenuItem.coffee_shop_id == coffee_shop_id,
            models.MenuItem.deleted == False,
        )
        .all()
    )


def get_user_in_the_shop_by_email(
    user_email: str, db: Session, coffee_shop_id: int
) -> models.User:
    """
    This helper function used to get a user in the shop by email
    *Args:
        user_email (str): email of the user
        db (Session): database session
        coffee_shop_id (int): coffee shop id of the user
    *Returns:
        the retrieved user if found, else None
    """
    return (
        db.query(models.User)
        .filter(
            models.User.email == user_email,
            models.User.branch_id == models.Branch.id,
            models.Branch.coffee_shop_id == coffee_shop_id,
        )
        .first()
    )


def get_user_in_the_shop_by_phone(
    user_phone_no: str, db: Session, coffee_shop_id: int
) -> models.User:
    """
    This helper function used to get a user in the shop by phone number
    *Args:
        phone_no (str): phone number of the user
        db (Session): database session
        coffee_shop_id (int): coffee shop id of the user
    *Returns:
        the retrieved user if found, else None
    """
    return (
        db.query(models.User)
        .filter(
            models.User.phone_no == user_phone_no,
            models.User.branch_id == models.Branch.id,
            models.Branch.coffee_shop_id == coffee_shop_id,
        )
        .first()
    )
