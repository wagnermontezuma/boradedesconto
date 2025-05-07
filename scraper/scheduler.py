"""
Agendador de tarefas para o BoraDeDesconto usando APScheduler.
"""
import asyncio
import os
import signal
import sys
from pathlib import Path

# Adiciona o diretório parent ao PYTHONPATH
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from main import main as run_scraper
from utils import setup_logging


# Inicializa o logger
logger = setup_logging()


# Cria o scheduler
scheduler = AsyncIOScheduler(timezone="UTC")


async def run_task(merchant=None):
    """
    Wrapper para executar o scraper e capturar exceções.
    """
    try:
        logger.info(f"Iniciando tarefa agendada: {merchant or 'todos'}")
        await run_scraper(merchant)
        logger.info(f"Tarefa agendada finalizada: {merchant or 'todos'}")
    except Exception as e:
        logger.error(f"Erro na execução agendada: {str(e)}")


def handle_exit(signum, frame):
    """
    Manipulador de sinal para desligar o scheduler.
    """
    logger.info(f"Recebido sinal {signum}. Encerrando scheduler...")
    scheduler.shutdown(wait=False)
    sys.exit(0)


async def main():
    """
    Configura e inicia o scheduler.
    """
    logger.info("Iniciando scheduler do BoraDeDesconto")
    
    # Configura handlers para sinais de terminação
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    # Adiciona as tarefas
    scheduler.add_job(
        run_task,
        trigger=IntervalTrigger(hours=1),
        id="amazon",
        kwargs={"merchant": "amazon"},
        next_run_time=None  # Não executa imediatamente
    )
    
    # TODO: Adicionar outros merchants
    
    # Adiciona uma tarefa para executar todos os merchants
    scheduler.add_job(
        run_task,
        trigger=IntervalTrigger(hours=6),
        id="all_merchants",
        next_run_time=None  # Não executa imediatamente
    )
    
    # Inicia o scheduler
    scheduler.start()
    
    logger.info("Scheduler iniciado. Pressione CTRL+C para sair.")
    
    # Executa uma vez ao iniciar
    await run_task()
    
    # Loop infinito para manter o programa rodando
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    # Executa o scheduler diretamente
    asyncio.run(main()) 