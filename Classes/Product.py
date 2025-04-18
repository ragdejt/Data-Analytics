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

    
    def to_dict(self):
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
        try:
            with pandas.ExcelWriter(path=EXCEL_FOLDER / (f"{self.name}.xlsx"), engine="xlsxwriter", mode="w") as writer:
                pandas.DataFrame(data=self.to_dict()).to_excel(excel_writer=writer, sheet_name=self.name, index=False)
        except FileNotFoundError:
            pass
            
    def NewSQLTable():
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

    def ProductPage():
        streamlit.sidebar.title("Produtos")
        options = streamlit.sidebar.selectbox(
            label="Selecione uma opção disponivel:",
            options=["Adicionar", "Remover"]
        )
        
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

                if streamlit.button(label="Cadastrar", help="Register", icon=None, use_container_width=True):
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
                        new_product.AddSQLTable()
                        new_product.NewExcelTable()
                        streamlit.success("Produto cadastrado com sucesso!")
                    except Exception:
                        streamlit.error("Erro ao cadastrar produto!")
            case "Remover":
                streamlit.header("Remover Produto!")
                product_remove = streamlit.text_input(
                    label="Nome do produto",
                    type="default",
                    help="Product name",
                    placeholder="Digite o nome do produto"
                )
                if streamlit.button(label="Procurar", help="Search", icon=None, use_container_width=True):
                    with sqlite3.connect(SQL_PRODUCTS) as connect:
                        cursor = connect.cursor()
                        cursor.execute("SELECT * FROM Produtos WHERE Nome = ?", (product_remove,))
                        results = cursor.fetchall()
                        if results:
                            streamlit.success("Produto encontrado com sucesso!")
                            df = pandas.DataFrame(results)
                            streamlit.dataframe(df)
                            streamlit.success("Produto removido!")
                            cursor.execute("DELETE FROM Produtos WHERE Nome = ?", (product_remove,))
                            connect.commit()
                        else:
                            streamlit.error("Produto não encontrado!")
                    