from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time

class ShopProductSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=1024)
    short_description: Optional[str] = None
    primary_image: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    public_url: Optional[str] = None
    seo_keywords: Optional[str] = None
    regular_price: Optional[float] = None
    sale_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
    call_for_price: bool = False
    unit_price: Optional[float] = None
    tax_exempt: bool = False
    stock_quantity: Optional[int] = None
    display_stock_quantity: bool = False
    draft_or_published: Optional[str] = None
    package_product: bool = False
    internal_notes: Optional[str] = None
    save_as_template: bool = False
    product_or_service: bool = False
    verified: bool = False
    product_snapshot_json: Optional[Dict[str, Any]] = None
    product_snapshot_json_url: Optional[str] = None
    snapshot_generated_at: Optional[datetime] = None
    rating_score: Optional[int] = None
    product_category_id: Optional[int] = None
    master_currency_id: Optional[int] = None
    store_id: Optional[int] = None
    product_manager_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopOrderSchema(BaseModel):
    id: Optional[int] = None
    order_number: str = Field(..., min_length=1, max_length=256)
    order_date: Optional[datetime] = None
    service_or_product: bool = True
    delivery_or_pickup: bool = False
    payment_completed: bool = False
    full_name: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    customer_notes: Optional[str] = None
    total_discount_amount: Optional[float] = None
    service_charge: Optional[float] = None
    number_of_items: Optional[int] = None
    sub_total_excluded_tax: Optional[float] = None
    total_tax_amount: Optional[float] = None
    discount_code_id: Optional[int] = None
    zone_id: Optional[int] = None
    master_country_id: Optional[int] = None
    shop_order_status_type_id: Optional[int] = None
    shop_order_channel_type_id: Optional[int] = None
    user_id: Optional[int] = None
    shop_order_status: str = "Processing"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopOrderDetailSchema(BaseModel):
    id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    discount_percentage_by_item: Optional[float] = None
    discount_amount_by_item: Optional[float] = None
    total_amount_by_item: Optional[float] = None
    shop_order_id: int
    shop_product_id: int
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopProductInventorySchema(BaseModel):
    id: Optional[int] = None
    shop_product_id: int
    shop_store_id: int
    quantity: int = 0
    location_aisle: Optional[str] = None
    location_shelf: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopInventoryMovementSchema(BaseModel):
    id: Optional[int] = None
    shop_product_id: int
    shop_store_id: int
    shop_product_inventory_id: Optional[int] = None
    quantity_change: int
    movement_type: str
    movement_status: str = "Completed"
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    performed_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopProductReviewSchema(BaseModel):
    id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    review_title: Optional[str] = None
    review_content: Optional[str] = None
    is_verified_purchase: bool = False
    published: bool = True
    shop_product_id: int
    shop_store_id: int
    shop_order_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopOrderReturnSchema(BaseModel):
    id: Optional[int] = None
    return_reason: str = Field(..., min_length=1, max_length=256)
    return_status: str = "Requested"
    admin_notes: Optional[str] = None
    customer_notes: Optional[str] = None
    refund_amount: Optional[float] = None
    shop_order_id: int
    shop_order_detail_id: Optional[int] = None
    user_id: Optional[int] = None
    processed_by_user_id: Optional[int] = None
    shop_store_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShopWishlistSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    shop_product_id: int
    added_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
