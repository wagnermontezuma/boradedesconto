"""Script para inserir dados de amostra no banco de dados."""
import asyncio
import datetime
from models import init_db, Offer, upsert_offer

# Dados de amostra
SAMPLE_OFFERS = [
    {
        "merchant": "amazon",
        "external_id": "B08X7JX9MB",
        "title": "Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto",
        "url": "https://www.amazon.com.br/dp/B08X7JX9MB",
        "price": 1899.99,
        "discount_pct": 25,
        "ts": datetime.datetime.utcnow()
    },
    {
        "merchant": "amazon",
        "external_id": "B09V3YW11L",
        "title": "Aspirador de Pó Robô Xiaomi Robot Vacuum-Mop 2",
        "url": "https://www.amazon.com.br/dp/B09V3YW11L",
        "price": 1499.99,
        "discount_pct": 35,
        "ts": datetime.datetime.utcnow()
    },
    {
        "merchant": "mercadolivre",
        "external_id": "MLB2163772914",
        "title": "Smart TV Samsung 50\" Crystal UHD 4K BU8000 2022",
        "url": "https://www.mercadolivre.com.br/p/MLB2163772914",
        "price": 2399.99,
        "discount_pct": 40,
        "ts": datetime.datetime.utcnow()
    },
    {
        "merchant": "mercadolivre",
        "external_id": "MLB2789425378",
        "title": "Notebook Dell Inspiron 15 3000 Intel Core i5 8GB RAM 256GB SSD",
        "url": "https://www.mercadolivre.com.br/p/MLB2789425378",
        "price": 3299.99,
        "discount_pct": 15,
        "ts": datetime.datetime.utcnow()
    },
    {
        "merchant": "aliexpress",
        "external_id": "1005004563781452",
        "title": "Fones de ouvido sem fio TWS Bluetooth 5.3",
        "url": "https://www.aliexpress.com/item/1005004563781452.html",
        "price": 89.99,
        "discount_pct": 60,
        "ts": datetime.datetime.utcnow()
    },
    {
        "merchant": "amazon",
        "external_id": "B08JCRL4T5",
        "title": "Echo Dot 4ª Geração Smart Speaker com Alexa",
        "url": "https://www.amazon.com.br/dp/B08JCRL4T5",
        "price": 299.99,
        "discount_pct": 45,
        "ts": datetime.datetime.utcnow()
    }
]

async def insert_sample_data():
    """Insere dados de amostra no banco de dados."""
    # Inicializa o banco se ainda não estiver inicializado
    await init_db()
    
    print("Inserindo dados de amostra no banco...")
    
    # Insere cada oferta
    for offer_data in SAMPLE_OFFERS:
        offer = Offer(**offer_data)
        await upsert_offer(offer)
        print(f"Oferta inserida: {offer.title}")
    
    print("Dados de amostra inseridos com sucesso!")

if __name__ == "__main__":
    asyncio.run(insert_sample_data()) 