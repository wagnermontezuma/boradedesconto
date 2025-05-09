"""
API REST do BoraDeDesconto implementada com FastAPI.

Esta API fornece endpoints para consultar ofertas coletadas em tempo quase-real 
de diversos e-commerces, com suporte a filtros, paginação e estatísticas de cliques.
"""
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

import models

# Definir modelos Pydantic para as respostas para melhor documentação
class OfferResponse(BaseModel):
    """Modelo de resposta para uma oferta"""
    id: int = Field(..., description="ID único da oferta no sistema")
    merchant: str = Field(..., description="Nome do e-commerce (amazon, mercadolivre, etc)")
    external_id: str = Field(..., description="ID externo da oferta no e-commerce de origem")
    title: str = Field(..., description="Título do produto")
    url: str = Field(..., description="URL para a página do produto")
    price: float = Field(..., description="Preço atual do produto em reais")
    discount_pct: int = Field(..., description="Percentual de desconto (0-100)")
    ts: datetime = Field(..., description="Timestamp da coleta da oferta")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "merchant": "amazon",
                "external_id": "B08X7JX9MB",
                "title": "Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto",
                "url": "https://www.amazon.com.br/dp/B08X7JX9MB",
                "price": 1899.99,
                "discount_pct": 25,
                "ts": "2023-06-01T10:00:00Z"
            }
        }

class PaginatedOfferResponse(BaseModel):
    """Modelo de resposta paginada para ofertas"""
    data: List[OfferResponse] = Field(..., description="Lista de ofertas")
    count: int = Field(..., description="Número total de ofertas na resposta")
    
    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "id": 1,
                        "merchant": "amazon",
                        "external_id": "B08X7JX9MB",
                        "title": "Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto",
                        "url": "https://www.amazon.com.br/dp/B08X7JX9MB",
                        "price": 1899.99,
                        "discount_pct": 25,
                        "ts": "2023-06-01T10:00:00Z"
                    }
                ],
                "count": 1
            }
        }

class ClickStatsResponse(BaseModel):
    """Modelo de resposta para estatísticas de cliques"""
    offer_id: int = Field(..., description="ID da oferta")
    merchant: str = Field(..., description="Nome do e-commerce")
    title: str = Field(..., description="Título do produto")
    click_count: int = Field(..., description="Número de cliques")
    
    class Config:
        schema_extra = {
            "example": {
                "offer_id": 1,
                "merchant": "amazon",
                "title": "Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto",
                "click_count": 42
            }
        }

class ClickStatsListResponse(BaseModel):
    """Modelo de resposta para lista de estatísticas de cliques"""
    data: List[ClickStatsResponse] = Field(..., description="Lista de estatísticas de cliques")
    days: int = Field(..., description="Período em dias da análise")
    
    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "offer_id": 1,
                        "merchant": "amazon",
                        "title": "Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto",
                        "click_count": 42
                    }
                ],
                "days": 30
            }
        }

