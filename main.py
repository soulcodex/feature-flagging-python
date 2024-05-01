from fastapi import FastAPI
from fastapi.responses import JSONResponse

from shared.infrastructure.flag_router import flags_router
from shoe.infrastructure.shoes_router import shoes_router


def create_app() -> FastAPI:
    app = FastAPI(
        version='1.0.0',
        title='Shoes API',
        description='Shoes API Documentation - Python Coruña 2024',
        docs_url=None,
        redoc_url='/docs'
    )

    @app.get('/', status_code=200, include_in_schema=False)
    async def index() -> JSONResponse:
        return JSONResponse({'name': 'Shoes Shop - Feature Flagging v1'})

    app.include_router(prefix='/v1/shoes', router=shoes_router)
    app.include_router(prefix='/feature-flags', router=flags_router)

    return app
