import tkinter as tk


class ProductsDialog(tk.Toplevel):
    def __init__(self, parent, existing=None):
        super().__init__(parent)
        self.title("Product")
        self.geometry("300x260")
        self.data = {}

        fields = ["name", "reference", "price", "quantity"]
        self.entries = {}

        for field in fields:
            tk.Label(self, text=field.capitalize()).pack(pady=(8, 0))
            entry = tk.Entry(self, width=30)
            entry.pack(pady=(0, 5))
            self.entries[field] = entry

        if existing:
            # existing is expected as (id, name, reference, price, quantity)
            self.entries["name"].insert(0, existing[1])
            self.entries["reference"].insert(0, existing[2])
            self.entries["price"].insert(0, existing[3])
            self.entries["quantity"].insert(0, existing[4])

        tk.Button(self, text="Save", command=self.save).pack(pady=15)

    def save(self):
        name = self.entries["name"].get().strip()
        if not name:
            return  # keep it simple: just don't close if name is empty
        self.data = {
            "name": name,
            "reference": self.entries["reference"].get().strip(),
            "price": self.entries["price"].get().strip() or "0",
            "quantity": self.entries["quantity"].get().strip() or "0",
        }
        self.destroy()

    def get_data(self):
        return self.data
