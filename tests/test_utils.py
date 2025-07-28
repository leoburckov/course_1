import json
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (
    fetch_currency_rates,
    fetch_stock_prices,
    filter_month_to_date,
    get_greeting,
    get_top_transactions,
    load_transactions,
    load_user_settings,
    search_transactions,
    summarize_cards
)

# -------- Тесты --------


def test_load_user_settings() -> None:
    mock_data = {"name": "Test"}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = load_user_settings("fake_path.json")
        assert result == mock_data


def test_load_transactions(tmp_path: Path) -> None:
    file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"Дата операции": ["2024-01-01"], "Сумма платежа": [100]})
    df.to_excel(file, index=False)

    result = load_transactions(str(file))
    assert isinstance(result, pd.DataFrame)
    assert "Дата операции" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["Дата операция"])


def test_filter_month_to_date() -> None:
    df = pd.DataFrame(
        {"Дата операция": pd.to_datetime(["2024-07-01", "2024-07-10", "2024-06-30"]), "Сумма платежа": [100, 200, 300]}
    )
    target_date = datetime(2024, 7, 14)
    filtered = filter_month_to_date(df, target_date)
    assert len(filtered) == 2


@pytest.mark.parametrize(
    "hour,expected",
    [
        (6, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (1, "Доброй ночи"),
    ],
)
def test_get_greeting(hour: int, expected: int) -> None:
    dt = datetime(2024, 7, 14, hour)
    assert get_greeting(dt) == expected


def test_summarize_cards() -> None:
    df = pd.DataFrame({"Номер карты": ["1234", "1234", "5678"], "Сумма платежа": [100.0, 150.0, 200.0]})
    result = summarize_cards(df)
    assert len(result) == 2
    assert result[0]["cashback"] == round(result[0]["total_spent"] * 0.01, 2)


def test_get_top_transactions() -> None:
    df = pd.DataFrame(
        {
            "Дата операция": pd.to_datetime(["2024-07-01", "2024-07-02", "2024-07-03"]),
            "Сумма платежа": [100.0, 300.0, 200.0],
            "Категория": ["еда", "техника", "одежда"],
            "Описание": ["завтрак", "ноутбук", "футболка"],
        }
    )
    top = get_top_transactions(df)
    assert len(top) == 3
    assert top[0]["amount"] == 300.0


@patch("main.requests.get")
def test_fetch_currency_rates(mock_get: Mock) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"USD": 0.011}}

    result = fetch_currency_rates(["USD"])
    assert result == [{"currency": "USD", "rate": 0.01}]


def test_fetch_stock_prices() -> None:
    stocks = ["AAPL", "GOOGL"]
    result = fetch_stock_prices(stocks)
    assert len(result) == 2
    assert all("stock" in r and "price" in r for r in result)


def test_search_transactions() -> None:
    txs = [
        {"Описание": "магазин", "Категория": "еда"},
        {"Описание": "такси", "Категория": "транспорт"},
        {"Описание": "кино", "Категория": "развлечения"},
    ]
    found = search_transactions("такси", txs)
    assert len(found) == 1
    assert found[0]["Описание"] == "такси"
