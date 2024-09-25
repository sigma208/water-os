import json

def load_wop_file(file_path):
    """
    Загружает содержимое .wop файла.
    
    :param file_path: Путь к .wop файлу.
    :return: Словарь с данными из файла или None в случае ошибки.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            app_data = json.load(file)
        return app_data
    except Exception as e:
        print(f"Error loading .wop file: {e}")
        return None

def save_wop_file(file_path, app_data):
    """
    Сохраняет данные в .wop файл.
    
    :param file_path: Путь к .wop файлу.
    :param app_data: Словарь с данными для сохранения.
    :return: True, если сохранение прошло успешно, иначе False.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(app_data, file)
        return True
    except Exception as e:
        print(f"Error saving .wop file: {e}")
        return False

def load_watercash_file(file_path):
    """
    Загружает содержимое .watercash файла.
    
    :param file_path: Путь к .watercash файлу.
    :return: Строка с содержимым файла или None в случае ошибки.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error loading .watercash file: {e}")
        return None

def save_watercash_file(file_path, content):
    """
    Сохраняет данные в .watercash файл.
    
    :param file_path: Путь к .watercash файлу.
    :param content: Строка с данными для сохранения.
    :return: True, если сохранение прошло успешно, иначе False.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error saving .watercash file: {e}")
        return False
