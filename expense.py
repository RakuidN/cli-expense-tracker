import csv
import math
import datetime
import os
import sys
from collections import defaultdict

import tabulate

USAGE_TEXT = "Need to use with the available commands:\n\n1. list \t\t\t\t\t\t\t\t:prints every expense as a neat table, or No expenses yet. \n2. total \t\t\t\t\t\t\t\t:prints spend per category, then a grand total.\n3. month N \t\t\t\t\t\t\t\t:lists and totals only expenses for months 1 - 12.\n4. delete N \t\t\t\t\t\t\t\t:removes expense #N, or prints Expense #N not found.\n5. add AMOUNT CATEGORY [NOTE] [--date YYYY-MM-DD] \t\t\t:saves a row with the next id and today's date. The note & date is optional.\n"

FILE = "expenses.csv"


def load_expenses():
    """Load all expenses from the CSV file.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary
        represents an expense. Returns an empty list if the file
        does not exist.
    """
    
    if not os.path.exists(FILE):
        return []
    
    with open(FILE, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        
        return list(reader)

def save_expenses(expenses):
    """Save expense records to the CSV file.

    Args:
        expenses (list[dict]): Expense records containing id, date,
            amount, category, and notes.

    Side Effects:
        Overwrites the existing CSV file with the supplied records.
    """
    
    with open(FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "date", "amount", "category", "note"])
        
        writer.writeheader()
        
        for row in expenses:
            writer.writerow(row)

def add():
    """Add a new expense using command-line arguments.
    
        Parses the amount, category, optional note, and optional date
        from sys.argv. Assigns a unique sequential ID and saves the
        expense to the CSV file.
    
        Raises:
            SystemExit: If arguments are insufficient or invalid.
    
        Side Effects:
            Appends the new expense to the existing expense records
            and persists the updated records to the CSV file.
        """
    if len(sys.argv) < 4:
        sys.exit("Usage: add AMOUNT CATEGORY [NOTE] [--date YYYY-MM-DD]")

    try:
        amount = float(sys.argv[2])
    except ValueError:
        sys.exit("Amount must be a number, like 250 or 99.50")
    if not math.isfinite(amount) or amount <= 0:
        sys.exit("Amount must be a positive number")

    date = datetime.date.today().isoformat()
    if "--date" in sys.argv:
        i = sys.argv.index("--date")
        if i + 1 >= len(sys.argv):
            sys.exit("--date needs a value, like 2026-11-23")
        try:
            date = datetime.date.fromisoformat(sys.argv[i + 1]).isoformat()
        except ValueError:
            sys.exit("Date must be YYYY-MM-DD")

    note = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "--date" else ""

    existing_rows = load_expenses()
    curr_row = {
        "id": max(int(r["id"]) for r in existing_rows) + 1 if existing_rows else 1,
        "date": date,
        "amount": f"{amount:.2f}",
        "category": sys.argv[3].lower(),
        "note": note,
    }
    existing_rows.append(curr_row)
    save_expenses(existing_rows)

    msg = f"Added #{curr_row['id']}: ₹{curr_row['amount']} {curr_row['category']}"
    print(f"{msg} ({note})" if note else msg)

def list_expense(expenses, empty_msg = "No Expenses yet."):
    """List expenses in a tabular format.
    
    expenses: List of dictionaries containes expenses as per the CSV format.
    """   
    
    if not expenses:
        print(empty_msg)
        return
    
    expenses = sorted(expenses, key = lambda row: (row['date'], int(row['id'])))
    
    for row in expenses:
        row["amount"] = f"{float(row['amount']):.2f}"
    
    print(tabulate.tabulate(expenses, headers = "keys", tablefmt = "psql", floatfmt=".2f"))

def total(expenses):
    """Prints expenses per category along with a grand total.
    
    expenses: List of dictionaries containes expenses as per the CSV format.
    """
    
    if not expenses:
        print("No Expenses yet.")
        return
    
    categories = defaultdict(float)
            
    grand_total = 0
            
    for row in expenses:
        categories[row['category']] += float(row['amount'])
        grand_total += float(row['amount'])
            
    print("Categories: Expense")
            
    for category, amount in sorted(categories.items(), key = lambda x: x[1], reverse=True):
        print(f"{category}: {amount:.2f}")
    print(f"Grand Total: {grand_total:.2f}")

def month():
    """Lists expenses and displays total for the given month of the current year."""
    if len(sys.argv) != 3:
        sys.exit("Usage: month N  (N is 1 to 12)")

    try:
        n = int(sys.argv[2])
    except ValueError:
        sys.exit("Month must be a number from 1 to 12")
    if not 1 <= n <= 12:
        sys.exit("Month must be 1 to 12")

    current_year = datetime.date.today().year
    filtered_expenses = []
    for row in load_expenses():
        row_year, row_month, _ = row["date"].split("-")
        if int(row_month) == n and int(row_year) == current_year:
            filtered_expenses.append(row)

    if not filtered_expenses:
        print("No expenses for that month.")
        return

    list_expense(filtered_expenses)
    total(filtered_expenses)

def delete():
    """Delete an expense using its unique ID.

    Reads the expense ID from command-line arguments and removes
    the corresponding record from the CSV file.

    Side Effects:
        Rewrites the CSV file without the specified expense.
    """
    
    if len(sys.argv) != 3:
        sys.exit("Insufficient Arguments.")
    
    try:
        n = int(sys.argv[2])

        expenses = load_expenses() 
        
        filtered_expenses = []
                
        for row in expenses:
            if int(row["id"]) != n:
                filtered_expenses.append(row)
        
        if len(filtered_expenses) == len(expenses):
            print(f"Expense #{n} not found.")
        else:
            save_expenses(filtered_expenses)
            print(f"Deleted #{n}.")
            
            
    except ValueError:
        sys.exit("Invalid Arguments")


def main():
    
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        sys.exit(USAGE_TEXT)
    
    cmd = sys.argv[1]
    if cmd not in ("add", "list", "total", "month", "delete"):
        print(f"Unknown command: {cmd}")
        sys.exit(USAGE_TEXT)
    
    match cmd:
        case "add":
            add()
        case "list":
            list_expense(load_expenses())
        case "total":
            total(load_expenses())
        case "month":
            month()
        case "delete":
            delete()
            
            
if __name__ == "__main__":
    main()