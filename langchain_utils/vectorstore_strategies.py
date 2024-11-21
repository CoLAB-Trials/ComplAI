from langchain_community.vectorstores import faiss

def get_vectorstore(text_chunks, embeddings):
        
    vectorstore = faiss.FAISS.from_texts(
        texts=text_chunks, embedding=embeddings)
    
    vectorstore.save_local("faiss_index")
    
    return vectorstore