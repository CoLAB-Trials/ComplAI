from langchain_community.vectorstores import faiss
from langchain_milvus import Milvus
import os
from langchain.chains import HypotheticalDocumentEmbedder
from typing import List, Dict, Any, Optional
from langchain.chains import HypotheticalDocumentEmbedder, LLMChain
from langchain.prompts import PromptTemplate

def _get_store_path(config: Dict[str, Any]) -> str:
    """Generate the storage path based on configuration.

    Constructs the path based on the configuration parameters. For
    boolean values, includes the key name if `True`, and omits it otherwise.

    Args:
        config: Configuration dictionary containing chunking, data, and embeddings information.

    Returns:
        str: The constructed storage path.
    """
    clustering = "clustering" if config['data']['clustering'] else ""
    rewriting = "rewriting" if config['data']['rewriting'] else ""
    
    return f"_{config['chunking']['type']}_{config['chunking']['chunk_size']}_{config['chunking']['chunk_overlap']}{clustering}{rewriting}"

def get_vectorstore(text_chunks: List[str], embeddings: Any, config: Dict[str, Any], llm: Optional[Any] = None) -> Any:
    """Create a new vectorstore with the given text chunks and embeddings.
    
    Args:
        text_chunks: List of text segments to store.
        embeddings: Embedding model to use.
        config: Configuration dictionary.
        llm: Optional language model for HypotheticalDocumentEmbedder.
    
    Returns:
        Any: The initialized vector store.
        
    Raises:
        ValueError: If an invalid vectorstore provider is specified.
    """
    store_path = _get_store_path(config)
    if config['HyDe']:
        if config["system"] == "md_class":
            prompt_template = """Hypothetically describe the medical device and its functionalities: {question}
            Answer:"""
            prompt = PromptTemplate(input_variables=["QUESTION"], template=prompt_template)
            embeddings = HypotheticalDocumentEmbedder.from_llm(llm=llm, base_embeddings=embeddings, custom_prompt=prompt)
        else:
            embeddings = HypotheticalDocumentEmbedder.from_llm(llm=llm, base_embeddings=embeddings, prompt_key='web_search')
    if config["vectorstore"]["provider"] == "FAISS":    
        vectorstore = faiss.FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        vectorstore.save_local(f"db/faiss_index{store_path}")
    elif config["vectorstore"]["provider"] == "Milvus":
        print(text_chunks)
        vectorstore = Milvus.from_documents(
                documents=text_chunks,
                embedding=embeddings,
                connection_args={
                    "uri": "in03-88a0c9bd0f51ecf.serverless.gcp-us-west1.cloud.zilliz.com",
                    "token": "f19a5ce7ea1662aee58534a57cb9dab3b930f05f8899a3a359121c04d21fbf8a6babf3f4a0bfecd362e94af0b201a31316ef3e98",  # API key, for serverless clusters which can be used as replacements for user and password
                    "secure": True,
                    },
                drop_old=True,
        )
    else:
        raise ValueError(f"Unsupported vectorstore provider: {config['vectorstore']['provider']}")
    
    return vectorstore

def load_vectorstore(embeddings: Any, config: Dict[str, Any], llm: Optional[Any] = None) -> Any:
    """Load an existing vectorstore from disk.
    
    Args:
        embeddings: Embedding model to use.
        config: Configuration dictionary.
        llm: Optional language model for HypotheticalDocumentEmbedder.
    
    Returns:
        Any: The loaded vector store.
        
    Raises:
        ValueError: If an invalid vectorstore provider is specified.
    """
    store_path = _get_store_path(config)
    if config['HyDe']:
        if config["system"] == "md_class":
            prompt_template = """Hypothetically describe the medical device and its functionalities: {question}
            Answer:"""
            prompt = PromptTemplate(input_variables=["QUESTION"], template=prompt_template)
            embeddings = HypotheticalDocumentEmbedder.from_llm(llm=llm, base_embeddings=embeddings, custom_prompt=prompt)
        else:
            embeddings = HypotheticalDocumentEmbedder.from_llm(llm=llm, base_embeddings=embeddings, prompt_key='web_search')
    if config["vectorstore"]["provider"] == "Milvus":
        vectorstore = Milvus(
            embedding_function=embeddings,
            connection_args={
                    "uri": "in03-88a0c9bd0f51ecf.serverless.gcp-us-west1.cloud.zilliz.com",
                    "token": "f19a5ce7ea1662aee58534a57cb9dab3b930f05f8899a3a359121c04d21fbf8a6babf3f4a0bfecd362e94af0b201a31316ef3e98",  # API key, for serverless clusters which can be used as replacements for user and password
                    "secure": True,
                    },
        )
    elif config["vectorstore"]["provider"] == "FAISS":
        vectorstore = faiss.FAISS.load_local(
            f"db/faiss_index{store_path}", 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    else:
        raise ValueError(f"Unsupported vectorstore provider: {config['vectorstore']['provider']}")
        
    return vectorstore

def vectorstore_existence_check(config: Dict[str, Any]) -> bool:
    """Check if a vectorstore exists for the given configuration.
    
    Args:
        config: Configuration dictionary.
    
    Returns:
        bool: True if the vectorstore exists, False otherwise.
        
    Raises:
        ValueError: If an invalid vectorstore provider is specified.
    """
    store_path = _get_store_path(config)
    
    if config["vectorstore"]["provider"] == "Milvus":
        return os.path.exists(f"db/./milvus{store_path}.db")
    elif config["vectorstore"]["provider"] == "FAISS":
        return os.path.exists(f"db/faiss_index{store_path}")
    else:
        raise ValueError(f"Unsupported vectorstore provider: {config['vectorstore']['provider']}")