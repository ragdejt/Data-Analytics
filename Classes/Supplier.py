import streamlit
import sqlite3
import pandas
from dataclasses import dataclass
from Constants.Paths import *

@dataclass
class Supplier:
    pass

    def to_dict(self):
        table_data = {
            "":[],
        }
    def NewExcelTable(self):
        try:
            with pandas.ExcelWriter(path=None, engine="xlsxwriter", mode="w") as writer:
                pandas.DataFrame(data=self.to_dict()).to_excel(excel_writer=writer, sheet_name="", index=False)
        except FileNotFoundError:
            pass
        else:
            pass
    def NewSQLTable(self):
        try:
            with sqlite3.connect(SQL_SUPPLIERS) as connect:
                cursor = connect.cursor()
                cursor.execute("""
                
                """)        
        except FileNotFoundError:
            pass
        else:
            connect.commit()

    def AddSQLTable(self):
        try:
            with sqlite3.connect(SQL_SUPPLIERS) as connect:
                cursor = connect.cursor()
                cursor.execute("""
                
                """)
        except FileNotFoundError:
            pass
        else:
            connect.commit()

    def SupplierPage():
        streamlit.title("Fornecedores")
        streamlit.sidebar.title("Fornecedores")
        options = streamlit.sidebar.selectbox(
            label="Selecione uma opção disponivel:",
            options=["Adicionar", "Remover"]
        )
       
        match options:
            case "Adicionar":
                pass
            case "Remover":
                pass
