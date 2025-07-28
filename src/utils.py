import json
import logging
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_user_settings(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_transactions(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
    return df


def filter_month_to_date(df: pd.DataFrame, target_date: datetime) -> pd.DataFrame:
    start_of_month = target_date.replace(day=1)
    return df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= target_date)]


def get_greeting(dt: datetime) -> str:
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def summarize_cards(df: pd.DataFrame) -> List[Dict]:
    cards = []
    for card in df["Номер карты"].dropna().unique():
        card_df = df[df["Номер карты"] == card]
        total = round(card_df["Сумма платежа"].sum(), 2)
        cashback = round(total * 0.01, 2)
        cards.append({"last_digits": str(card), "total_spent": total, "cashback": cashback})
    return cards


def get_top_transactions(df: pd.DataFrame) -> List[Dict]:
    top = df.sort_values(by="Сумма платежа", ascending=False).head(5)
    return [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for _, row in top.iterrows()
    ]


def fetch_currency_rates(codes: List[str]) -> List[Dict]:
    rates = []
    for code in codes:
        try:
            resp = requests.get(f"https://api.exchangerate.host/latest?base=RUB&symbols={code}")
            resp.raise_for_status()
            rate = resp.json()["rates"].get(code)
            rates.append({"currency": code, "rate": round(rate, 2)})
        except Exception as e:
            logger.error("Ошибка получения курса %s: %s", code, e)
    return rates


def fetch_stock_prices(stocks: List[str]) -> List[Dict]:
    return [{"stock": stock, "price": round(100 + hash(stock) % 1000 / 10, 2)} for stock in stocks]


def search_transactions(query: str, transactions: List[Dict]) -> List[Dict]:
    return [
        tx
        for tx in transactions
        if query.lower() in str(tx.get("Описание", "")).lower()
        or query.lower() in str(tx.get("Категория", "")).lower()
    ]
