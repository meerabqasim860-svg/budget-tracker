import json
import os

DATA_FILE = "budget_data.json"


def load_transactions():
    """Load saved transactions, or start with an empty list."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_transactions(transactions):
    """Save all transactions to the data file."""
    with open(DATA_FILE, "w") as file:
        json.dump(transactions, file, indent=2)


def get_amount():
    """Keep asking until the user types a valid number above 0."""
    while True:
        try:
            amount = float(input("Amount: £"))
            if amount > 0:
                return round(amount, 2)
            print("Please enter a number greater than 0.")
        except ValueError:
            print("That's not a valid number. Try again.")


def add_transaction(transactions, kind):
    """Add an income or an expense."""
    amount = get_amount()
    category = input("Category (e.g. food, travel, wages): ").strip().lower()
    if category == "":
        category = "other"
    transactions.append({"type": kind, "amount": amount, "category": category})
    save_transactions(transactions)
    print(f"{kind.capitalize()} of £{amount:.2f} added.")


def view_transactions(transactions):
    """List every transaction."""
    if not transactions:
        print("No transactions yet.")
        return
    for number, t in enumerate(transactions, start=1):
        sign = "+" if t["type"] == "income" else "-"
        print(f"{number}. {sign}£{t['amount']:.2f}  ({t['category']})")


def show_summary(transactions):
    """Show totals, balance and spending by category."""
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    print(f"Total income:   £{income:.2f}")
    print(f"Total expenses: £{expenses:.2f}")
    print(f"Balance:        £{income - expenses:.2f}")

    spending = {}
    for t in transactions:
        if t["type"] == "expense":
            spending[t["category"]] = spending.get(t["category"], 0) + t["amount"]
    if spending:
        print("\nSpending by category:")
        for category, total in sorted(spending.items(), key=lambda item: item[1], reverse=True):
            print(f"  {category}: £{total:.2f}")


def main():
    transactions = load_transactions()
    while True:
        print("\n--- Budget Tracker ---")
        print("1. Add income")
        print("2. Add expense")
        print("3. View transactions")
        print("4. Show summary")
        print("5. Quit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_transaction(transactions, "income")
        elif choice == "2":
            add_transaction(transactions, "expense")
        elif choice == "3":
            view_transactions(transactions)
        elif choice == "4":
            show_summary(transactions)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
