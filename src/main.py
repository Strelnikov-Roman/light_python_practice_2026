import sys
import os

def scan_directory(current_path, level=0):
    try:
        # Получаем список всех элементов в текущей директории
        items = os.listdir(current_path)
    except PermissionError:
        # Обработка папок, к которым у пользователя нет прав доступа
        print("  " * level + "├── [Доступ ограничен]")
        return

    for item in items:
        full_path = os.path.join(current_path, item)
        indent = "  " * level  # Вычисление отступа для отображения вложенности
        
        if os.path.isdir(full_path):
            print(f"{indent}└── [Папка] {item}")
            # Рекурсивно заходим внутрь обнаруженной папки, увеличивая уровень глубины
            scan_directory(full_path, level + 1)
        else:
            print(f"{indent}├── [Файл] {item}")

def main():
    if len(sys.argv) < 2:
        print("Ошибка: Не указан путь к папке.")
        print("Использование: python src/main.py <путь_к_папке>")
        sys.exit(1)

    target_path = sys.argv[1]
    print("Программа утилиты индексатора успешно запущена.")
    print(f"Целевая папка для анализа: {target_path}\n")

    if os.path.exists(target_path) and os.path.isdir(target_path):
        print(f"Структура директории {os.path.basename(os.path.abspath(target_path))}:")
        scan_directory(target_path)
    else:
        print("Ошибка: Указанный путь не существует или не является директорией.")

if __name__ == "__main__":
    main()