app = FastAPI(
    title="BoraDeDesconto API",
    description="""API para consulta de ofertas em tempo quase-real dos principais e-commerces.
    
Esta API permite consultar ofertas coletadas por scrapers, filtrar por loja e porcentagem de desconto,
obter detalhes de ofertas específicas, registrar cliques e consultar estatísticas de cliques.

Os dados são atualizados periodicamente pelos scrapers automatizados que coletam informações da Amazon e Mercado Livre.
""",
    version="1.0.0",
    openapi_tags=[
        {"name": "ofertas", "description": "Operações relacionadas a ofertas"},
        {"name": "estatísticas", "description": "Operações relacionadas a estatísticas de cliques"},
        {"name": "sistema", "description": "Operações relacionadas ao sistema"}
    ],
    contact={
        "name": "BoraDeDesconto",
        "url": "https://github.com/username/boradedesconto",
        "email": "suporte@boradedesconto.com.br"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configura CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint principal para listar ofertas
@app.get(
    "/offers", 
    response_model=PaginatedOfferResponse,
    tags=["ofertas"],
    summary="Lista ofertas com filtros",
    responses={
        200: {"description": "Lista de ofertas retornada com sucesso"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def list_offers(
    merchant: str = Query(None, description="Filtrar por loja (amazon, mercadolivre etc)"),
    min_discount: int = Query(0, ge=0, le=100, description="Desconto mínimo em porcentagem (0-100)"),
    limit: int = Query(20, ge=1, le=100, description="Limite de resultados (1-100)"),
    offset: int = Query(0, ge=0, description="Deslocamento para paginação")
):
    """
    Lista ofertas com suporte a filtros e paginação.
    
    - **merchant**: Filtrar por loja específica (amazon, mercadolivre etc)
    - **min_discount**: Desconto mínimo em porcentagem (0-100)
    - **limit**: Limite de resultados por página (1-100)
    - **offset**: Deslocamento para paginação
    
    Exemplo de requisição: `/offers?merchant=amazon&min_discount=20`
    """
    offers = await models.get_offers(
        merchant=merchant,
        min_discount=min_discount,
        limit=limit,
        offset=offset
    )
    
    return {"data": offers, "count": len(offers)}


# Endpoint para detalhes de uma oferta específica
@app.get(
    "/offers/{offer_id}", 
    response_model=OfferResponse,
    tags=["ofertas"],
    summary="Obter detalhes de uma oferta específica",
    responses={
        200: {"description": "Detalhes da oferta retornados com sucesso"},
        404: {"description": "Oferta não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_offer(offer_id: int):
    """
    Retorna detalhes de uma oferta específica pelo ID.
    
    - **offer_id**: ID único da oferta no sistema
    
    Exemplo de requisição: `/offers/42`
    """
    offer = await models.get_offer_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Oferta não encontrada")
    
    return offer


# Endpoint para redirecionamento com registro de clique
@app.get(
    "/go/{offer_id}",
    tags=["ofertas"],
    summary="Redirecionar para oferta com registro de clique",
    responses={
        307: {"description": "Redirecionamento temporário para a URL da oferta"},
        404: {"description": "Oferta não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def redirect_offer(offer_id: int, request: Request):
    """
    Registra o clique e redireciona para a URL da oferta.
    
    Este endpoint registra o clique do usuário na oferta e redireciona para a página do produto no e-commerce.
    Para links da Amazon, o ID de afiliado é automaticamente adicionado se não estiver presente.
    
    - **offer_id**: ID único da oferta no sistema
    
    Exemplo de uso: `<a href="/go/42">Ver oferta</a>`
    """
    offer = await models.get_offer_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Oferta não encontrada")
    
    # Registra o clique na oferta
    user_agent = request.headers.get("user-agent", "")
    referer = request.headers.get("referer", "")
    
    await models.register_offer_click(
        offer_id=offer_id,
        user_agent=user_agent,
        referer=referer
    )
    
    # Obtém a URL para redirecionamento
    redirect_url = offer["url"]
    
    # Adiciona o ID de afiliado para links da Amazon
    if "amazon.com.br" in redirect_url and "tag=" not in redirect_url:
        separator = "&" if "?" in redirect_url else "?"
        redirect_url = f"{redirect_url}{separator}tag=wagnermontezu-20"
    
    return RedirectResponse(url=redirect_url, status_code=307)


# Endpoint para consultar estatísticas de cliques
@app.get(
    "/stats/clicks",
    response_model=ClickStatsListResponse,
    tags=["estatísticas"],
    summary="Obter estatísticas de cliques",
    responses={
        200: {"description": "Estatísticas de cliques retornadas com sucesso"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_click_stats(
    offer_id: int = Query(None, description="ID opcional da oferta para filtrar"),
    days: int = Query(30, ge=1, le=365, description="Número de dias para análise (1-365)")
):
    """
    Retorna estatísticas de cliques nas ofertas.
    
    Permite visualizar quantos cliques cada oferta recebeu durante o período especificado.
    
    - **offer_id**: ID opcional da oferta para filtrar estatísticas para uma oferta específica
    - **days**: Número de dias para a análise retrospectiva (1-365)
    
    Exemplo de requisição: `/stats/clicks?days=7` ou `/stats/clicks?offer_id=42&days=30`
    """
    stats = await models.get_offer_clicks_stats(
        offer_id=offer_id,
        days=days
    )
    
    return {"data": stats, "days": days}


# Rota de verificação de saúde
@app.get(
    "/health",
    tags=["sistema"],
    summary="Verificar saúde da API",
    response_model=Dict[str, Any],
    responses={
        200: {"description": "API está funcionando corretamente"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def health_check():
    """
    Verifica se a API está funcionando corretamente.
    
    Útil para monitoramento e verificação de disponibilidade da API.
    
    Exemplo de requisição: `/health`
    """
    return {"status": "ok", "version": app.version}


# Inicializa o banco de dados na startup
@app.on_event("startup")
async def startup_db_client():
    """
    Garante que o banco está inicializado na startup da API.
    """
    await models.init_db()


# Documentação personalizada
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Endpoint personalizado para a documentação Swagger.
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentação",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


# Personalização do schema OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True) 