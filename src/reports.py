import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в каждый из дней недели за последние три месяца от указанной даты.
    """
    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    logger.info("Формируем отчет по тратам по дням недели с %s по %s", start_date.date(), end_date.date())

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    df["weekday"] = df["Дата операции"].dt.day_name()
    result = df.groupby("weekday")["Сумма платежа"].mean().round(2).reset_index()
    result.columns = ["weekday", "avg_spending"]
    return result
