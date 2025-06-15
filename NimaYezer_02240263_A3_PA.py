
import uuid
import tkinter as tk
from tkinter import messagebox


class Account:
    def __init__(self, account_type):
        self.account_id = str(uuid.uuid4())[:8]
        self.passcode = str(uuid.uuid4())[:4]
        self.account_type = account_type
        self.funds = 0.0
        self.phone_balance = 0.0

    def deposit(self, amount):
        self.funds += amount
        return f"Nu{amount} deposited successfully."

    def withdraw(self, amount):
        if amount > self.funds:
            return "Insufficient funds."
        self.funds -= amount
        return f"Nu{amount} withdrawn successfully."

    def transfer(self, amount, recipient_account):
        if amount > self.funds:
            return "Insufficient funds for transfer."
        self.funds -= amount
        recipient_account.funds += amount
        return f"Nu{amount} transferred to {recipient_account.account_id}."

    def top_up_phone(self, amount):
        if amount > self.funds:
            return "Insufficient funds for top-up."
        self.funds -= amount
        self.phone_balance += amount
        return f"Phone topped up with Nu{amount}."


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_type):
        account = Account(account_type)
        self.accounts[account.account_id] = account
        return account

    def login(self, account_id, passcode):
        account = self.accounts.get(account_id)
        if account and account.passcode == passcode:
            return account
        return None


class BankingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Application")
        self.bank = BankingSystem()
        self.account = None
        self.init_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def init_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Banking App", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Account ID").pack()
        self.account_id_entry = tk.Entry(self.root)
        self.account_id_entry.pack()

        tk.Label(self.root, text="Passcode").pack()
        self.passcode_entry = tk.Entry(self.root, show='*')
        self.passcode_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Create Account", command=self.init_account_creation).pack()

    def init_account_creation(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Account Type").pack()

        self.account_type_var = tk.StringVar(value="Personal")
        tk.Radiobutton(self.root, text="Personal", variable=self.account_type_var, value="Personal").pack()
        tk.Radiobutton(self.root, text="Business", variable=self.account_type_var, value="Business").pack()

        tk.Button(self.root, text="Create", command=self.create_account).pack()

    def create_account(self):
        acc_type = self.account_type_var.get()
        account = self.bank.create_account(acc_type)
        messagebox.showinfo("Account Created",
                            f"ID: {account.account_id}\nPasscode: {account.passcode}")
        self.init_login_screen()

    def login(self):
        acc_id = self.account_id_entry.get()
        passcode = self.passcode_entry.get()
        account = self.bank.login(acc_id, passcode)
        if account:
            self.account = account
            self.init_account_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def init_account_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.account.account_id}", font=("Arial", 14)).pack()

        tk.Label(self.root, text=f"Balance: Nu{self.account.funds:.2f}").pack()
        tk.Label(self.root, text=f"Phone Balance: Nu{self.account.phone_balance:.2f}").pack()

        self.amount_entry = self.create_labeled_entry("Amount:")
        self.recipient_entry = self.create_labeled_entry("Recipient ID (for Transfer):")

        tk.Button(self.root, text="Deposit", command=self.deposit).pack()
        tk.Button(self.root, text="Withdraw", command=self.withdraw).pack()
        tk.Button(self.root, text="Transfer", command=self.transfer).pack()
        tk.Button(self.root, text="Phone Top-up", command=self.phone_top_up).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.init_login_screen).pack(pady=10)

    def create_labeled_entry(self, label_text):
        tk.Label(self.root, text=label_text).pack()
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            msg = self.account.deposit(amount)
            self.init_account_dashboard()
            messagebox.showinfo("Success", msg)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid amount.")

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            msg = self.account.withdraw(amount)
            self.init_account_dashboard()
            messagebox.showinfo("Success", msg)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid amount.")

    def transfer(self):
        try:
            amount = float(self.amount_entry.get())
            recipient_id = self.recipient_entry.get()
            if recipient_id not in self.bank.accounts:
                raise KeyError
            recipient_account = self.bank.accounts[recipient_id]
            msg = self.account.transfer(amount, recipient_account)
            self.init_account_dashboard()
            messagebox.showinfo("Success", msg)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid amount.")
        except KeyError:
            messagebox.showerror("Error", "Recipient not found.")

    def phone_top_up(self):
        try:
            amount = float(self.amount_entry.get())
            msg = self.account.top_up_phone(amount)
            self.init_account_dashboard()
            messagebox.showinfo("Success", msg)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid amount.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingAppGUI(root)
    root.mainloop()
