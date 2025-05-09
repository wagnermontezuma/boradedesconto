"""Script para inserir ofertas manualmente no banco de dados."""
import asyncio
import datetime
import sqlite3
import os
from pathlib import Path

# Caminho para o banco de dados
DB_PATH = Path(__file__).parent / "deals.db"

# Dados de ofertas da Amazon para inserir
AMAZON_OFFERS = [
    {
        "merchant": "amazon",
        "external_id": "B09V3YW11L",
        "title": "Echo Dot 5ª Geração | Smart speaker com Alexa | Cor Preta",
        "url": "https://www.amazon.com.br/dp/B09V3YW11L?tag=wagnermontezu-20",
        "price": 299.99,
        "discount_pct": 40,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B091G4T5HB",
        "title": "Smartphone Samsung Galaxy S22 5G 128GB 8GB RAM Preto",
        "url": "https://www.amazon.com.br/dp/B091G4T5HB?tag=wagnermontezu-20",
        "price": 2599.99,
        "discount_pct": 35,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B08LNBW179",
        "title": "Notebook Dell Inspiron 15 3000 Intel Core i5-1135G7 8GB 256GB SSD Windows 11",
        "url": "https://www.amazon.com.br/dp/B08LNBW179?tag=wagnermontezu-20",
        "price": 3199.99,
        "discount_pct": 25,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B07VGRWSF7",
        "title": "Smart TV Samsung 50\" Crystal UHD 4K AU7700",
        "url": "https://www.amazon.com.br/dp/B07VGRWSF7?tag=wagnermontezu-20",
        "price": 2199.99,
        "discount_pct": 30,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B08S3L9CBP",
        "title": "Headset Sem Fio JBL Quantum 600 Gamer",
        "url": "https://www.amazon.com.br/dp/B08S3L9CBP?tag=wagnermontezu-20",
        "price": 499.99,
        "discount_pct": 45,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B07ZDK7YSF",
        "title": "Console PlayStation 5 Sony",
        "url": "https://www.amazon.com.br/dp/B07ZDK7YSF?tag=wagnermontezu-20",
        "price": 3899.99,
        "discount_pct": 15,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B084DWCZY6",
        "title": "Apple AirPods Pro com Estojo de Recarga MagSafe",
        "url": "https://www.amazon.com.br/dp/B084DWCZY6?tag=wagnermontezu-20",
        "price": 1599.99,
        "discount_pct": 20,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B07PDHSPYD",
        "title": "Smartwatch Samsung Galaxy Watch 4 40mm Preto",
        "url": "https://www.amazon.com.br/dp/B07PDHSPYD?tag=wagnermontezu-20",
        "price": 999.99,
        "discount_pct": 50,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B07NJPXFVY",
        "title": "Kindle 11ª Geração com Iluminação Embutida",
        "url": "https://www.amazon.com.br/dp/B07NJPXFVY?tag=wagnermontezu-20",
        "price": 349.99,
        "discount_pct": 38,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "amazon",
        "external_id": "B07X37DT9M",
        "title": "Tablet Samsung Galaxy Tab S7 128GB WiFi",
        "url": "https://www.amazon.com.br/dp/B07X37DT9M?tag=wagnermontezu-20",
        "price": 2799.99,
        "discount_pct": 22,
        "ts": datetime.datetime.utcnow().isoformat()
    }
]

# Dados de ofertas do Mercado Livre para inserir
ML_OFFERS = [
    {
        "merchant": "mercadolivre",
        "external_id": "MLB2163772914",
        "title": "Smart TV Samsung 50\" Crystal UHD 4K BU8000 2022",
        "url": "https://www.mercadolivre.com.br/p/MLB2163772914",
        "price": 2399.99,
        "discount_pct": 40,
        "ts": datetime.datetime.utcnow().isoformat()
    },
    {
        "merchant": "mercadolivre",
        "external_id": "MLB2789425378",
        "title": "Notebook Dell Inspiron 15 3000 Intel Core i5 8GB RAM 256GB SSD",
        "url": "https://www.mercadolivre.com.br/p/MLB2789425378",
        "price": 3299.99,
        "discount_pct": 15,
        "ts": datetime.datetime.utcnow().isoformat()
    }
]

def init_db():
    """Inicializa o banco de dados SQLite."""
    print(f"Verificando banco em: {DB_PATH}")
    
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Cria a conexão com o banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ativa o modo WAL para melhor concorrência
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Cria a tabela de ofertas se não existir
    cursor.execute("""
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
    cursor.execute("""
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_discount ON offers(discount_pct DESC);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON offers(ts DESC);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_offer_clicks ON offer_clicks(offer_id);")
    
    conn.commit()
    conn.close()
    
    print("Banco inicializado com sucesso.")

def insert_offers(offers):
    """Insere ou atualiza ofertas no banco."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for offer in offers:
        try:
            # Tenta inserir primeiro
            cursor.execute("""
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
                offer["merchant"],
                offer["external_id"],
                offer["title"],
                offer["url"],
                offer["price"],
                offer["discount_pct"],
                offer["ts"]
            ))
            
            print(f"Oferta inserida/atualizada: {offer['title'][:30]}...")
        except Exception as e:
            print(f"Erro ao inserir oferta: {str(e)}")
    
    conn.commit()
    conn.close()
    print(f"Total: {len(offers)} ofertas inseridas/atualizadas.")

def main():
    """Função principal"""
    print("Iniciando inserção manual de ofertas...")
    
    # Inicializa o banco
    init_db()
    
    # Insere ofertas da Amazon
    print("\nInserindo ofertas da Amazon...")
    insert_offers(AMAZON_OFFERS)
    
    # Insere ofertas do Mercado Livre
    print("\nInserindo ofertas do Mercado Livre...")
    insert_offers(ML_OFFERS)
    
    print("\n✅ Processo concluído!")

if __name__ == "__main__":
    main() 