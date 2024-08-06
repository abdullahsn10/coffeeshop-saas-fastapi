from sqlalchemy.orm import Session
from shops_app.schemas.coffee_shop import CoffeeShopBase
from shops_app.models import CoffeeShop


def create(request: CoffeeShopBase, db: Session) -> CoffeeShop:
    """
    This helper function used to create a coffee shop
    *Args:
        request (CoffeeShopBase): contains coffee shop details
        db (Session): database session
    *Returns:
        CoffeeShop: created coffee shop instance
    """
    created_shop_instance: CoffeeShop = CoffeeShop(**request.model_dump(exclude_unset=True))
    db.add(created_shop_instance)
    db.commit()
    db.refresh(created_shop_instance)
    return created_shop_instance
