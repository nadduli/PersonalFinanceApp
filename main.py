import tkinter as tk
from tkinter import ttk, messagebox
import csv

class PersonalFinanceApp:
    def __init__(self, root: tk.Tk):
        """
        Initialize the PersonalFinanceApp.

        Args:
        root: The root window for the app.
        """
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("600x400")

        # Data Storage
        self.transactions = []

        # Header
        tk.Label(self.root, text="Personal Finance Manager", font=("Arial", 16, "bold")).pack(pady=10)

        # Add Transaction Frame
        self.add_frame = tk.Frame(self.root, padx=10, pady=10)
        self.add_frame.pack(fill=tk.X)

        tk.Label(self.add_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Income")
        self.type_dropdown = ttk.Combobox(self.add_frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly")
        self.type_dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.add_frame)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.add_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.add_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.add_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=1, column=2, columnspan=2, pady=5)

        # Transaction List
        self.transaction_frame = tk.Frame(self.root, padx=10, pady=10)
        self.transaction_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.transaction_frame, columns=("Type", "Category", "Amount"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_transaction)
        self.delete_button.pack(pady=5)

        # Export Button
        self.export_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(pady=5)

    def add_transaction(self):
        trans_type = self.type_var.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        if not category or not amount:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        self.transactions.append((trans_type, category, amount))
        self.tree.insert("", "end", values=(trans_type, category, amount))

        # Clear inputs
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No transaction selected.")
            return

        for item in selected_item:
            self.tree.delete(item)

        # Remove from data storage
        self.transactions = [
            trans for idx, trans in enumerate(self.transactions)
            if f"I{idx}" not in selected_item
        ]

    def export_to_csv(self):
        if not self.transactions:
            messagebox.showwarning("Warning", "No transactions to export.")
            return

        with open("transactions.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Category", "Amount"])
            writer.writerows(self.transactions)

        messagebox.showinfo("Success", "Transactions exported to transactions.csv.")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceApp(root)
    root.mainloop()
