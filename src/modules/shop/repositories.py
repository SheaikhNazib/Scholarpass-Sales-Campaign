from typing import Optional, List, Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.shop.models import (
    ShopProduct, ShopOrder, ShopOrderDetail, ShopProductInventory,
    ShopInventoryMovement, ShopProductReview, ShopOrderReturn, ShopWishlist
)

class IShopProductRepository(Protocol):
    def create(self, product: ShopProduct) -> ShopProduct: ...
    def get_by_id(self, product_id: int) -> Optional[ShopProduct]: ...
    def list_all(self, limit: int = 20) -> List[ShopProduct]: ...
    def list_by_category(self, category_id: int, limit: int = 20) -> List[ShopProduct]: ...
    def list_by_store(self, store_id: int, limit: int = 20) -> List[ShopProduct]: ...
    def update(self, product_id: int, **kwargs) -> Optional[ShopProduct]: ...

class IShopOrderRepository(Protocol):
    def create(self, order: ShopOrder) -> ShopOrder: ...
    def get_by_id(self, order_id: int) -> Optional[ShopOrder]: ...
    def list_all(self, limit: int = 20) -> List[ShopOrder]: ...
    def list_by_user(self, user_id: int, limit: int = 20) -> List[ShopOrder]: ...
    def list_by_status(self, status: str, limit: int = 20) -> List[ShopOrder]: ...
    def update(self, order_id: int, **kwargs) -> Optional[ShopOrder]: ...

class IShopInventoryRepository(Protocol):
    def create(self, inventory: ShopProductInventory) -> ShopProductInventory: ...
    def get_by_id(self, inventory_id: int) -> Optional[ShopProductInventory]: ...
    def get_by_product_store(self, product_id: int, store_id: int) -> Optional[ShopProductInventory]: ...
    def list_by_store(self, store_id: int) -> List[ShopProductInventory]: ...
    def update_quantity(self, inventory_id: int, quantity: int) -> Optional[ShopProductInventory]: ...

class IShopInventoryMovementRepository(Protocol):
    def create(self, movement: ShopInventoryMovement) -> ShopInventoryMovement: ...
    def get_by_id(self, movement_id: int) -> Optional[ShopInventoryMovement]: ...
    def list_by_product(self, product_id: int, limit: int = 20) -> List[ShopInventoryMovement]: ...
    def list_by_store(self, store_id: int, limit: int = 20) -> List[ShopInventoryMovement]: ...

class ShopProductRepository(IShopProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: ShopProduct) -> ShopProduct:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Optional[ShopProduct]:
        return self.db.query(ShopProduct).filter(ShopProduct.id == product_id).first()

    def list_all(self, limit: int = 20) -> List[ShopProduct]:
        return self.db.query(ShopProduct).order_by(ShopProduct.created_at.desc()).limit(limit).all()

    def list_by_category(self, category_id: int, limit: int = 20) -> List[ShopProduct]:
        return self.db.query(ShopProduct).filter(
            ShopProduct.product_category_id == category_id
        ).order_by(ShopProduct.created_at.desc()).limit(limit).all()

    def list_by_store(self, store_id: int, limit: int = 20) -> List[ShopProduct]:
        return self.db.query(ShopProduct).filter(
            ShopProduct.store_id == store_id
        ).order_by(ShopProduct.created_at.desc()).limit(limit).all()

    def update(self, product_id: int, **kwargs) -> Optional[ShopProduct]:
        product = self.get_by_id(product_id)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product

class ShopOrderRepository(IShopOrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: ShopOrder) -> ShopOrder:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Optional[ShopOrder]:
        return self.db.query(ShopOrder).filter(ShopOrder.id == order_id).first()

    def list_all(self, limit: int = 20) -> List[ShopOrder]:
        return self.db.query(ShopOrder).order_by(ShopOrder.created_at.desc()).limit(limit).all()

    def list_by_user(self, user_id: int, limit: int = 20) -> List[ShopOrder]:
        return self.db.query(ShopOrder).filter(
            ShopOrder.user_id == user_id
        ).order_by(ShopOrder.created_at.desc()).limit(limit).all()

    def list_by_status(self, status: str, limit: int = 20) -> List[ShopOrder]:
        return self.db.query(ShopOrder).filter(
            ShopOrder.shop_order_status == status
        ).order_by(ShopOrder.created_at.desc()).limit(limit).all()

    def update(self, order_id: int, **kwargs) -> Optional[ShopOrder]:
        order = self.get_by_id(order_id)
        if order:
            for key, value in kwargs.items():
                setattr(order, key, value)
            self.db.commit()
            self.db.refresh(order)
        return order

class ShopProductInventoryRepository(IShopInventoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, inventory: ShopProductInventory) -> ShopProductInventory:
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def get_by_id(self, inventory_id: int) -> Optional[ShopProductInventory]:
        return self.db.query(ShopProductInventory).filter(ShopProductInventory.id == inventory_id).first()

    def get_by_product_store(self, product_id: int, store_id: int) -> Optional[ShopProductInventory]:
        return self.db.query(ShopProductInventory).filter(
            ShopProductInventory.shop_product_id == product_id,
            ShopProductInventory.shop_store_id == store_id
        ).first()

    def list_by_store(self, store_id: int) -> List[ShopProductInventory]:
        return self.db.query(ShopProductInventory).filter(
            ShopProductInventory.shop_store_id == store_id
        ).all()

    def update_quantity(self, inventory_id: int, quantity: int) -> Optional[ShopProductInventory]:
        inventory = self.get_by_id(inventory_id)
        if inventory:
            inventory.quantity = quantity
            self.db.commit()
            self.db.refresh(inventory)
        return inventory

class ShopInventoryMovementRepository(IShopInventoryMovementRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, movement: ShopInventoryMovement) -> ShopInventoryMovement:
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)
        return movement

    def get_by_id(self, movement_id: int) -> Optional[ShopInventoryMovement]:
        return self.db.query(ShopInventoryMovement).filter(ShopInventoryMovement.id == movement_id).first()

    def list_by_product(self, product_id: int, limit: int = 20) -> List[ShopInventoryMovement]:
        return self.db.query(ShopInventoryMovement).filter(
            ShopInventoryMovement.shop_product_id == product_id
        ).order_by(ShopInventoryMovement.created_at.desc()).limit(limit).all()

    def list_by_store(self, store_id: int, limit: int = 20) -> List[ShopInventoryMovement]:
        return self.db.query(ShopInventoryMovement).filter(
            ShopInventoryMovement.shop_store_id == store_id
        ).order_by(ShopInventoryMovement.created_at.desc()).limit(limit).all()
