from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import tkinter as tk
from tkinter import scrolledtext

# Проверка доступности GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Загрузка предварительно обученной модели и токенизатора DialoGPT
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

def chat_with_ai(user_input, chat_history_ids=None):
    # Токенизация пользовательского ввода
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)

    # Объединение истории чата с новым вводом
    if chat_history_ids is not None:
        input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        input_ids = new_input_ids

    # Создание attention mask
    attention_mask = torch.ones_like(input_ids)

    # Генерация ответа с дополнительными параметрами
    chat_history_ids = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        top_p=0.95,
        top_k=50,
        temperature=0.75  # Добавлен параметр температуры для управления креативностью ответа
    )

    # Декодирование ответа
    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with AI")

        self.chat_history_ids = None

        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_field = tk.Entry(self.input_frame)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def send_message(self, event=None):
        user_input = self.input_field.get()
        if user_input.lower() == 'выход':
            self.root.quit()
            return

        self.input_field.delete(0, tk.END)
        self.display_message("You: " + user_input)

        response, self.chat_history_ids = chat_with_ai(user_input, self.chat_history_ids)
        self.display_message("AI: " + response)

    def display_message(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message + "\n")
        self.chat_window.config(state='disabled')
        self.chat_window.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()
    
