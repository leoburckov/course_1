from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from src.views import index


@pytest.fixture
def mock_user_settings(tmp_path: Path, monkeypatch: Any) -> None:
    settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "MSFT"]}
    path = tmp_path / "user_settings.json"
    path.write_text(str(settings).replace("'", '"'))
    monkeypatch.setattr(
        "builtins.open", lambda f, *a, **kw: path.open(*a, **kw) if "user_settings" in f else open(f, *a, **kw)
    )


@pytest.fixture
def sample_excel(tmp_path: Path) -> Path:
    import pandas as pd

    df = pd.DataFrame(
        [
            {
                "Дата операции": "2024-07-01",
                "Номер карты": 1234,
                "Сумма платежа": 100.0,
                "Категория": "Кафе",
                "Описание": "кофе",
            },
            {
                "Дата операции": "2024-07-02",
                "Номер карты": 1234,
                "Сумма платежа": 200.0,
                "Категория": "Переводы",
                "Описание": "другу",
            },
            {
                "Дата операции": "2024-07-03",
                "Номер карты": 5678,
                "Сумма платежа": 300.0,
                "Категория": "Супермаркеты",
                "Описание": "еда",
            },
        ]
    )
    file_path = tmp_path / "operations.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


def test_index_json_response(monkeypatch: Any, sample_excel: None, mock_user_settings: Any) -> None:
    monkeypatch.setattr("src.views.pd.read_excel", lambda _: pd.read_excel(sample_excel))
    result = index("2024-07-03 12:00:00")

    assert "greeting" in result
    assert "cards" in result
    assert isinstance(result["cards"], list)
    assert len(result["cards"]) > 0

    assert "top_transactions" in result
    assert isinstance(result["top_transactions"], list)

    assert "currency_rates" in result
    assert "stock_prices" in result
