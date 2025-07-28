import logging
from datetime import datetime
from typing import Dict


from utils import (
    fetch_currency_rates,
    fetch_stock_prices,
    filter_month_to_date,
    get_greeting,
    get_top_transactions,
    load_transactions,
    load_user_settings,
    summarize_cards,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def index(date_str: str) -> Dict:
    """
    Главная страница: возвращает JSON-ответ по входной дате в формате YYYY-MM-DD HH:MM:SS
    """
    logger.info("Запуск функции index с датой %s", date_str)

    settings = load_user_settings("user_settings.json")
    df = load_transactions("data/operations.xlsx")

    target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    filtered_df = filter_month_to_date(df, target_date)

    result = {
        "greeting": get_greeting(target_date),
        "cards": summarize_cards(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": fetch_currency_rates(settings["user_currencies"]),
        "stock_prices": fetch_stock_prices(settings["user_stocks"]),
    }

    logger.info("Формирование JSON-ответа завершено")
    return result
