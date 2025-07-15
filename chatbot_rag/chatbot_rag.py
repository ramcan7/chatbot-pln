from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.memory import ConversationBufferMemory

def cargar_chat_con_memoria():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./vector_db", embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 30})

    llm = OllamaLLM(
        model="llama3.2:3b",
        model_kwargs={
            "temperature": 0.3,
            "top_k": 30,
            "top_p": 0.90,
            "num_predict": 60
        }
    )
    memoria = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    prompt_es = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template="""
        You are METROBot, a friendly shopping assistant for METRO supermarket in Peru.
        Your task is to assist users by providing accurate, helpful recommendations about METRO's real products, brands, promotions, and shopping tips, using only the information available in the provided context. 
        Never respond with information unrelated to the user’s question.
        You must only answer questions directly related to METRO's catalog or services. If a user asks about something unrelated (e.g., personal, sensitive, or off-topic), respond briefly and kindly redirect the conversation to METRO-related content.
        
        Important rules:
        - If the user asks about payment methods, do not invent or assume. Use only the exact information from the product context.
        - If the retrieved product context does not contain any relevant match do NOT attempt to guess or recommend unrelated items. Do NOT invent or assume product, categories or sections.
        - Only mention products that are present in the provided context.
        - Do not invent product names, brands, categories, or prices. If the context does not contain the product requested, respond politely that it is not available in the current catalog.
        - If recommending a product, always include its full name and exact price from the context.
        - Never use placeholders like “[insert price here]” or uncertain expressions like “I think” or “probably”.
        
        Your tone should be warm, helpful, and approachable — like a trusted in-store advisor.
        
        Use the following to generate your answer:
        
        Recent conversation history:
        {chat_history}

        METROS´s Products information available (context):
        {context}

        Question:
        {question}

        Answer (always in Spanish):
        """.strip()
    )

    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memoria,
        combine_docs_chain_kwargs={"prompt": prompt_es}
    )

    return chat_chain

def ejecutar_chat():
    chat = cargar_chat_con_memoria()
    print("Hola soy METROBot, tu chatbot de confianza para comprar.")

    while True:
        pregunta = input("Tú: ").strip()
        if pregunta.lower() in ["salir", "exit"]:
            print("Bot: ¡Hasta pronto! 😊")
            break
        respuesta_completa = chat.invoke(pregunta)
        respuesta = respuesta_completa["answer"]
        print(f"\nBot:\n{respuesta}\n")

if __name__ == "__main__":
    ejecutar_chat()
