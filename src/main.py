import sys
import os

def print_help():
    """Вывод короткой инструкции по запуску утилиты."""
    print("=" * 50)
    print("УТИЛИТА ИНДЕКСАЦИИ ПАПОК — СПРАВКА ПО ЗАПУСКУ")
    print("=" * 50)
    print("Использование:")
    print("  python src/main.py <путь_к_папке> [фильтр]")
    print("\nПараметры:")
    print("  <путь_к_папке>  Путь к директории, которую нужно проанализировать.")
    print("  [фильтр]        (Опционально) Фильтр для поиска файлов.")
    print("                  • Если начинается с точки (например, .txt),")
    print("                    ищет строго по расширению.")
    print("                  • Если без точки (например, meta),")
    print("                    ищет совпадение слова в имени файла.")
    print("\nПримеры запуска:")
    print("  python src/main.py .")
    print("  python src/main.py C:/Users/User/Documents .py")
    print("  python src/main.py ./src main")
    print("=" * 50)

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
                    # Вариант 1: Строгая проверка по расширению файла
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
    # 1. Проверка на запрос справки или отсутствие аргументов
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    target_path = sys.argv[1]
    filter_term = sys.argv[2] if len(sys.argv) > 2 else None

    # 2. МНОГОУРОВНЕВАЯ ВАЛИДАЦИЯ ВХОДНЫХ ДАННЫХ
    # Проверяем существование пути
    if not os.path.exists(target_path):
        print(f"Ошибка валидации: Указанный путь '{target_path}' не существует.")
        sys.exit(1)
        
    # Проверяем, является ли путь директорией
    if not os.path.isdir(target_path):
        print(f"Ошибка валидации: Путь '{target_path}' существует, но не является папкой.")
        sys.exit(1)
        
    # Проверяем права на чтение папки
    if not os.access(target_path, os.R_OK):
        print(f"Ошибка валидации: Нет прав на чтение папки '{target_path}'.")
        sys.exit(1)

    # Если все проверки пройдены, запускаем основную логику
    print("Программа утилиты индексатора успешно запущена.")
    print(f"Целевая папка для анализа: {os.path.abspath(target_path)}")
    if filter_term:
        print(f"Применен фильтр поиска: '{filter_term}'")
    print()

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

if __name__ == "__main__":
    main()