import logging
from typing import Dict, List

from utils import search_transactions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def simple_search(query: str, transactions: List[Dict]) -> Dict:
    """
    Простой поиск: возвращает JSON с транзакциями, содержащими query в описании или категории
    """
    logger.info("Выполняется простой поиск по запросу: '%s'", query)
    result = search_transactions(query, transactions)
    logger.info("Найдено %d совпадений", len(result))
    return {"results": result}
