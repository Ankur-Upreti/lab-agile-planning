import tkinter as tk

OPERATORS = {"+", "-", "*", "/"}


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        self._build_display()
        self._build_buttons()

    def _build_display(self):
        display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Segoe UI", 24),
            justify="right",
            state="readonly",
            bd=0,
            relief="flat",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)

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

    def _on_press(self, label):
        if label == "C":
            self.expression = ""
        elif label == "=":
            self._evaluate()
            return
        else:
            self.expression += label

        self.display_var.set(self.expression or "0")

    def _evaluate(self):
        try:
            result = eval(self.expression, {"__builtins__": {}}, {})
            self.expression = str(result)
        except Exception:
            self.expression = ""
            result = "Error"
        self.display_var.set(str(result))


if __name__ == "__main__":
    Calculator().mainloop()
