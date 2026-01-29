from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.modules.user.routes import router as user_router
from src.modules.access.routes import router as access_router
from src.modules.notification.routes import router as notification_router
from src.modules.master.routes import router as master_router
from src.modules.connect.routes import router as connect_router
from src.modules.tpm.routes import router as tpm_router
from src.modules.crm.routes import router as crm_router
from src.modules.sales.routes import router as sales_router
from src.modules.contract.routes import router as contract_router
from src.modules.shop.routes import router as shop_router

settings = get_settings()
app = FastAPI(
    title="ScholarPASS Backend",
    description="Hexagonal Architecture API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(access_router)
app.include_router(notification_router)
app.include_router(master_router)
app.include_router(connect_router)
app.include_router(tpm_router)
app.include_router(crm_router)
app.include_router(sales_router)
app.include_router(contract_router)
app.include_router(shop_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
