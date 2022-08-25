# Python Command-Line Contact Book
#### https://github.com/M-Moon/crud-basiccontactbook

<br>

This small Python program allows you to store, view, add, and delete contacts on a local database.
It features all 4 basic CRUD operations, utilising SQLite3.

## Usage
Using Python, run the program from the command-line and select an available option using the dash (-) convention.
```
python3 contactbook.py -v [View] -a [Add] -e [Edit] -d [Delete] -f [ViewAll] -h [Help]
```

The program will then walk you through the steps for your selected task.

Inputs must be typed *exactly*, including being case-sensitive, to match any column names or values in the contact book

Including desired values as command-line arguments has not yet been added.

## Disclaimer

This was done as a simple, quick and small experimental project to practise using a db in Python.

The contents of the db are **NOT** encrypted or protected so please do **not** store any sensitive information using this program. You have been warned.
