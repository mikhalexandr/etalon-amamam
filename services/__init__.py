from services.default.api.v1.endpoints import router as default_router
from services.objects.api.v1.endpoints import router as objects_router
from services.reports.api.v1.endpoints import router as reports_router


# Инициализация роутеров
def init_routers(app):
    app.include_router(default_router)
    app.include_router(objects_router)
    app.include_router(reports_router)
