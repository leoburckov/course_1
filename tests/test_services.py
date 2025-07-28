import pytest

from src.services import simple_search


@pytest.fixture
def sample_transactions() -> list[dict[str, str] | dict[str, str] | dict[str, str] | dict[str, str]]:
    return [
        {"Описание": "Покупка кофе в Starbucks", "Категория": "Кафе"},
        {"Описание": "Перевод другу", "Категория": "Переводы"},
        {"Описание": "Оплата интернета", "Категория": "Связь"},
        {"Описание": "Еда в Макдоналдс", "Категория": "Фастфуд"},
    ]


def test_simple_search_description(sample_transactions: list[dict[str, str]]) -> None:
    result = simple_search("кофе", sample_transactions)
    assert len(result["results"]) == 1
    assert result["results"][0]["Категория"] == "Кафе"


def test_simple_search_category(sample_transactions: list[dict[str, str]]) -> None:
    result = simple_search("фастфуд", sample_transactions)
    assert len(result["results"]) == 1
    assert result["results"][0]["Описание"] == "Еда в Макдоналдс"


def test_simple_search_no_results(sample_transactions: list[dict[str, str]]) -> None:
    result = simple_search("автомойка", sample_transactions)
    assert result["results"] == []


def test_simple_search_case_insensitive(sample_transactions: list[dict[str, str]]) -> None:
    result = simple_search("СТАРБАКС", sample_transactions)
    assert len(result["results"]) == 1
