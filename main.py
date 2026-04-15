"""
GMUD - Sistema de Gestão de Manutenção de Equipamentos
Calendário para gerenciar manutenções de máquinas críticas em produção
"""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from app.config import get_settings
from app.database import init_db
from app.routers.gmuds import router as gmuds_router

# Configurações
settings = get_settings()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar banco de dados
init_db()

# Criar app FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de gestão de calendário de manutenção de equipamentos",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Rotas
app.include_router(gmuds_router)


@app.get("/health", tags=["health"])
def health_check():
    """Health check da aplicação"""
    return {"status": "healthy"}


@app.get("/", tags=["root"], include_in_schema=False)
async def root():
    """Serve a página principal do dashboard"""
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(path=index_path, media_type="text/html")


@app.get("/favicon.ico", tags=["static"], include_in_schema=False)
async def favicon():
    """Favicon da aplicação"""
    favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(path=favicon_path)
    # Se não existir, retornar 204 No Content
    return Response(status_code=204)


@app.get("/logo.png.png", tags=["static"], include_in_schema=False)
async def logo():
    """Logo da aplicação"""
    logo_path = os.path.join(os.path.dirname(__file__), "static", "images", "logo.png")
    if os.path.exists(logo_path):
        return FileResponse(path=logo_path, media_type="image/png")
    # Se não existir, retornar 204 No Content
    return Response(status_code=204)


@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 {settings.APP_NAME} iniciado - v{settings.APP_VERSION}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"🛑 {settings.APP_NAME} finalizado")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
