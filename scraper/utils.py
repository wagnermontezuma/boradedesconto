"""
Funções utilitárias para o scraper do BoraDeDesconto.
"""
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


# Configuração de logging
def setup_logging():
    """
    Configura o sistema de logs com rotação de arquivos.
    """
    log_dir = Path.home() / ".local" / "share" / "deals-hub" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_path = log_dir / "scraper.log"
    
    # Remove handlers padrão
    logger.remove()
    
    # Adiciona handler para arquivo com rotação
    logger.add(
        log_path,
        rotation="1 MB",
        retention=5,
        compression="gz",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    # Adiciona handler para console em desenvolvimento
    if "uvicorn" in sys.modules:
        logger.add(sys.stderr, level="DEBUG", format="{time:HH:mm:ss} | {level} | {message}")
    
    return logger


# Lista de User-Agents para rotação
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
]

ACCEPT_LANGUAGES = ["pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7", "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3"]


def get_random_headers() -> Dict[str, str]:
    """
    Retorna headers HTTP aleatórios para evitar detecção de bots.
    """
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }


def calculate_discount(original_price: float, current_price: float) -> int:
    """
    Calcula o percentual de desconto.
    
    Args:
        original_price: Preço original do produto
        current_price: Preço atual do produto
        
    Returns:
        Percentual de desconto (0-100)
    """
    if original_price <= 0:
        return 0
    
    # Se o preço atual for zero, significa 100% de desconto
    if current_price <= 0:
        return 100
    
    discount = ((original_price - current_price) / original_price) * 100
    return max(0, min(100, int(discount)))


def format_price(price_str: str) -> float:
    """
    Converte string de preço para float.
    Remove R$, pontos e substitui vírgulas.
    """
    if not price_str:
        return 0.0
    
    # Remove caracteres não numéricos, exceto vírgula e ponto
    clean = ''.join(c for c in price_str if c.isdigit() or c in [',', '.'])
    
    # Substitui vírgula por ponto
    clean = clean.replace(',', '.')
    
    # Se tiver mais de um ponto, remove todos exceto o último
    if clean.count('.') > 1:
        parts = clean.split('.')
        last = parts.pop()
        clean = ''.join(parts).replace('.', '') + '.' + last
    
    try:
        return float(clean)
    except ValueError:
        return 0.0


# Decorator retry com backoff exponencial para APIs e requisições HTTP
retry_with_backoff = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    reraise=True
) 