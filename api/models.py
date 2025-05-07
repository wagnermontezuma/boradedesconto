"""
Modelos de dados e inicialização do banco SQLite para o BoraDeDesconto.
"""
import datetime
import os
import sqlite3
from pathlib import Path

import aiosqlite
from pydantic import BaseModel, Field


class Offer(BaseModel):
    """Modelo para representar uma oferta."""
    id: int = None
    merchant: str
    external_id: str
    title: str
    url: str
    price: float
    discount_pct: int
    ts: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class OfferClick(BaseModel):
    """Modelo para representar um clique em uma oferta."""
    id: int = None
    offer_id: int
    user_agent: str = None
    referer: str = None
    ts: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


async def get_db_path() -> Path:
    """Retorna o caminho para o banco de dados."""
    db_path = Path(__file__).parent / "deals.db"
    return db_path


async def init_db():
    """
    Inicializa o banco de dados SQLite em modo WAL.
    """
    db_path = await get_db_path()
    
    # Verifica se o diretório existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    async with aiosqlite.connect(db_path) as db:
        # Ativa o modo WAL para melhor concorrência
        await db.execute("PRAGMA journal_mode=WAL;")
        
        # Cria a tabela de ofertas se não existir
        await db.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant TEXT NOT NULL,
            external_id TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            price REAL NOT NULL,
            discount_pct INTEGER NOT NULL,
            ts DATETIME NOT NULL,
            UNIQUE(merchant, external_id)
        );
        """)
        
        # Cria a tabela de cliques se não existir
        await db.execute("""
        CREATE TABLE IF NOT EXISTS offer_clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id INTEGER NOT NULL,
            user_agent TEXT,
            referer TEXT,
            ts DATETIME NOT NULL,
            FOREIGN KEY (offer_id) REFERENCES offers (id)
        );
        """)
        
        # Cria índices para consultas comuns
        await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_discount ON offers(discount_pct DESC);
        """)
        
        await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp ON offers(ts DESC);
        """)
        
        await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_offer_clicks ON offer_clicks(offer_id);
        """)
        
        await db.commit()
    
    print(f"Banco inicializado em {db_path}")


# Função para inserir ou atualizar ofertas
async def upsert_offer(offer: Offer):
    """
    Insere ou atualiza uma oferta no banco.
    Usa a restrição UNIQUE para garantir não duplicação.
    """
    db_path = await get_db_path()
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
        INSERT INTO offers (merchant, external_id, title, url, price, discount_pct, ts)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(merchant, external_id) 
        DO UPDATE SET 
            title=excluded.title,
            url=excluded.url,
            price=excluded.price,
            discount_pct=excluded.discount_pct,
            ts=excluded.ts
        """, (
            offer.merchant,
            offer.external_id,
            offer.title,
            offer.url,
            offer.price,
            offer.discount_pct,
            offer.ts.isoformat()
        ))
        
        await db.commit()


# Função para registrar clique na oferta
async def register_offer_click(offer_id: int, user_agent: str = None, referer: str = None):
    """
    Registra um clique em uma oferta.
    """
    db_path = await get_db_path()
    
    click = OfferClick(
        offer_id=offer_id,
        user_agent=user_agent,
        referer=referer
    )
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
        INSERT INTO offer_clicks (offer_id, user_agent, referer, ts)
        VALUES (?, ?, ?, ?)
        """, (
            click.offer_id,
            click.user_agent,
            click.referer,
            click.ts.isoformat()
        ))
        
        await db.commit()
    
    return click


# Função para obter estatísticas de cliques por oferta
async def get_offer_clicks_stats(offer_id: int = None, days: int = 30):
    """
    Retorna estatísticas de cliques para uma oferta específica ou todas.
    """
    db_path = await get_db_path()
    
    # Calcula a data limite para a consulta
    date_limit = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).isoformat()
    
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        
        if offer_id:
            # Estatísticas para uma oferta específica
            cursor = await db.execute("""
            SELECT COUNT(*) as click_count, offer_id, o.merchant, o.title
            FROM offer_clicks c
            JOIN offers o ON c.offer_id = o.id
            WHERE c.offer_id = ? AND c.ts > ?
            GROUP BY offer_id
            """, (offer_id, date_limit))
        else:
            # Estatísticas para todas as ofertas
            cursor = await db.execute("""
            SELECT COUNT(*) as click_count, offer_id, o.merchant, o.title
            FROM offer_clicks c
            JOIN offers o ON c.offer_id = o.id
            WHERE c.ts > ?
            GROUP BY offer_id
            ORDER BY click_count DESC
            LIMIT 100
            """, (date_limit,))
            
        rows = await cursor.fetchall()
        
        return [dict(row) for row in rows]


# Função para consultar ofertas com filtros
async def get_offers(merchant=None, min_discount=0, limit=20, offset=0):
    """
    Consulta ofertas com filtros opcionais.
    """
    db_path = await get_db_path()
    
    query = "SELECT * FROM offers WHERE discount_pct >= ?"
    params = [min_discount]
    
    if merchant:
        query += " AND merchant = ?"
        params.append(merchant)
    
    query += " ORDER BY ts DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        return [dict(row) for row in rows]


# Função para obter oferta por ID
async def get_offer_by_id(offer_id: int):
    """
    Retorna uma oferta pelo ID.
    """
    db_path = await get_db_path()
    
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        cursor = await db.execute("SELECT * FROM offers WHERE id = ?", (offer_id,))
        row = await cursor.fetchone()
        
        return dict(row) if row else None


if __name__ == "__main__":
    # Quando executado diretamente, inicializa o banco
    import asyncio
    asyncio.run(init_db()) 