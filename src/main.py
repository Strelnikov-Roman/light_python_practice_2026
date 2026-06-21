import sys
import os

def scan_directory(current_path, level=0, stats=None):
    if stats is None:
        stats = {"files": 0, "folders": 0, "size": 0}
        
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
            # Рекурсивно заходим внутрь обнаруженной папки, увеличивая уровень глубины и передавая словарь со статистикой
            scan_directory(full_path, level + 1, stats)
        else:
            print(f"{indent}├── [Файл] {item}")
            stats["files"] += 1
            try:
                # Суммируем размер файла в байтах
                stats["size"] += os.path.getsize(full_path)
            except FileNotFoundError:
                pass
                
    return stats

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
        
        # Создаем стартовый словарь для накопления метрик
        directory_stats = {"files": 0, "folders": 0, "size": 0}
        scan_directory(target_path, 0, directory_stats)
        
        # Вывод понятного структурированного отчета
        print("\n" + "=" * 40)
        print("ОТЧЕТ ПО РЕЗУЛЬТАТАМ ИНДЕКСАЦИИ")
        print("=" * 40)
        print(f"Всего вложенных папок: {directory_stats['folders']}")
        print(f"Всего найденных файлов: {directory_stats['files']}")
        print(f"Общий размер данных:   {directory_stats['size']} байт")
        print("=" * 40)
    else:
        print("Ошибка: Указанный путь не существует или не является директорией.")

if __name__ == "__main__":
    main()