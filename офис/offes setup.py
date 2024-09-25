import os
import time

def rename_file(file_path, new_extension):
    base = os.path.splitext(file_path)[0]
    new_file_path = base + new_extension
    os.rename(file_path, new_file_path)
    return new_file_path

def monitor_file(file_path):
    while True:
        if os.path.exists(file_path):
            # Переименовываем файл в .zip
            zip_file_path = rename_file(file_path, '.zip')
            print(f"File renamed to: {zip_file_path}")
            
            # Ждем, пока файл не будет закрыт
            while os.path.exists(zip_file_path):
                time.sleep(1)
            
            # Переименовываем файл обратно в .watsys
            rename_file(zip_file_path, '.watprog')
            print(f"File renamed back to: {file_path}")
        
        # Ждем некоторое время перед следующей проверкой
        time.sleep(1)

if __name__ == "__main__":
    file_path = "ofess.prog"  # Укажите путь к вашему файлу
    monitor_file(file_path)
