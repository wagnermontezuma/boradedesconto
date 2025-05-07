"""
API REST do BoraDeDesconto implementada com FastAPI.
"""
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import models

app = FastAPI(
    title="BoraDeDesconto API",
    description="API para consulta de ofertas em tempo quase-real",
    version="0.1.0"
)

# Configura CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint principal para listar ofertas
@app.get("/offers")
async def list_offers(
    merchant: str = None,
    min_discount: int = Query(0, ge=0, le=100),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Lista ofertas com filtros opcionais:
    - merchant: Filtrar por loja (Amazon, Mercado Livre etc)
    - min_discount: Desconto mínimo em porcentagem (0-100)
    - limit: Limite de resultados (1-100)
    - offset: Deslocamento para paginação
    """
    offers = await models.get_offers(
        merchant=merchant,
        min_discount=min_discount,
        limit=limit,
        offset=offset
    )
    
    return {"data": offers, "count": len(offers)}


# Endpoint para detalhes de uma oferta específica
@app.get("/offers/{offer_id}")
async def get_offer(offer_id: int):
    """
    Retorna detalhes de uma oferta específica pelo ID.
    """
    offer = await models.get_offer_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Oferta não encontrada")
    
    return offer


# Endpoint para redirecionamento com registro de clique
@app.get("/go/{offer_id}")
async def redirect_offer(offer_id: int, request: Request):
    """
    Registra o clique e redireciona para a URL da oferta.
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
    
    return RedirectResponse(url=offer["url"], status_code=307)


# Endpoint para consultar estatísticas de cliques
@app.get("/stats/clicks")
async def get_click_stats(
    offer_id: int = None,
    days: int = Query(30, ge=1, le=365)
):
    """
    Retorna estatísticas de cliques nas ofertas:
    - offer_id: ID opcional da oferta para filtrar
    - days: Número de dias para análise (1-365)
    """
    stats = await models.get_offer_clicks_stats(
        offer_id=offer_id,
        days=days
    )
    
    return {"data": stats, "days": days}


# Rota de verificação de saúde
@app.get("/health")
async def health_check():
    """
    Verifica se a API está funcionando.
    """
    return {"status": "ok", "version": app.version}


# Inicializa o banco de dados na startup
@app.on_event("startup")
async def startup_db_client():
    """
    Garante que o banco está inicializado na startup da API.
    """
    await models.init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True) 