import subprocess
import sys
import pygame
import os
import platform
import datetime
import requests
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, simpledialog
import wop_file_utils  # Импортируем наш модуль
import tempfile

required_libraries = ['pygame', 'requests', 'ttkbootstrap']

def install_libraries():
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_libraries()

pygame.init()
pygame.mixer.init()

# Проверка успешности загрузки файла
sound_file = '1.mp3'
if os.path.exists(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
else:
    print(f"Error: File {sound_file} not found.")

click_sound = pygame.mixer.Sound('click.wav')
error_sound = pygame.mixer.Sound('error.wav')
success_sound = pygame.mixer.Sound('success.wav')

def play_sound(sound):
    sound.play()

def log_action(action):
    with open("log.watercash", "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")

def save_wop_app():
    app_name = simpledialog.askstring("Save .wop App", "Enter the name of the application:")
    if app_name:
        app_code = simpledialog.askstring("Save .wop App", "Enter the code for the application:")
        if app_code:
            if wop_file_utils.save_wop_file(f"{app_name}.wop", {"name": app_name, "code": app_code}):
                play_sound(success_sound)
                log_action(f"Save .wop App: Application saved successfully ({app_name}.wop)")
                messagebox.showinfo("Save .wop App", f"Application '{app_name}' saved successfully.")

def load_wop_app():
    file_path = filedialog.askopenfilename(title="Select .wop file", filetypes=[("WOP files", "*.wop")])
    if file_path:
        app_data = wop_file_utils.load_wop_file(file_path)
        if app_data:
            play_sound(success_sound)
            log_action(f"Load .wop App: Application loaded successfully ({file_path})")
            messagebox.showinfo("Load .wop App", f"Application '{app_data['name']}' loaded successfully.\n\nCode:\n{app_data['code']}")

def open_watercash_file():
    file_path = filedialog.askopenfilename(title="Select .watercash file", filetypes=[("Watercash files", "*.watercash")])
    if file_path:
        content = wop_file_utils.load_watercash_file(file_path)
        if content:
            play_sound(success_sound)
            log_action(f"Open .watercash File: File opened successfully ({file_path})")
            messagebox.showinfo("Open .watercash File", f"Content of '{file_path}':\n\n{content}")

def compile_python_to_wop():
    file_path = filedialog.askopenfilename(title="Select Python file", filetypes=[("Python files", "*.py")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            app_name = os.path.splitext(os.path.basename(file_path))[0]
            if wop_file_utils.save_wop_file(f"{app_name}.wop", {"name": app_name, "code": code}):
                play_sound(success_sound)
                log_action(f"Compile Python to .wop: Compilation successful ({app_name}.wop)")
                messagebox.showinfo("Compile Python to .wop", f"Python file '{file_path}' compiled to '{app_name}.wop' successfully.")
        except Exception as e:
            play_sound(error_sound)
            log_action(f"Compile Python to .wop error: {e}")
            messagebox.showerror("Error", f"Failed to compile Python file: {e}")

def run_wop_app():
    file_path = filedialog.askopenfilename(title="Select .wop file", filetypes=[("WOP files", "*.wop")])
    if file_path:
        app_data = wop_file_utils.load_wop_file(file_path)
        if app_data:
            try:
                # Создаем временный файл для выполнения кода
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                    temp_file.write(app_data['code'])
                    temp_file_path = temp_file.name
                
                # Выполняем код
                result = subprocess.run([sys.executable, temp_file_path], capture_output=True, text=True)
                play_sound(success_sound)
                log_action(f"Run .wop App: Application executed successfully ({file_path})")
                messagebox.showinfo("Run .wop App", f"Output:\n{result.stdout}")
            except Exception as e:
                play_sound(error_sound)
                log_action(f"Run .wop App error: {e}")
                messagebox.showerror("Error", f"Failed to run .wop application: {e}")
            finally:
                # Удаляем временный файл
                os.remove(temp_file_path)

def help():
    play_sound(click_sound)
    log_action("Help command executed")
    messagebox.showinfo("Help", "help=command\ncalc=calculator\ncls=clear screen\ndate=show current date and time\nweather=show weather for a city\nguess=play guess the number game\nlist_files=list files in current directory\nchange_theme=change theme\nchange_font_size=change font size\ninstall_exe=install .exe file\ninstall_apk=install .apk file\nrun_code=run code in various programming languages\noffice_apps=open built-in office applications\nlog_actions=log actions to .watercash file\nsave_wop_app=save .wop application\nload_wop_app=load .wop application\nopen_watercash_file=open .watercash file\ncompile_python_to_wop=compile Python file to .wop\nrun_wop_app=run .wop application")

def calculator():
    expression = simpledialog.askstring("Calculator", "Введите выражение для вычисления (например, 2 + 2):")
    try:
        result = eval(expression)
        play_sound(success_sound)
        log_action(f"Calculator result: {result}")
        messagebox.showinfo("Calculator", f"Результат: {result}")
    except Exception as e:
        play_sound(error_sound)
        log_action(f"Calculator error: {e}")
        messagebox.showerror("Error", f"Ошибка: {e}")

def clear_screen():
    play_sound(click_sound)
    log_action("Clear Screen command executed")
    os.system('cls' if platform.system().lower() == "windows" else 'clear')

def show_date():
    now = datetime.datetime.now()
    messagebox.showinfo("Date", f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

def get_weather():
    city = simpledialog.askstring("Weather", "Enter city:")
    if city:
        api_key = "YOUR_API_KEY"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        response = requests.get(f"{base_url}appid={api_key}&q={city}&units=metric")
        weather_data = response.json()
        if weather_data["cod"] != "404":
            main = weather_data["main"]
            play_sound(success_sound)
            log_action(f"Weather data for {city}: Temperature: {main['temp']}°C, Humidity: {main['humidity']}%, Description: {weather_data['weather'][0]['description']}")
            messagebox.showinfo("Weather", f"Temperature: {main['temp']}°C\nHumidity: {main['humidity']}%\nDescription: {weather_data['weather'][0]['description']}")
        else:
            play_sound(error_sound)
            log_action(f"Weather error: City not found ({city})")
            messagebox.showerror("Error", "City not found")

def guess_the_number():
    number = random.randint(1, 100)
    messagebox.showinfo("Guess the Number", "I'm thinking of a number between 1 and 100. Can you guess it?")
    attempts = 0
    while True:
        guess = simpledialog.askinteger("Guess the Number", "Enter your guess:")
        if guess is not None:
            attempts += 1
            if guess < number:
                play_sound(click_sound)
                messagebox.showinfo("Guess the Number", "Too low!")
            elif guess > number:
                play_sound(click_sound)
                messagebox.showinfo("Guess the Number", "Too high!")
            else:
                play_sound(success_sound)
                log_action(f"Guess the Number: Correct guess in {attempts} attempts")
                messagebox.showinfo("Guess the Number", f"Congratulations! You guessed the number in {attempts} attempts.")
                break

def list_files():
    files = os.listdir('.')
    file_list = "\n".join(files)
    messagebox.showinfo("Files in Current Directory", file_list)

def change_theme(root):
    themes = ttk.Style().theme_names()
    selected_theme = simpledialog.askstring("Change Theme", "Select a theme:", initialvalue=ttk.Style().theme.name, parent=root)
    if selected_theme in themes:
        ttk.Style().theme_use(selected_theme)

def change_font_size(root):
    new_size = simpledialog.askinteger("Change Font Size", "Enter new font size:", initialvalue=12, parent=root)
    if new_size:
        root.option_add("*Font", f"Helvetica {new_size}")
        root.update()

def install_exe():
    file_path = filedialog.askopenfilename(title="Select .exe file", filetypes=[("Executable files", "*.exe")])
    if file_path:
        try:
            subprocess.run(file_path, check=True)
            play_sound(success_sound)
            log_action(f"Install .exe: Installation started successfully ({file_path})")
            messagebox.showinfo("Installation", "Installation started successfully.")
        except subprocess.CalledProcessError as e:
            play_sound(error_sound)
            log_action(f"Install .exe error: {e}")
            messagebox.showerror("Error", f"Failed to start installation: {e}")

def install_apk():
    file_path = filedialog.askopenfilename(title="Select .apk file", filetypes=[("Android application package", "*.apk")])
    if file_path:
        try:
            subprocess.run(["adb", "install", file_path], check=True)
            play_sound(success_sound)
            log_action(f"Install .apk: APK installed successfully ({file_path})")
            messagebox.showinfo("Installation", "APK installed successfully.")
        except subprocess.CalledProcessError as e:
            play_sound(error_sound)
            log_action(f"Install .apk error: {e}")
            messagebox.showerror("Error", f"Failed to install APK: {e}")

def run_code():
    languages = {
        "Python": "python",
        "JavaScript": "node",
        "Java": "java",
        "C++": "g++",
        "C": "gcc",
        "Ruby": "ruby",
        "PHP": "php",
        "Perl": "perl",
        "Go": "go",
        "Rust": "rustc"
    }
    selected_language = simpledialog.askstring("Run Code", "Select a programming language:\n" + "\n".join(languages.keys()))
    if selected_language in languages:
        code = simpledialog.askstring("Run Code", f"Enter {selected_language} code:")
        if code:
            try:
                temp_file = f"temp.{languages[selected_language]}"
                with open(temp_file, "w") as f:
                    f.write(code)
                result = subprocess.run([languages[selected_language], temp_file], capture_output=True, text=True)
                play_sound(success_sound)
                log_action(f"Run Code: {selected_language} code executed successfully")
                messagebox.showinfo("Run Code", f"Output:\n{result.stdout}")
            except Exception as e:
                play_sound(error_sound)
                log_action(f"Run Code error: {e}")
                messagebox.showerror("Error", f"Failed to run code: {e}")
            finally:
                os.remove(temp_file)
    else:
        play_sound(error_sound)
        log_action("Run Code error: Invalid programming language selected")
        messagebox.showerror("Error", "Invalid programming language selected.")

def create_bottom_panel(root):
    bottom_panel = ttk.Frame(root, bootstyle="dark")
    bottom_panel.pack(side="bottom", fill="x")

    buttons = [
        ("Help", help),
        ("Clear Screen", clear_screen),
        ("Change Theme", lambda: change_theme(root)),
        ("Change Font Size", lambda: change_font_size(root)),
        ("Install .exe", install_exe),
        ("Install .apk", install_apk),
        ("Run Code", run_code),
        ("Save .wop App", save_wop_app),
        ("Load .wop App", load_wop_app),
        ("Open .watercash File", open_watercash_file),
        ("Compile Python to .wop", compile_python_to_wop),
        ("Run .wop App", run_wop_app)
    ]

    for text, command in buttons:
        ttk.Button(bottom_panel, text=text, command=command, bootstyle="outline-toolbutton").pack(side="left", padx=5, pady=5)

def main():
    root = ttk.Window(themename="cosmo")
    root.title("water dos [Версия 4.0]")
    root.geometry("800x600")

    create_bottom_panel(root)

    ttk.Label(root, text="(c) Компания sigma pc, 2024. Все права защищены.", font=("Helvetica", 12)).pack(pady=10)

    buttons = [
        ("Calculator", calculator),
        ("Show Date", show_date),
        ("Weather", get_weather),
        ("Guess the Number", guess_the_number),
        ("List Files", list_files)
    ]

    for text, command in buttons:
        ttk.Button(root, text=text, command=command, bootstyle=SUCCESS).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
