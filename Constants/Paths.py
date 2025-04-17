from pathlib import Path

USERPATH = Path.home()

SCRIPT_FOLDER = USERPATH / ("DataAnalytics")

EXCEL_FOLDER = SCRIPT_FOLDER / ("Tabelas - EXCEL")

SQL_FOLDER = SCRIPT_FOLDER / ("Tabelas - SQL")

SQL_PRODUCTS = SQL_FOLDER / ("Produtos.db")
SQL_EMPLOYEES = SQL_FOLDER / ("Funcionarios.db")
SQL_SUPPLIERS = SQL_FOLDER / ("Fornecedores.db")