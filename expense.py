import csv
import math
import datetime
import os
import sys
from collections import defaultdict
import argparse

import tabulate

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

def add(args):
    """Add a new expense using command-line arguments.
    
        Validates the amount and date, assigns the next expense ID,
        and saves the new record. 
    
        Raises:
            SystemExit: If arguments are insufficient or invalid.
    
        Side Effects:
            Appends the new expense to the existing expense records
            and persists the updated records to the CSV file.
        """
        
    amount = args.amount
        
    if not math.isfinite(amount) or amount <= 0:
        sys.exit("Amount must be a positive number")

    date = datetime.date.today().isoformat()
    
    if args.date:
        try:
            date = datetime.date.fromisoformat(args.date).isoformat()
        except ValueError:
            sys.exit("Date must be YYYY-MM-DD")

    note = args.notes if args.notes else ""

    existing_rows = load_expenses()
    curr_row = {
        "id": max(int(r["id"]) for r in existing_rows) + 1 if existing_rows else 1,
        "date": date,
        "amount": f"{amount:.2f}",
        "category": args.category.lower(),
        "note": note,
    }
    existing_rows.append(curr_row)
    save_expenses(existing_rows)

    msg = f"Added #{curr_row['id']}: ₹{curr_row['amount']} {curr_row['category']}"
    print(f"{msg} ({note})" if note else msg)

def list_expense(expenses, empty_msg = "No Expenses yet."):
    """Display expense records in a table.

    Args:
        expenses (list[dict]): Expense records to display.
        empty_msg (str): Message to display when no records exist.

    Sorts records by date and ID before displaying them.
    """
    
    if not expenses:
        print(empty_msg)
        return
    
    sorted_expenses = sorted(expenses, key = lambda row: (row['date'], int(row['id'])))
    
    display_expenses = [
        {**row, "amount": f"{float(row['amount']):.2f}"}
        for row in sorted_expenses
    ]
    
    print(tabulate.tabulate(display_expenses, headers = "keys", tablefmt = "psql", floatfmt=".2f"))

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

def month(args):
    """Displays expenses and total for the given month of the current year."""
    
    n = args.month

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

def delete(args):
    """Delete an expense using its unique ID.

    Reads the expense ID from command-line arguments and removes
    the corresponding record from the CSV file.

    Side Effects:
        Rewrites the CSV file without the specified expense.
    """

    n = args.id

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
            

def list_command(args):
    list_expense(load_expenses())


def total_command(args):
    total(load_expenses())

def main(argv=None):
    parser = argparse.ArgumentParser(prog="cli-expense-tracker", description="Command-Line Expense Tracker")

    subparser = parser.add_subparsers(dest="command",description="Subparser",help="Subcommand Help", required=True)

    subparser_add = subparser.add_parser("add", help="Saves a row with the next id and today's date. The note & date is optional.")
    subparser_add.add_argument("amount", type=float)
    subparser_add.add_argument("category")
    subparser_add.add_argument("--note")
    subparser_add.add_argument("--date")
    subparser_add.set_defaults(func=add)

    subparser_list = subparser.add_parser("list", help="Prints every expense as a neat table, or No expenses yet.")
    subparser_list.set_defaults(func=list_command)

    subparser_total = subparser.add_parser("total", help="Prints spend per category, then a grand total.")
    subparser_total.set_defaults(func=total_command)

    subparser_month = subparser.add_parser("month", help="Lists and Totals expenses only for valid months (1 -12).")
    subparser_month.add_argument("month", choices=range(1,13), type=int)
    subparser_month.set_defaults(func=month)

    subparser_delete = subparser.add_parser("delete", help="removes expense #id, or prints Expense #id not found.")
    subparser_delete.add_argument("id", type=int)
    subparser_delete.set_defaults(func=delete)

    args = parser.parse_args(argv)

    # print(args)
    
    args.func(args)

if __name__ == "__main__":
    main()