import pandas as pd
import pytest

from src.reports import spending_by_weekday


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Дата операции": "2024-05-01", "Сумма платежа": 100},  # Wednesday
            {"Дата операция": "2024-05-02", "Сумма платежа": 200},  # Thursday
            {"Дата операция": "2024-05-03", "Сумма платежа": 300},  # Friday
            {"Дата операция": "2024-05-04", "Сумма платежа": 400},  # Saturday
            {"Дата операция": "2024-05-05", "Сумма платежа": 500},  # Sunday
            {"Дата операция": "2024-05-06", "Сумма платежа": 600},  # Monday
            {"Дата операция": "2024-05-07", "Сумма платежа": 700},  # Tuesday
        ]
    )


def test_spending_by_weekday_structure(sample_transactions: pd.DataFrame) -> None:
    result = spending_by_weekday(sample_transactions, date="2024-05-07")
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {"weekday", "avg_spending"}
    assert not result.empty


def test_spending_by_weekday_values(sample_transactions: pd.DataFrame) -> None:
    result = spending_by_weekday(sample_transactions, date="2024-05-07")
    weekdays = result["weekday"].tolist()
    assert "Monday" in weekdays
    assert result[result["weekday"] == "Monday"]["avg_spending"].iloc[0] == 600.0
