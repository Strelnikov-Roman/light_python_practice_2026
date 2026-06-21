import sys
import os

def scan_directory(current_path, level=0, stats=None, filter_term=None):
    if stats is None:
        stats = {"files": 0, "folders": 0, "size": 0, "matched_files": 0, "matched_size": 0}
        
    try:
        # Получаем список всех элементов в текущей директории
        items = os.listdir(current_path)
    except PermissionError:
        # Обработка папок, к которым у пользователя нет прав доступа
        print("  " * level + "├── [Доступ ограничен]")
        return stats

    for item in items:
        full_path = os.path.join(current_path, item)
        indent = "  " * level  # Вычисление отступа для отображения вложенности
        
        if os.path.isdir(full_path):
            print(f"{indent}└── [Папка] {item}")
            stats["folders"] += 1
            # Рекурсивно заходим внутрь обнаруженной папки, увеличивая уровень глубины и передавая параметры фильтрации
            scan_directory(full_path, level + 1, stats, filter_term)
        else:
            # Проверяем условия фильтрации для файлов
            is_matched = True
            if filter_term:
                if filter_term.startswith('.'):
                    # Вариант 1: Проверка по расширению файла
                    is_matched = item.endswith(filter_term)
                else:
                    # Вариант 2: Поиск подстроки в имени файла
                    is_matched = filter_term in item
            
            try:
                file_size = os.path.getsize(full_path)
            except FileNotFoundError:
                file_size = 0

            # Увеличиваем общую статистику для папки
            stats["files"] += 1
            stats["size"] += file_size

            # Выводим файл и учитываем его в отчете только при успешном прохождении фильтра
            if is_matched:
                print(f"{indent}├── [Файл] {item}")
                stats["matched_files"] += 1
                stats["matched_size"] += file_size
                
    return stats

def main():
    if len(sys.argv) < 2:
        print("Ошибка: Не указан путь к папке.")
        print("Использование: python src/main.py <путь_к_папке> [фильтр]")
        sys.exit(1)

    target_path = sys.argv[1]
    # Извлекаем необязательный параметр фильтра из второго аргумента командной строки
    filter_term = sys.argv[2] if len(sys.argv) > 2 else None

    print("Программа утилиты индексатора успешно запущена.")
    print(f"Целевая папка для анализа: {target_path}")
    if filter_term:
        print(f"Применен фильтр поиска: '{filter_term}'")
    print()

    if os.path.exists(target_path) and os.path.isdir(target_path):
        print(f"Структура директории {os.path.basename(os.path.abspath(target_path))}:")
        
        # Создаем стартовый словарь для накопления метрик
        directory_stats = {"files": 0, "folders": 0, "size": 0, "matched_files": 0, "matched_size": 0}
        scan_directory(target_path, 0, directory_stats, filter_term)
        
        # Вывод понятного структурированного отчета
        print("\n" + "=" * 40)
        print("ОТЧЕТ ПО РЕЗУЛЬТАТАМ ИНДЕКСАЦИИ")
        print("=" * 40)
        print(f"Всего вложенных папок: {directory_stats['folders']}")
        print(f"Всего файлов в папке:  {directory_stats['files']} ({directory_stats['size']} байт)")
        if filter_term:
            print(f"Соответствуют фильтру: {directory_stats['matched_files']} ({directory_stats['matched_size']} байт)")
        print("=" * 40)
    else:
        print("Ошибка: Указанный путь не существует или не является директорией.")

if __name__ == "__main__":
    main()