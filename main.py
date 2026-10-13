
"""
Модуль: Менеджер нотаток
Опис: Консольний застосунок для обліку нотаток з категоріями та пошуком
Автор: Сироткін Антон
"""

import json
import os

FILE_NAME = "notes.json"


def load_notes_from_file() -> list:
    """Завантажує список нотаток із JSON-файлу."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file_handle:
            notes = json.load(file_handle)

        if not isinstance(notes, list):
            print("Помилка: файл має неправильний формат.\n")
            return []

        # Перевіряємо структуру кожної нотатки
        required_fields = {"id", "title", "category", "content"}

        for note in notes:
            if not isinstance(note, dict) or not required_fields.issubset(note):
                print("Помилка: файл містить некоректні нотатки.\n")
                return []

            if (
                not isinstance(note["id"], int)
                or not isinstance(note["title"], str)
                or not isinstance(note["category"], str)
                or not isinstance(note["content"], str)
            ):
                print("Помилка: файл містить некоректні дані.\n")
                return []

        return notes

    except json.JSONDecodeError:
        print("Помилка читання JSON-файлу. Перевірте його вміст.\n")
        return []
    except OSError as error:
        print(f"Помилка відкриття файлу: {error}\n")
        return []


def save_notes_to_file(notes_list: list) -> bool:
    """Зберігає список нотаток у JSON-файл."""
    temp_file = FILE_NAME + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file_handle:
            json.dump(
                notes_list,
                file_handle,
                ensure_ascii=False,
                indent=4
            )

        # Замінюємо основний файл лише після успішного запису
        os.replace(temp_file, FILE_NAME)
        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Помилка збереження нотаток: {error}")

        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except OSError:
            pass

        return False


def create_new_note(notes_list: list) -> None:
    """Створює нову нотатку та додає її до списку."""
    title = input("Введіть заголовок нотатки: ").strip()
    category = input(
        "Введіть категорію (напр. Робота, Навчання): "
    ).strip()
    content = input("Введіть текст нотатки: ").strip()

    if not title or not content:
        print("Помилка: заголовок і текст не можуть бути порожніми!\n")
        return

    new_id = max(
        (note["id"] for note in notes_list),
        default=0
    ) + 1

    new_note = {
        "id": new_id,
        "title": title,
        "category": category or "Загальна",
        "content": content
    }

    notes_list.append(new_note)

    if save_notes_to_file(notes_list):
        print("Нотатку успішно збережено!\n")
    else:
        notes_list.pop()
        print("Не вдалося зберегти нотатку. Спробуйте ще раз.\n")


def display_notes_list(notes_list: list) -> None:
    """Виводить на екран повний список нотаток."""
    if not notes_list:
        print("Список нотаток порожній.\n")
        return

    print("\n--- СПИСОК НОТАТОК ---")

    for note in notes_list:
        print(
            f"ID: {note['id']} | "
            f"Категорія: [{note['category']}] | "
            f"Заголовок: {note['title']}"
        )
        print(f"Текст: {note['content']}")
        print("-" * 40)

    print()


def search_notes_by_keyword(notes_list: list) -> None:
    """Шукає нотатки за ключовим словом у заголовку, категорії або тексті."""
    keyword = input(
        "Введіть слово або категорію для пошуку: "
    ).strip().casefold()

    if not keyword:
        print("Пошуковий запит не може бути порожнім.\n")
        return

    filtered_notes = [
        note for note in notes_list
        if keyword in note["category"].casefold()
        or keyword in note["title"].casefold()
        or keyword in note["content"].casefold()
    ]

    if not filtered_notes:
        print("Нічого не знайдено за вашим запитом.\n")
        return

    print(
        f"\n--- РЕЗУЛЬТАТИ ПОШУКУ "
        f"(Знайдено: {len(filtered_notes)}) ---"
    )

    for note in filtered_notes:
        print(
            f"ID: {note['id']} | "
            f"[{note['category']}] {note['title']}"
        )
        print(f"Текст: {note['content']}")
        print("-" * 40)

    print()


def print_menu() -> None:
    """Виводить головне меню програми."""
    print("=== МЕНЕДЖЕР НОТАТОК ===")
    print("1. Переглянути нотатки")
    print("2. Додати нотатку")
    print("3. Пошук нотаток")
    print("4. Вихід")


def main() -> None:
    """Головна точка входу в програму."""
    notes = load_notes_from_file()

    while True:
        print_menu()
        choice = input("Оберіть дію (1-4): ").strip()

        if choice == "1":
            display_notes_list(notes)

        elif choice == "2":
            create_new_note(notes)

        elif choice == "3":
            search_notes_by_keyword(notes)

        elif choice == "4":
            print("До побачення!")
            break

        else:
            print("Невірний вибір. Будь ласка, оберіть від 1 до 4.\n")


if __name__ == "__main__":
    main()
