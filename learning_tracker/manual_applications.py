"""Local manual application notebook. No service integration or automatic imports."""
import tkinter as tk
from tkinter import ttk, messagebox

LABELS = {"planned": "В плане", "sent": "Отправлен", "viewed": "Просмотрен", "invited": "Приглашение",
          "screening": "Скрининг", "technical": "Техническое", "final": "Финал", "offer": "Оффер",
          "rejected": "Отказ", "withdrawn": "Отозван", "unknown": "Неизвестно"}


def is_submitted(item):
    if item.get("status") not in LABELS or item.get("status") in {"planned", "unknown"} or item.get("application_origin") == "employer":
        return False
    return bool(item.get("submitted_at") or item.get("status") not in {"withdrawn", "invited"})


class ApplicationsWindow(tk.Toplevel):
    def __init__(self, master, store, on_change):
        from app import BG, PANEL, TEXT, MUTED, label, button
        super().__init__(master)
        self.store, self.on_change = store, on_change
        self.title("Ручной учёт откликов")
        self.geometry("960x700")
        self.configure(bg=BG)
        label(self, "Ручной учёт откликов", size=22, pack={"anchor": "w", "padx": 20, "pady": 12})
        label(self, "Только твои записи. Поиска, импорта, синхронизации и автоматической отправки нет.",
              color=MUTED, pack={"anchor": "w", "padx": 20})
        form = tk.Frame(self, bg=PANEL, padx=18, pady=12)
        form.pack(fill="x", padx=20, pady=12)
        self.fields = {}
        for key, caption in (("company", "Компания"), ("role", "Должность"), ("url", "Ссылка (необязательно)"), ("note", "Заметка / следующий шаг")):
            label(form, caption, pack={"anchor": "w"})
            field = tk.Entry(form, bg=BG, fg=TEXT, insertbackground=TEXT)
            field.pack(fill="x", ipady=4, pady=(0, 5))
            self.fields[key] = field
        self.stage = ttk.Combobox(form, values=list(LABELS.values()), state="readonly")
        self.stage.set(LABELS["planned"])
        self.stage.pack(anchor="w", pady=6)
        button(form, "Добавить запись", self.add, primary=True).pack(anchor="w")
        bar = tk.Frame(self, bg=BG)
        bar.pack(side="bottom", fill="x", padx=20, pady=8)
        button(bar, "Применить выбранный этап к строке", self.change_stage).pack(side="left")
        self.tree = ttk.Treeview(self, columns=("company", "role", "status", "note"), show="headings")
        for key, title in (("company", "Компания"), ("role", "Должность"), ("status", "Этап"), ("note", "Заметка")):
            self.tree.heading(key, text=title)
        self.tree.pack(fill="both", expand=True, padx=20, pady=8)
        self.render()

    def status(self):
        return next(k for k, value in LABELS.items() if value == self.stage.get())

    def add(self):
        values = {k: field.get().strip() for k, field in self.fields.items()}
        if not values["company"] or not values["role"]:
            messagebox.showerror("Запись", "Укажи компанию и должность.", parent=self)
            return
        self.store.add_application(status=self.status(), **values)
        self.render()
        self.on_change()

    def change_stage(self):
        selected = self.tree.selection()
        if selected:
            self.store.update_application_status(selected[0], self.status())
            self.render()
            self.on_change()

    def render(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.store.data.get("applications", []):
            self.tree.insert("", "end", iid=item["id"], values=(item.get("company"), item.get("role"), LABELS.get(item.get("status")), item.get("note")))
