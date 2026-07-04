import tkinter as tk

OPERATORS = {"+", "-", "*", "/"}
VALID_KEY_CHARS = set("0123456789+-*/.()%")

LIGHT_THEME = {
    "bg": "#f0f0f0",
    "display_bg": "#ffffff",
    "display_fg": "#000000",
    "button_bg": "#e0e0e0",
    "button_fg": "#000000",
}

DARK_THEME = {
    "bg": "#2b2b2b",
    "display_bg": "#1e1e1e",
    "display_fg": "#ffffff",
    "button_bg": "#3c3c3c",
    "button_fg": "#ffffff",
}


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.history = []
        self.buttons = []
        self.theme = LIGHT_THEME

        self._build_display()
        self._build_buttons()
        self._build_history()
        self._apply_theme()

        self.bind_all("<Key>", self._on_key)

    def _build_display(self):
        self.display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Segoe UI", 24),
            justify="right",
            state="readonly",
            bd=0,
            relief="flat",
        )
        self.display.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=8, pady=8)

        self.theme_button = tk.Button(
            self,
            text="\U0001F319",
            font=("Segoe UI", 14),
            command=self._toggle_theme,
        )
        self.theme_button.grid(row=0, column=3, sticky="nsew", padx=2, pady=8)

    def _build_buttons(self):
        rows = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "%"],
        ]

        for r, row in enumerate(rows, start=1):
            for c, label in enumerate(row):
                btn = tk.Button(
                    self,
                    text=label,
                    font=("Segoe UI", 16),
                    width=4,
                    height=2,
                    command=lambda l=label: self._on_press(l),
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons.append(btn)

    def _build_history(self):
        label = tk.Label(self, text="History", font=("Segoe UI", 12, "bold"))
        label.grid(row=0, column=4, sticky="nsew", padx=(8, 4), pady=(8, 0))

        self.history_box = tk.Listbox(self, width=20, font=("Segoe UI", 11))
        self.history_box.grid(row=1, column=4, rowspan=5, sticky="nsew", padx=(8, 4), pady=4)

    def _on_press(self, label):
        if label == "C":
            self.expression = ""
        elif label == "=":
            self._evaluate()
            return
        else:
            self.expression += label

        self.display_var.set(self.expression or "0")

    def _backspace(self):
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression or "0")

    def _on_key(self, event):
        if event.char in VALID_KEY_CHARS:
            self._on_press(event.char)
        elif event.keysym in ("Return", "KP_Enter"):
            self._on_press("=")
        elif event.keysym == "BackSpace":
            self._backspace()
        elif event.keysym == "Escape":
            self._on_press("C")

    def _evaluate(self):
        expr = self.expression
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            self.expression = str(result)
        except Exception:
            self.expression = ""
            result = "Error"
        self.display_var.set(str(result))

        if expr:
            entry = f"{expr} = {result}"
            self.history.append(entry)
            self.history_box.insert(tk.END, entry)
            self.history_box.see(tk.END)

    def _toggle_theme(self):
        self.theme = DARK_THEME if self.theme is LIGHT_THEME else LIGHT_THEME
        self._apply_theme()

    def _apply_theme(self):
        t = self.theme
        self.configure(bg=t["bg"])
        self.display.configure(readonlybackground=t["display_bg"], fg=t["display_fg"])
        self.history_box.configure(bg=t["display_bg"], fg=t["display_fg"])
        for btn in self.buttons:
            btn.configure(bg=t["button_bg"], fg=t["button_fg"])
        self.theme_button.configure(bg=t["button_bg"], fg=t["button_fg"])


if __name__ == "__main__":
    Calculator().mainloop()
