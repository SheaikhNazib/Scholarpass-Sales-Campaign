from typing import Optional, List
from src.modules.shop.repositories import (
    ShopProductRepository, ShopOrderRepository, ShopProductInventoryRepository,
    ShopInventoryMovementRepository
)
from src.modules.shop.models import (
    ShopProduct, ShopOrder, ShopProductInventory, ShopInventoryMovement
)
from src.modules.shop.schemas import (
    ShopProductSchema, ShopOrderSchema, ShopProductInventorySchema,
    ShopInventoryMovementSchema
)

class ShopProductService:
    def __init__(self, repo: ShopProductRepository):
        self.repo = repo

    def create_product(self, schema: ShopProductSchema) -> ShopProductSchema:
        product = ShopProduct(**schema.dict(exclude_unset=True))
        created = self.repo.create(product)
        return ShopProductSchema.from_orm(created)

    def get_product(self, product_id: int) -> Optional[ShopProductSchema]:
        product = self.repo.get_by_id(product_id)
        return ShopProductSchema.from_orm(product) if product else None

    def list_products(self, limit: int = 20) -> List[ShopProductSchema]:
        products = self.repo.list_all(limit)
        return [ShopProductSchema.from_orm(p) for p in products]

    def list_category_products(self, category_id: int, limit: int = 20) -> List[ShopProductSchema]:
        products = self.repo.list_by_category(category_id, limit)
        return [ShopProductSchema.from_orm(p) for p in products]

    def list_store_products(self, store_id: int, limit: int = 20) -> List[ShopProductSchema]:
        products = self.repo.list_by_store(store_id, limit)
        return [ShopProductSchema.from_orm(p) for p in products]

    def update_product(self, product_id: int, schema: ShopProductSchema) -> Optional[ShopProductSchema]:
        updated = self.repo.update(product_id, **schema.dict(exclude_unset=True))
        return ShopProductSchema.from_orm(updated) if updated else None

class ShopOrderService:
    def __init__(self, repo: ShopOrderRepository):
        self.repo = repo

    def create_order(self, schema: ShopOrderSchema) -> ShopOrderSchema:
        order = ShopOrder(**schema.dict(exclude_unset=True))
        created = self.repo.create(order)
        return ShopOrderSchema.from_orm(created)

    def get_order(self, order_id: int) -> Optional[ShopOrderSchema]:
        order = self.repo.get_by_id(order_id)
        return ShopOrderSchema.from_orm(order) if order else None

    def list_orders(self, limit: int = 20) -> List[ShopOrderSchema]:
        orders = self.repo.list_all(limit)
        return [ShopOrderSchema.from_orm(o) for o in orders]

    def list_user_orders(self, user_id: int, limit: int = 20) -> List[ShopOrderSchema]:
        orders = self.repo.list_by_user(user_id, limit)
        return [ShopOrderSchema.from_orm(o) for o in orders]

    def list_orders_by_status(self, status: str, limit: int = 20) -> List[ShopOrderSchema]:
        orders = self.repo.list_by_status(status, limit)
        return [ShopOrderSchema.from_orm(o) for o in orders]

    def update_order(self, order_id: int, schema: ShopOrderSchema) -> Optional[ShopOrderSchema]:
        updated = self.repo.update(order_id, **schema.dict(exclude_unset=True))
        return ShopOrderSchema.from_orm(updated) if updated else None

class ShopInventoryService:
    def __init__(self, repo: ShopProductInventoryRepository):
        self.repo = repo

    def create_inventory(self, schema: ShopProductInventorySchema) -> ShopProductInventorySchema:
        inventory = ShopProductInventory(**schema.dict(exclude_unset=True))
        created = self.repo.create(inventory)
        return ShopProductInventorySchema.from_orm(created)

    def get_inventory(self, inventory_id: int) -> Optional[ShopProductInventorySchema]:
        inventory = self.repo.get_by_id(inventory_id)
        return ShopProductInventorySchema.from_orm(inventory) if inventory else None

    def get_product_store_inventory(self, product_id: int, store_id: int) -> Optional[ShopProductInventorySchema]:
        inventory = self.repo.get_by_product_store(product_id, store_id)
        return ShopProductInventorySchema.from_orm(inventory) if inventory else None

    def list_store_inventory(self, store_id: int) -> List[ShopProductInventorySchema]:
        inventories = self.repo.list_by_store(store_id)
        return [ShopProductInventorySchema.from_orm(i) for i in inventories]

    def update_quantity(self, inventory_id: int, quantity: int) -> Optional[ShopProductInventorySchema]:
        updated = self.repo.update_quantity(inventory_id, quantity)
        return ShopProductInventorySchema.from_orm(updated) if updated else None

class ShopInventoryMovementService:
    def __init__(self, repo: ShopInventoryMovementRepository):
        self.repo = repo

    def record_movement(self, schema: ShopInventoryMovementSchema) -> ShopInventoryMovementSchema:
        movement = ShopInventoryMovement(**schema.dict(exclude_unset=True))
        created = self.repo.create(movement)
        return ShopInventoryMovementSchema.from_orm(created)

    def get_movement(self, movement_id: int) -> Optional[ShopInventoryMovementSchema]:
        movement = self.repo.get_by_id(movement_id)
        return ShopInventoryMovementSchema.from_orm(movement) if movement else None

    def list_product_movements(self, product_id: int, limit: int = 20) -> List[ShopInventoryMovementSchema]:
        movements = self.repo.list_by_product(product_id, limit)
        return [ShopInventoryMovementSchema.from_orm(m) for m in movements]

    def list_store_movements(self, store_id: int, limit: int = 20) -> List[ShopInventoryMovementSchema]:
        movements = self.repo.list_by_store(store_id, limit)
        return [ShopInventoryMovementSchema.from_orm(m) for m in movements]
