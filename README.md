# Mnemosine

A database indexing utility designed to organize and route data across multiple SQLite database files based on an index mapping. Named after the Greek goddess of memory, Mnemosyne, the project aims to optimize personal knowledge and archive retrieval.

## Features

- **SQLite Backend**: Uses Python's native `sqlite3` library to interface with lightweight, self-contained databases.
- **Index Routing**: Leverages an index database (`index.db`) containing mappings (e.g., ID, key, path) to route data queries to specific sub-databases.
- **Python Interface**: Class-based database connector (`mnemosine.py`) for custom routing functions.
- **Tracking Sheet**: Includes an Excel file (`Index_database.xlsx`) summarizing the database indices and schema design.

## Files

- `mnemosine.py`: Main class interface module for database routing.
- `index.db`: The master sqlite3 database catalog containing routing indexes.
- `Index_database.xlsx`: Spreadsheet detailing the database schema index configuration.
- `prova.py`: Sandbox script for testing tables, inserts, and selections.

## Requirements

- Python 3.x
- `sqlite3` (built-in)

## How to Run

1. Initialize or query the master database with the script:
   ```bash
   python prova.py
   ```
2. Import `database` class from `mnemosine.py` to route queries programmatically:
   ```python
   from mnemosine import database
   db = database("path/to/database/dir/")
   ```
