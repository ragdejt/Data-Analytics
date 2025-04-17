import pandas
import sqlite3
import streamlit
from Constants.Paths import *
from dataclasses import dataclass

@dataclass
class Product:
    name:str
    category:str
    sku:int
    brand:str
    manufacturer:str
    model:str
    version:str
    height:float 
    width:float
    length:float
    weight:float
    price:float

    def get_data(self):
        table_data = {
            "Nome":[self.name],
            "Categoria":[self.category],
            "SKU":[self.sku],
            "Marca":[self.brand],
            "Fabricante":[self.manufacturer],
            "Modelo":[self.model],
            "Versão":[self.version],
            "Altura":[self.height],
            "Largura":[self.width],
            "Comprimento":[self.length],
            "Peso":[self.weight],
            "Preço":[self.price]
        }
        return table_data
    
    def NewExcelTable(self):
        with pandas.ExcelWriter(path=EXCEL_FOLDER / (f"{self.name}.xlsx"), engine="xlsxwriter") as writer:
            pandas.DataFrame(data=self.get_data()).to_excel(excel_writer=writer, sheet_name=self.name)
            
    def NewSQLTable(self):
        with sqlite3.connect(SQL_PRODUCTS) as connect:
            cursor = connect.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Produtos (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Categoria TEXT NOT NULL,
            SKU INTEGER NOT NULL,
            Marca TEXT NOT NULL,
            Fabricante TEXT NOT NULL,
            Modelo TEXT NOT NULL,
            Versão TEXT NOT NULL,
            Altura FLOAT NOT NULL,
            Largura FLOAT NOT NULL,
            Comprimento NOT NULL,
            Peso NOT NULL,
            Preço NOT NULL
            )
            """)
            connect.commit()

    def AddSQLTable(self):
        with sqlite3.connect(SQL_PRODUCTS) as connect:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO Produtos (
                Nome, Categoria, SKU, Marca, Fabricante, Modelo, Versão,
                Altura, Largura, Comprimento, Peso, Preço
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.name, self.category, self.sku, self.brand, self.manufacturer,
                self.model, self.version, self.height, self.width, self.length,
                self.weight, self.price
            ))
            connect.commit()

    def ProductPage():
        streamlit.set_page_config(
            page_title="Data Analytics - Produto",
            page_icon=None,
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        streamlit.sidebar.title("Data Analytics")
        options = streamlit.sidebar.selectbox(
            label="Selecione uma opção disponivel:",
            options=["Adicionar", "Editar", "Remover"]
        )
        streamlit.title("Data Analytics")
        
        match options:
            case "Adicionar":
                streamlit.header("Adicionar Produto!")

                product_name = streamlit.text_input(
                    label="Nome do Produto",
                    type="default",
                    help="Product name",
                    placeholder="Digite o nome do Produto"
                )
                storage_type = streamlit.selectbox(
                    label="Tipo de armazenamento",
                    options=["Seco", "Resfriado", "Congelado", "Ultra Congelado"],
                    help="Storage type",
                    placeholder="Escolha uma opção"
                )
                brand = streamlit.text_input(
                    label="Marca",
                    type="default",
                    help="Brand",
                    placeholder="Digite a marca"
                )
                manufacturer = streamlit.text_input(
                    label="Fabricante",
                    type="default",
                    help="Manufacturer",
                    placeholder="Digite o fabricante"
                )
                model = streamlit.text_input(
                    label="Modelo",
                    type="default",
                    help="Model",
                    placeholder="Digite o modelo"
                )
                version = streamlit.text_input(
                    label="Versão",
                    type="default",
                    help="Version",
                    placeholder="Digite a versão"
                )
                height = streamlit.text_input(
                    label="Altura",
                    type="default",
                    help="Height",
                    placeholder="Digite a altura"
                )
                width = streamlit.text_input(
                    label="Largura",
                    type="default",
                    help="Width",
                    placeholder="Digite a largura"
                )
                length = streamlit.text_input(
                    label="Comprimento",
                    type="default",
                    help="Length",
                    placeholder="Digite o comprimento"
                )
                weight = streamlit.text_input(
                    label="Peso",
                    type="default",
                    help="Weight",
                    placeholder="Digite o peso"
                )
                price = streamlit.text_input(
                    label="Preço",
                    type="default",
                    help="Price",
                    placeholder="Digite o preço"
                )

                if streamlit.button(label="Cadastrar", key="RegisterButton", help="Register", on_click=None, icon=None, use_container_width=True):
                    try:
                        new_product = Product(
                            name=product_name,
                            category=storage_type,
                            sku="0",
                            brand=brand,
                            manufacturer=manufacturer,
                            model=model,
                            version=version,
                            height=height,
                            width=width,
                            length=length,
                            weight=weight,
                            price=price
                        )
                        new_product.NewSQLTable()
                        new_product.AddSQLTable()
                        new_product.NewExcelTable()
                        streamlit.success("Produto cadastrado com sucesso!")
                        streamlit.session_state["show_product_input"] = False
                    except Exception:
                        streamlit.error("Erro ao cadastrar produto!")
            case "Editar":
                pass
            case "Remover":
                pass

