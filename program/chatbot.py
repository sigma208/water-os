
import tkinter as tk
from tkinter import scrolledtext, ttk
import json
import random

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой Чат-Бот с Обучением")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_frame = ttk.Frame(self.notebook)
        self.learn_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.chat_frame, text="Чат")
        self.notebook.add(self.learn_frame, text="Обучение")

        self.setup_chat_tab()
        self.setup_learn_tab()

        self.knowledge_base = self.load_knowledge_base()

    def setup_chat_tab(self):
        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.chat_frame)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_field = tk.Entry(self.input_frame)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Отправить", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def setup_learn_tab(self):
        self.learn_window = scrolledtext.ScrolledText(self.learn_frame, wrap=tk.WORD, state='disabled')
        self.learn_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.learn_input_frame = tk.Frame(self.learn_frame)
        self.learn_input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.learn_input_field = tk.Entry(self.learn_input_frame)
        self.learn_input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.learn_input_field.bind("<Return>", self.save_learned_message)

        self.learn_button = tk.Button(self.learn_input_frame, text="Сохранить", command=self.save_learned_message)
        self.learn_button.pack(side=tk.RIGHT)

    def send_message(self, event=None):
        user_message = self.input_field.get()
        if user_message:
            self.display_message("Вы", user_message, self.chat_window)
            response = self.process_message(user_message)
            self.display_message("Бот", response, self.chat_window)
            self.input_field.delete(0, tk.END)

    def display_message(self, sender, message, window):
        window.config(state='normal')
        window.insert(tk.END, f"{sender}: {message}\n")
        window.config(state='disabled')
        window.yview(tk.END)

    def process_message(self, message):
        message = message.lower()
        if message in self.knowledge_base:
            return random.choice(self.knowledge_base[message])
        else:
            return "Извините, я не понял. Можете переформулировать?"

    def save_learned_message(self, event=None):
        user_response = self.learn_input_field.get()
        if user_response:
            parts = user_response.split(" - ")
            if len(parts) == 2:
                intent = parts[0].strip()
                response = parts[1].strip()
                if intent not in self.knowledge_base:
                    self.knowledge_base[intent] = []
                self.knowledge_base[intent].append(response)
                self.display_message("Бот", f"Я запомнил: '{intent}' - '{response}'", self.learn_window)
                self.save_knowledge_base()
                self.learn_input_field.delete(0, tk.END)

    def save_knowledge_base(self):
        with open("knowledge_base.json", "w", encoding="utf-8") as file:
            json.dump(self.knowledge_base, file, ensure_ascii=False, indent=4)

    def load_knowledge_base(self):
        try:
            with open("knowledge_base.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                "привет": ["Привет! Чем могу помочь?", "Здравствуй! Как я могу вам помочь?"],
                "здравствуй": ["Привет! Чем могу помочь?", "Здравствуй! Как я могу вам помочь?"],
                "пока": ["До свидания! Хорошего дня!", "Пока! Буду рад снова вам помочь!"],
                "до свидания": ["До свидания! Хорошего дня!", "Пока! Буду рад снова вам помочь!"],
                "как дела": ["Я просто бот, но у меня все отлично! А у вас?", "У меня все хорошо! Как у вас дела?"]
            }

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
