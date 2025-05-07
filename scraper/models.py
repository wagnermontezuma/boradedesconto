"""
Modelos para o scraper do BoraDeDesconto.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class Offer:
    """
    Classe para representar uma oferta coletada pelos scrapers.
    """
    def __init__(self, 
                 title: str, 
                 price: float, 
                 url: str, 
                 merchant: str, 
                 external_id: str,
                 discount_pct: int = 0,
                 original_price: Optional[float] = None):
        """
        Inicializa uma nova oferta.
        
        Args:
            title: Título do produto
            price: Preço atual do produto
            url: URL da oferta
            merchant: Nome do e-commerce (amazon, mercadolivre, etc)
            external_id: ID externo do produto no site de origem
            discount_pct: Percentual de desconto (0-100)
            original_price: Preço original antes do desconto (opcional)
        """
        self.title = title
        self.price = price
        self.url = url
        self.merchant = merchant
        self.external_id = external_id
        self.discount_pct = discount_pct
        self.original_price = original_price if original_price is not None else price
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """
        Converte a oferta para um dicionário.
        """
        return {
            "title": self.title,
            "price": self.price,
            "original_price": self.original_price,
            "url": self.url,
            "merchant": self.merchant,
            "external_id": self.external_id,
            "discount_pct": self.discount_pct,
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        """
        Converte a oferta para JSON.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __eq__(self, other):
        """
        Compara duas ofertas pela igualdade.
        Duas ofertas são iguais se tiverem o mesmo merchant e external_id.
        """
        if not isinstance(other, Offer):
            return False
        return (self.merchant == other.merchant and 
                self.external_id == other.external_id)
    
    def __repr__(self):
        return f"Offer({self.merchant}, {self.external_id}, {self.price}, {self.discount_pct}%)"


def save_offers(offers: List[Offer], source: str, output_dir: str = None) -> str:
    """
    Salva uma lista de ofertas em um arquivo JSON.
    
    Args:
        offers: Lista de ofertas para salvar
        source: Nome da fonte (ex: amazon, mercadolivre)
        output_dir: Diretório de saída (opcional)
        
    Returns:
        Caminho do arquivo salvo
    """
    # Define o diretório de saída
    if not output_dir:
        output_dir = Path.home() / "ofertas"
    
    # Garante que o diretório existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Gera o nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{source}_{timestamp}.json"
    output_path = Path(output_dir) / filename
    
    # Converte todas as ofertas para dicionários
    offers_data = [offer.to_dict() for offer in offers]
    
    # Salva o arquivo JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(offers_data, f, ensure_ascii=False, indent=2)
    
    return str(output_path) 