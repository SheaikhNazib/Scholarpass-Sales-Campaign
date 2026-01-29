from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.shop.services import (
    ShopProductService, ShopOrderService, ShopInventoryService,
    ShopInventoryMovementService
)
from src.modules.shop.repositories import (
    ShopProductRepository, ShopOrderRepository, ShopProductInventoryRepository,
    ShopInventoryMovementRepository
)
from src.modules.shop.schemas import (
    ShopProductSchema, ShopOrderSchema, ShopProductInventorySchema,
    ShopInventoryMovementSchema
)

router = APIRouter(prefix="/api/shop", tags=["shop"])

def get_product_service(db: Session = Depends(get_db)) -> ShopProductService:
    return ShopProductService(ShopProductRepository(db))

def get_order_service(db: Session = Depends(get_db)) -> ShopOrderService:
    return ShopOrderService(ShopOrderRepository(db))

def get_inventory_service(db: Session = Depends(get_db)) -> ShopInventoryService:
    return ShopInventoryService(ShopProductInventoryRepository(db))

def get_movement_service(db: Session = Depends(get_db)) -> ShopInventoryMovementService:
    return ShopInventoryMovementService(ShopInventoryMovementRepository(db))

@router.post("/products", response_model=ShopProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(schema: ShopProductSchema, service: ShopProductService = Depends(get_product_service)):
    return service.create_product(schema)

@router.get("/products/{product_id}", response_model=ShopProductSchema)
def get_product(product_id: int, service: ShopProductService = Depends(get_product_service)):
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.get("/products", response_model=list[ShopProductSchema])
def list_products(limit: int = 20, service: ShopProductService = Depends(get_product_service)):
    return service.list_products(limit)

@router.get("/products/category/{category_id}", response_model=list[ShopProductSchema])
def list_category_products(category_id: int, limit: int = 20, service: ShopProductService = Depends(get_product_service)):
    return service.list_category_products(category_id, limit)

@router.get("/products/store/{store_id}", response_model=list[ShopProductSchema])
def list_store_products(store_id: int, limit: int = 20, service: ShopProductService = Depends(get_product_service)):
    return service.list_store_products(store_id, limit)

@router.put("/products/{product_id}", response_model=ShopProductSchema)
def update_product(product_id: int, schema: ShopProductSchema, service: ShopProductService = Depends(get_product_service)):
    updated = service.update_product(product_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated

@router.post("/orders", response_model=ShopOrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(schema: ShopOrderSchema, service: ShopOrderService = Depends(get_order_service)):
    return service.create_order(schema)

@router.get("/orders/{order_id}", response_model=ShopOrderSchema)
def get_order(order_id: int, service: ShopOrderService = Depends(get_order_service)):
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.get("/orders", response_model=list[ShopOrderSchema])
def list_orders(limit: int = 20, service: ShopOrderService = Depends(get_order_service)):
    return service.list_orders(limit)

@router.get("/orders/user/{user_id}", response_model=list[ShopOrderSchema])
def list_user_orders(user_id: int, limit: int = 20, service: ShopOrderService = Depends(get_order_service)):
    return service.list_user_orders(user_id, limit)

@router.get("/orders/status/{status}", response_model=list[ShopOrderSchema])
def list_orders_by_status(status: str, limit: int = 20, service: ShopOrderService = Depends(get_order_service)):
    return service.list_orders_by_status(status, limit)

@router.put("/orders/{order_id}", response_model=ShopOrderSchema)
def update_order(order_id: int, schema: ShopOrderSchema, service: ShopOrderService = Depends(get_order_service)):
    updated = service.update_order(order_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated

@router.post("/inventory", response_model=ShopProductInventorySchema, status_code=status.HTTP_201_CREATED)
def create_inventory(schema: ShopProductInventorySchema, service: ShopInventoryService = Depends(get_inventory_service)):
    return service.create_inventory(schema)

@router.get("/inventory/{inventory_id}", response_model=ShopProductInventorySchema)
def get_inventory(inventory_id: int, service: ShopInventoryService = Depends(get_inventory_service)):
    inventory = service.get_inventory(inventory_id)
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return inventory

@router.get("/inventory/product/{product_id}/store/{store_id}", response_model=ShopProductInventorySchema)
def get_product_store_inventory(product_id: int, store_id: int, service: ShopInventoryService = Depends(get_inventory_service)):
    inventory = service.get_product_store_inventory(product_id, store_id)
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return inventory

@router.get("/inventory/store/{store_id}", response_model=list[ShopProductInventorySchema])
def list_store_inventory(store_id: int, service: ShopInventoryService = Depends(get_inventory_service)):
    return service.list_store_inventory(store_id)

@router.patch("/inventory/{inventory_id}/quantity", response_model=ShopProductInventorySchema)
def update_inventory_quantity(inventory_id: int, quantity: int, service: ShopInventoryService = Depends(get_inventory_service)):
    updated = service.update_quantity(inventory_id, quantity)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return updated

@router.post("/inventory-movements", response_model=ShopInventoryMovementSchema, status_code=status.HTTP_201_CREATED)
def record_movement(schema: ShopInventoryMovementSchema, service: ShopInventoryMovementService = Depends(get_movement_service)):
    return service.record_movement(schema)

@router.get("/inventory-movements/{movement_id}", response_model=ShopInventoryMovementSchema)
def get_movement(movement_id: int, service: ShopInventoryMovementService = Depends(get_movement_service)):
    movement = service.get_movement(movement_id)
    if not movement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
    return movement

@router.get("/inventory-movements/product/{product_id}", response_model=list[ShopInventoryMovementSchema])
def list_product_movements(product_id: int, limit: int = 20, service: ShopInventoryMovementService = Depends(get_movement_service)):
    return service.list_product_movements(product_id, limit)

@router.get("/inventory-movements/store/{store_id}", response_model=list[ShopInventoryMovementSchema])
def list_store_movements(store_id: int, limit: int = 20, service: ShopInventoryMovementService = Depends(get_movement_service)):
    return service.list_store_movements(store_id, limit)
