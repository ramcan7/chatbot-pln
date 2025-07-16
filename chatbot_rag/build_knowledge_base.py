from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.schema import Document
from db.load_products import load_products


def build_vector_store():
    df = load_products()

    textos = []
    for _, row in df.iterrows():
        texto = f"""
        - Nombre: {row['product_name']}
        - Marca: {row['brand']}
        - Precio: S/ {row['price']} (Antes: S/ {row['list_price']})
        - Unidad: {row['unit_multiplier']} {row['measurement_unit']}
        - Categoría: {row['category']}
        - Promociones: {row['promotions']}
        - Métodos de pago: {row['payment_methods']}
        - Stock: {row['stock']} unidades
        """
        textos.append(Document(page_content=texto))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=len
    )
    chunks = splitter.split_documents(textos)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = Chroma.from_documents(chunks, embeddings, persist_directory="./vector_db")
    db.persist()


if __name__ == "__main__":
    build_vector_store()
