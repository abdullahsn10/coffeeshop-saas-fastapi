from sqlalchemy.orm import Session
from src import schemas, models
from src.exceptions.exception import *
from src.helpers import user, branch_user


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
    This helper function used to fully update a coffee shop\n
    *Args:
        request (CoffeeShopBase): contains coffee shop details\n
        db (Session): database session\n
        coffee_shop_id (int): coffee shop id\n
    *Returns:
        The updated coffee shop instance
    """

    found_coffee_shop: models.CoffeeShop = find_coffee_shop_by_id(
        db=db, coffee_shop_id=coffee_shop_id
    )
    if not found_coffee_shop:
        raise ShopsAppException(
            message=f"Coffee shop with id {coffee_shop_id} could not be found",
            status_code=404,
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


def get_all_branches(id: int, db: Session) -> list[models.Branch]:
    """
    This helper function used to get all branches of a coffee shop
    *Args:
        id (int): coffee shop id
        db (Session): database session
    *Returns:
        list[Branch]: List of branches
    """
    return db.query(models.Branch).filter(models.Branch.coffee_shop_id == id).all()


def get_all_admins(id: int, db: Session) -> list[models.User]:
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
            models.Branch.coffee_shop_id == id,
            models.User.role == models.UserRole.ADMIN,
            models.User.deleted == False,
        )
        .all()
    )


def attach_all_branches_to_admin(id: int, manager_id: int, db: Session) -> None:
    """
    This helper function used to attach all branches to a manager
    *Args:
        id (int): coffee shop id
        manager_id (int): manager id
        db (Session): database session
    """
    branches = get_all_branches(id=id, db=db)
    for branch in branches:
        branch_user.create(branch_id=branch.id, manager_id=manager_id, db=db)


def attach_branch_to_all_admins(
    coffee_shop_id: int, branch_id: int, db: Session
) -> None:
    """
    This helper function used to attach a branch to all admins of a coffee shop
    *Args:
        coffee_shop_id (int): coffee shop id
        branch_id (int): branch id
        db (Session): database session
    """
    admins = get_all_admins(id=coffee_shop_id, db=db)
    for admin in admins:
        branch_user.create(branch_id=branch_id, manager_id=admin.id, db=db)
