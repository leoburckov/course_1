import logging
from datetime import datetime

from services import simple_search
from utils import load_transactions
from views import index

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main() -> None:
    print("Добро пожаловать в систему анализа транзакций!")
    print("1. Главная страница (сводка по дате)")
    print("2. Простой поиск по описанию/категории")

    choice = input("Выберите действие (1/2): ").strip()

    if choice == "1":
        date_input = input("Введите дату и время (в формате YYYY-MM-DD HH:MM:SS): ").strip()
        try:
            datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
            result = index(date_input)
            print("\nJSON-результат:\n")
            for k, v in result.items():
                print(f"{k}: {v}")
        except ValueError:
            print("Неверный формат даты.")

    elif choice == "2":
        transactions = load_transactions("data/operations.xlsx")
        query = input("Введите строку для поиска: ").strip()
        result = simple_search(query, transactions.to_dict(orient="records"))
        print("\nНайденные транзакции:\n")
        for tx in result["results"]:
            print(tx)

    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    main()
