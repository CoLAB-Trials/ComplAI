import streamlit as st
from langchain.globals import set_debug
from langchain_utils.retrieval_strategies import retriever
from utils.reading_data import get_pdf_text_from_folder
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_utils.chunking_strategies import get_text_chunks
from utils_functions import setup_llm_pipeline, create_conversation_chain, initialize_embedding_model, query_rewriter
from langchain_utils.vectorstore_strategies import get_vectorstore, load_vectorstore, vectorstore_existence_check
from utils.config import load_config
from utils_functions import setup_llm_pipeline, create_conversation_chain, curate_dataset, initialize_embedding_model, query_rewriter, llm_initialization, clustering_chunks
from langchain_utils.vectorstore_strategies import get_vectorstore, load_vectorstore, vectorstore_existence_check
from langchain_utils.retrieval_strategies import retriever
from utils.reading_data import reader

#set_debug(True)

# Set page configuration at the very top
st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

def handle_userinput(user_question, llm, config):
    
    query = query_rewriter(llm, user_question) if config["rewrite_query"] else user_question             
    response = st.session_state.conversation.invoke({'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": st.session_state.chat_history})
    st.session_state.chat_history.extend([HumanMessage(content=user_question), SystemMessage(response["answer"])])
            

def main():
    
    config = load_config("config.yaml")
    embeddings = initialize_embedding_model()
    llm_rewriting = llm_initialization(model=config["models"]["rewriting"]["name"], provider=config["models"]["rewriting"]["provider"], temperature=config["models"]["rewriting"]["temperature"])
    llm_generation = llm_initialization(model=config["models"]["generation"]["name"], provider=config["models"]["generation"]["provider"], temperature=config["models"]["generation"]["temperature"])
    if "conversation" not in st.session_state:
        
        # Load or create vectorstore
        if vectorstore_existence_check(config):
            vectorstore = load_vectorstore(embeddings, config, llm=llm_generation)
        else:
            raw_text = reader(config["pdf_path"], config["reader"]["provider"], config["reader"]["file_type"])
            if config["reader"]["file_type"] == "PDF": 
                text_chunks = get_text_chunks(raw_text, config["chunking"]["chunk_size"], 
                                        config["chunking"]["chunk_overlap"], 
                                        method=config["chunking"]["type"])
            elif config["reader"]["file_type"] == "Markdown":
                text_chunks = raw_text
                
            vectorstore = get_vectorstore(text_chunks, embeddings=embeddings, config=config, llm=llm_generation)
            
            if config["data"]["rewriting"] or config["data"]["clustering"]:
                if config["data"]["clustering"]:
                    text_chunks = clustering_chunks(vectorstore=vectorstore, embeddings=embeddings)
                if config["data"]["rewriting"]:
                    text_chunks = curate_dataset(llm_rewriting, text_chunks)
                vectorstore = get_vectorstore(text_chunks, embeddings=embeddings, config=config, llm=llm_generation)

        # Setup conversation chain
        llm_retrieve = llm_initialization(model=config["models"]["retrieve"]["name"], provider=config["models"]["retrieve"]["provider"], temperature=config["models"]["retrieve"]["temperature"])
        retriever_chain = retriever(llm_retrieve, vectorstore, config=config, embeddings=embeddings)
        
        # create conversation chain
        st.session_state.conversation = create_conversation_chain(llm_generation, retriever_chain, config)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chatbot for regulation of medical devices")
    user_question = st.chat_input("Ask a question about medical devices regulation")

    if user_question:
        handle_userinput(user_question, llm_generation, config)
        
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.write(message.content)
        else:
            with st.chat_message("assistant"):
                st.write(message.content)
                


if __name__ == "__main__":
    main()
