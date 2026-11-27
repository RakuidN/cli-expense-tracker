# **Command Line Expense Tracker**

## *Description*
This program is a command-line expense tracker which can be used to track your expenses efficiently.

## *Installation*

## *Usage*
You have to provide command-line arguments.

The following are the list of arguments you can execute:
1. ***list***: Prints every expense as a neat table, or No expenses yet.
2. ***total***: Prints spend per category, then a grand total.
3. ***month N***: Lists and totals only expenses for months 1 - 12. 
4. ***delete N***: Removes expense #N, or prints Expense #N not found.
5. ***add AMOUNT CATEGORY [NOTE] [--date YYYY-MM-DD]***: Saves a row with the next id and today's date. The note & date is optional.

### Sample Commands:  

*python expenses.py list*  

Output:
```
+------+------------+----------+------------+------------------+
|   id | date       |   amount | category   | notes            |
|------+------------+----------+------------+------------------|
|    4 | 2026-10-22 |   100.00 | bike       | oil              |
|    1 | 2026-11-22 |   210.00 | reading    | siddhartha       |
|    3 | 2026-11-22 |   979.00 | play       | playstation-plus |
+------+------------+----------+------------+------------------+
```  
*python expenses.py total*  

Output:
```
Categories: Expense
play: 979.00
reading: 210.00
bike: 100.00
Grand Total: 1289.00
```
*python expenses.py month 11*  

Output:  

```
+------+------------+----------+------------+------------------+
|   id | date       |   amount | category   | notes            |
|------+------------+----------+------------+------------------|
|    1 | 2026-11-22 |   210.00 | reading    | siddhartha       |
|    3 | 2026-11-22 |   979.00 | play       | playstation-plus |
+------+------------+----------+------------+------------------+
Categories: Expense
play: 979.00
reading: 210.00
Grand Total: 1189.00
```  

*python expenses.py delete 4*  

Output:  

```
Deleted #4.
```  

*python expenses.py add 350 music earphones --date 2026-12-11*  

Output:  

```
Added #4: ₹350.00 music (earphones)
```


## What I learned
- Reading and writing CSV files with `csv.DictReader` and `csv.DictWriter`, and keeping the file's header in sync with the code (a renamed column broke saving).
- Parsing command-line arguments by hand with `sys.argv`, including optional flags like `--date`.
- Validating input before touching the file: each check gets its own clear error message instead of a traceback.
- When to use `print` versus `sys.exit`: empty data is a normal result, bad input is an error.
- Python has no function overloading, because a second `def` with the same name replaces the first. Default arguments are the Python way.
- Dispatching commands with `match`/`case`, and grouping totals with `collections.defaultdict`.
- Generating unique IDs with `max()` rather than trusting the order of rows.

## *License*
MIT License

## *Contact*
LinkedIn: RakuidN