import streamlit as st
from langchain.globals import set_debug
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_utils.chunking_strategies import get_text_chunks, get_recursive_text_chunks
from utils_functions import setup_llm_pipeline, create_conversation_chain, curate_dataset, initialize_embedding_model
from langchain_utils.vectorstore_strategies import get_vectorstore
from langchain_utils.retrieval_strategies import retriever
from utils.reading_data import get_pdf_text_from_folder, unstructured_pdf_reader
import os
from langchain_community.vectorstores import faiss

set_debug(True)

# Set page configuration at the very top
st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

def handle_userinput(user_question):
                
    response = st.session_state.conversation.invoke({'input': user_question + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": st.session_state.chat_history})
    st.session_state.chat_history.extend([HumanMessage(content=user_question), SystemMessage(response["answer"])])
            

def main():
    
    if "conversation" not in st.session_state:
        embeddings = initialize_embedding_model()
    
        if os.path.exists("faiss_index"):
            vectorstore = faiss.FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        else:
            pdf_docs = '/mnt/c/Users/pc/Documents/complAI/Training materials for models'
            # Envokes a function that gets the pdf_text
            raw_text = get_pdf_text_from_folder(pdf_docs)

            # Get the text chunks
            text_chunks = get_recursive_text_chunks(raw_text, 1000, 200)
            # create vector store
            vectorstore = get_vectorstore(text_chunks, embeddings=embeddings)
        
        llm = setup_llm_pipeline()

        history_aware_retriever = retriever(llm, vectorstore, retriever_type='ensemble_retriever')
        
        # create conversation chain
        st.session_state.conversation = create_conversation_chain(llm, history_aware_retriever)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chatbot for regulation of medical devices")
    user_question = st.chat_input("Ask a question about medical devices regulation:")

    if user_question:
        handle_userinput(user_question)
        
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.write(message.content)
        else:
            with st.chat_message("assistant"):
                st.write(message.content)
                


if __name__ == "__main__":
    main()
