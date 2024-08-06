from fastapi import FastAPI
from shops_app.routers import (authentication, branch, coffee_shop,
                               customer, inventory_item, menu_item,
                               order, report, user)


app = FastAPI()

# register routes
app.include_router(authentication.router)
app.include_router(coffee_shop.router)
app.include_router(user.router)
app.include_router(branch.router)
app.include_router(customer.router)
app.include_router(inventory_item.router)
app.include_router(menu_item.router)
app.include_router(order.router)
app.include_router(report.router)



