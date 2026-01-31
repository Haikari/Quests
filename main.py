#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk, font
# from PIL import Image, ImageTk  # Not needed
import json
import logging
import os
import shutil
import sys

APP_NAME = "Quests"
APP_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", APP_NAME)
os.makedirs(APP_DIR, exist_ok=True)

log_file = os.path.join(APP_DIR, "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Single instance check
lock_file = os.path.join(APP_DIR, "app.lock")

def _pid_is_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True

if os.path.exists(lock_file):
    try:
        with open(lock_file, "r") as f:
            existing_pid = int((f.read() or "0").strip())
    except Exception:
        existing_pid = 0

    if existing_pid and _pid_is_running(existing_pid):
        sys.exit(0)
    else:
        try:
            os.remove(lock_file)
        except Exception:
            pass

with open(lock_file, "w") as f:
    f.write(str(os.getpid()))

def cleanup():
    if os.path.exists(lock_file):
        os.remove(lock_file)

# Register cleanup on exit
import atexit
atexit.register(cleanup)

class Quest:
    def __init__(self, name, difficulty, exp_reward, coin_reward, description=""):
        self.name = name
        self.difficulty = difficulty
        self.exp_reward = exp_reward
        self.coin_reward = coin_reward
        self.description = description
        self.completed = False

class Player:
    def __init__(self):
        self.total_exp = 0
        self.total_coins = 0

    @property
    def level(self):
        exp_needed = 0
        level = 0
        base = 100.0
        while self.total_exp >= exp_needed:
            level += 1
            exp_needed += int(base)
            base *= 1.2
        return level - 1

class QuestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarefas")
        # Load icon - not working in executable
        # try:
        #     icon_image = Image.open("icon.png")
        #     icon_photo = ImageTk.PhotoImage(icon_image)
        #     self.root.iconphoto(True, icon_photo)
        # except Exception as e:
        #     print(f"Could not load icon: {e}")
        self.player = Player()
        self.quests = []
        self.data_file = os.path.join(APP_DIR, "quests.json")
        self.config = {"dark_theme": False, "font_size": 10, "annotations": ""}
        self.style = ttk.Style()
        self.load_data()
        # self.apply_theme()  # Moved later

        # Player info
        self.player_frame = tk.Frame(root)
        self.player_frame.pack(pady=10)
        self.level_label = tk.Label(self.player_frame, text=f"Nível: {self.player.level}")
        self.level_label.pack(side=tk.LEFT, padx=10)
        self.exp_label = tk.Label(self.player_frame, text=f"EXP: {self.player.total_exp}")
        self.exp_label.pack(side=tk.LEFT, padx=10)
        self.coins_label = tk.Label(self.player_frame, text=f"Moedas: {self.player.total_coins}")
        self.coins_label.pack(side=tk.LEFT, padx=10)

        # Create quest frame
        self.create_frame = tk.Frame(root)
        self.create_frame.pack(pady=10)
        tk.Label(self.create_frame, text="Nome da Quest:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.create_frame)
        self.name_entry.grid(row=0, column=1)
        tk.Label(self.create_frame, text="Dificuldade (0-10):").grid(row=1, column=0)
        self.difficulty_spin = tk.Spinbox(self.create_frame, from_=0, to=10)
        self.difficulty_spin.grid(row=1, column=1)
        tk.Label(self.create_frame, text="Recompensa EXP:").grid(row=2, column=0)
        self.exp_entry = tk.Entry(self.create_frame)
        self.exp_entry.grid(row=2, column=1)
        tk.Label(self.create_frame, text="Recompensa Moedas:").grid(row=3, column=0)
        self.coins_entry = tk.Entry(self.create_frame)
        self.coins_entry.grid(row=3, column=1)
        tk.Label(self.create_frame, text="Descrição:").grid(row=4, column=0)
        self.description_entry = tk.Text(self.create_frame, height=3, width=30)
        self.description_entry.grid(row=4, column=1)
        self.create_button = tk.Button(self.create_frame, text="Criar Quest", command=self.create_quest)
        self.create_button.grid(row=5, columnspan=2, pady=5)

        # Settings button
        self.settings_button = tk.Button(root, text="Configurações", command=self.open_settings)
        self.settings_button.pack(pady=5)
        # Annotations button
        self.annotations_button = tk.Button(root, text="Anotações", command=self.open_annotations)
        self.annotations_button.pack(pady=5)

        # Notebook for quests
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, fill="both", expand=True)

        # Active quests tab
        self.active_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.active_frame, text="Quests Ativas")
        self.active_tree = ttk.Treeview(self.active_frame, columns=("name", "difficulty", "exp", "coins", "description"), show="headings")
        self.active_tree.heading("name", text="Nome")
        self.active_tree.heading("difficulty", text="Dificuldade")
        self.active_tree.heading("exp", text="EXP")
        self.active_tree.heading("coins", text="Moedas")
        self.active_tree.heading("description", text="Descrição")
        self.active_tree.pack(fill="both", expand=True)
        self.complete_button = tk.Button(self.active_frame, text="Completar Quest Selecionada", command=self.complete_quest)
        self.complete_button.pack(pady=5)
        self.delete_button = tk.Button(self.active_frame, text="Excluir Quest Selecionada", command=self.delete_quest)
        self.delete_button.pack(pady=5)

        # History tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="Histórico")
        self.history_tree = ttk.Treeview(self.history_frame, columns=("name", "difficulty", "exp", "coins", "description"), show="headings")
        self.history_tree.heading("name", text="Nome")
        self.history_tree.heading("difficulty", text="Dificuldade")
        self.history_tree.heading("exp", text="EXP")
        self.history_tree.heading("coins", text="Moedas")
        self.history_tree.heading("description", text="Descrição")
        self.history_tree.pack(fill="both", expand=True)

        self.update_quest_list()

        self.apply_theme()  # Apply theme after creating widgets

        # Save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_quest(self):
        name = self.name_entry.get()
        try:
            difficulty = int(self.difficulty_spin.get())
            exp = int(self.exp_entry.get())
            coins = int(self.coins_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
            return
        if not name:
            messagebox.showerror("Erro", "Nome da quest não pode estar vazio.")
            return
        description = self.description_entry.get("1.0", tk.END).strip()
        quest = Quest(name, difficulty, exp, coins, description)
        self.quests.append(quest)
        self.update_quest_list()
        self.clear_create_fields()

    def clear_create_fields(self):
        self.name_entry.delete(0, tk.END)
        self.difficulty_spin.delete(0, tk.END)
        self.difficulty_spin.insert(0, "0")
        self.exp_entry.delete(0, tk.END)
        self.coins_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)

    def update_quest_list(self):
        # Clear active
        for item in self.active_tree.get_children():
            self.active_tree.delete(item)
        # Clear history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        for quest in self.quests:
            if not quest.completed:
                self.active_tree.insert("", tk.END, values=(quest.name, quest.difficulty, quest.exp_reward, quest.coin_reward, quest.description))
            else:
                self.history_tree.insert("", tk.END, values=(quest.name, quest.difficulty, quest.exp_reward, quest.coin_reward, quest.description))

    def complete_quest(self):
        selected = self.active_tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma quest para completar.")
            return
        item = selected[0]
        values = self.active_tree.item(item, "values")
        name = values[0]
        for quest in self.quests:
            if quest.name == name and not quest.completed:
                quest.completed = True
                self.player.total_exp += quest.exp_reward
                self.player.total_coins += quest.coin_reward
                self.update_player_info()
                self.update_quest_list()
                messagebox.showinfo("Sucesso", f"Quest '{name}' completada! Ganhou {quest.exp_reward} EXP e {quest.coin_reward} moedas.")
                break

    def update_player_info(self):
        self.level_label.config(text=f"Nível: {self.player.level}")
        self.exp_label.config(text=f"EXP: {self.player.total_exp}")
        self.coins_label.config(text=f"Moedas: {self.player.total_coins}")

    def apply_theme(self):
        if self.config["dark_theme"]:
            bg_color = "#333333"
            fg_color = "white"
            self.root.configure(bg=bg_color)
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TLabel", background=bg_color, foreground=fg_color)
            self.style.configure("TButton", background=bg_color, foreground=fg_color)
            self.style.configure("Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color)
            self.style.map("Treeview", background=[("selected", "#555555")])
            # Update existing widgets
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg=bg_color)
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=bg_color, fg=fg_color)
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=bg_color, fg=fg_color)
        else:
            bg_color = "#f0f0f0"
            fg_color = "black"
            self.root.configure(bg=bg_color)
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TLabel", background=bg_color, foreground=fg_color)
            self.style.configure("TButton", background=bg_color, foreground=fg_color)
            self.style.configure("Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color)
            self.style.map("Treeview", background=[("selected", "#cce7ff")])
            # Reset widgets
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg=bg_color)
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=bg_color, fg=fg_color)
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=bg_color, fg=fg_color)

        # Apply font
        self.default_font = font.Font(size=self.config["font_size"])
        self.style.configure("TLabel", font=self.default_font)
        self.style.configure("TButton", font=self.default_font)
        self.style.configure("Treeview", font=self.default_font)
        self.style.configure("Treeview.Heading", font=self.default_font)
        # Ajustar altura das linhas do Treeview conforme o tamanho da fonte
        row_height = int(self.config["font_size"] * 2.2)  # ajuste o multiplicador se necessário
        self.style.configure("Treeview", rowheight=row_height)
        # Update tk widgets font
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Spinbox)):
                widget.config(font=self.default_font)
        # Adjust treeview column widths based on font size
        base_width = 120
        extra_width = self.config["font_size"] * 10  # Increased multiplier
        for tree in [self.active_tree, self.history_tree]:
            tree.column("name", width=base_width + extra_width, stretch=True)
            tree.column("difficulty", width=100 + extra_width // 2, stretch=True)
            tree.column("exp", width=80 + extra_width // 2, stretch=True)
            tree.column("coins", width=90 + extra_width // 2, stretch=True)
            tree.column("description", width=base_width + extra_width * 3, stretch=True)  # More space for description

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Configurações")
        settings_win.geometry("300x200")
        dark_var = tk.BooleanVar(value=self.config["dark_theme"])
        tk.Checkbutton(settings_win, text="Tema Escuro", variable=dark_var).pack(pady=20)
        tk.Label(settings_win, text="Tamanho da Fonte:").pack(pady=5)
        font_spin = tk.Spinbox(settings_win, from_=8, to=20)
        font_spin.delete(0, tk.END)
        font_spin.insert(0, str(self.config["font_size"]))
        font_spin.pack()
        tk.Button(settings_win, text="Aplicar", command=lambda: self.apply_settings(dark_var.get(), int(font_spin.get()), settings_win)).pack()

    def open_annotations(self):
        annotations_win = tk.Toplevel(self.root)
        annotations_win.title("Anotações")
        annotations_win.geometry("400x300")
        text_area = tk.Text(annotations_win)
        text_area.pack(fill="both", expand=True)
        text_area.insert("1.0", self.config["annotations"])
        def save_annotations():
            self.config["annotations"] = text_area.get("1.0", tk.END).strip()
            self.save_data()
            annotations_win.destroy()
        tk.Button(annotations_win, text="Salvar", command=save_annotations).pack()

    def apply_settings(self, dark_theme, font_size, win):
        self.config["dark_theme"] = dark_theme
        self.config["font_size"] = font_size
        self.apply_theme()
        self.save_data()
        win.destroy()

    def delete_quest(self):
        selected = self.active_tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma quest para excluir.")
            return
        item = selected[0]
        values = self.active_tree.item(item, "values")
        name = values[0]
        for i, quest in enumerate(self.quests):
            if quest.name == name and not quest.completed:
                del self.quests[i]
                self.update_quest_list()
                messagebox.showinfo("Sucesso", f"Quest '{name}' excluída.")
                break

    def load_data(self):
        if not os.path.exists(self.data_file):
            legacy_file = "quests.json"
            if os.path.exists(legacy_file):
                try:
                    shutil.copy2(legacy_file, self.data_file)
                except Exception:
                    logging.exception("Falha ao migrar dados antigos")

        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.player.total_exp = data.get("exp", 0)
                self.player.total_coins = data.get("coins", 0)
                self.config = data.get("config", {"dark_theme": False, "font_size": 10, "annotations": ""})
                quests_data = data.get("quests", [])
                for q in quests_data:
                    quest = Quest(q["name"], q["difficulty"], q["exp_reward"], q["coin_reward"], q.get("description", ""))
                    quest.completed = q.get("completed", False)
                    self.quests.append(quest)

    def save_data(self):
        data = {
            "exp": self.player.total_exp,
            "coins": self.player.total_coins,
            "config": self.config,
            "quests": [
                {
                    "name": q.name,
                    "difficulty": q.difficulty,
                    "exp_reward": q.exp_reward,
                    "coin_reward": q.coin_reward,
                    "description": q.description,
                    "completed": q.completed
                } for q in self.quests
            ]
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    try:
        logging.info("Iniciando o app")
        root = tk.Tk()
        logging.info("Tk inicializado")
        app = QuestApp(root)
        logging.info("Interface construída")
        root.mainloop()
        logging.info("Loop principal encerrado")
    except Exception:
        logging.exception("Erro fatal ao iniciar o app")
        raise
    