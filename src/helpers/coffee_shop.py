from sqlalchemy.orm import Session
from src import schemas, models


def create(request: schemas.CoffeeShopBase, db: Session) -> models.CoffeeShop:
    """
    This helper function used to create a coffee shop
    *Args:
        request (CoffeeShopBase): contains coffee shop details
        db (Session): database session
    *Returns:
        CoffeeShop: created coffee shop instance
    """
    created_shop_instance: models.CoffeeShop \
        = models.CoffeeShop(**request.model_dump(exclude_unset=True))
    db.add(created_shop_instance)
    db.commit()
    db.refresh(created_shop_instance)
    return created_shop_instance
