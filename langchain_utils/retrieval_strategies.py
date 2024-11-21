import os
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_cohere import CohereRerank
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline, EmbeddingsFilter, CrossEncoderReranker
from langchain_community.cross_encoders.huggingface import HuggingFaceCrossEncoder
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.retrievers import TavilySearchAPIRetriever


def simple_retriever(vectorstore, search_type='similarity', search_kwargs=None):
    """
    Create a retriever with customizable search parameters.

    Args:
        vectorstore: The vector store to retrieve documents from.
        search_type (str): The type of search. Options are 'similarity', 'mmr', 'similarity_score_threshold'.
        search_kwargs (dict, optional): Custom parameters for the search. Defaults to predefined settings for each type.

    Returns:
        A retriever object.
    """
    # Default search_kwargs for each search_type
    default_search_kwargs = {
        "similarity": {"k": 20},
        "mmr": {"k": 3, "fetch_k": 20, "lambda_mult": 0.5},
        "similarity_score_threshold": {"k": 3, "score_threshold": 0.1},
    }

    # Use provided search_kwargs or default to the predefined ones
    search_kwargs = search_kwargs or default_search_kwargs.get(search_type, {})

    return vectorstore.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

def get_reranker(provider="Cohere", model_name=None):
    """
    Creates a reranker based on the specified provider.

    Args:
        provider (str): The reranking provider ("Cohere" or "HuggingFace"). 
                        Defaults to "Cohere".
        model_name (str, optional): HuggingFace model name if using "HuggingFace". 
                                    Defaults to "BAAI/bge-reranker-v2-m3".

    Returns:
        object: A reranker for ranking documents.
    """
    if provider == "HuggingFace":
        model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
        compressor = CrossEncoderReranker(model=model, top_n=10)
    elif provider == "Cohere":
        compressor = CohereRerank(cohere_api_key=os.environ['COHERE_API_KEY'], model="rerank-multilingual-v3.0", top_n=10)

    return compressor

def create_pipeline_compressor(base_retriever, model='hkunlp/instructor-xl', provider="Cohere"):
    """
    Creates a pipeline compressor combining reranking, redundancy filtering, 
    and relevance filtering for document retrieval.

    Args:
        base_retriever: The base retriever to enhance with compression.
        model (str): The embeddings model for filtering. Defaults to 'hkunlp/instructor-xl'.
        provider (str): The reranker provider ("Cohere" or "HuggingFace"). Defaults to "Cohere".

    Returns:
        ContextualCompressionRetriever: A retriever with document compression.
    """    
    embeddings = HuggingFaceInstructEmbeddings(model_name=model)
    redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
    relevant_filter = EmbeddingsFilter(embeddings=embeddings,similarity_threshold=0.7)
    
    compressor = get_reranker(provider)
    pipeline = DocumentCompressorPipeline(transformers=[compressor,redundant_filter,relevant_filter])
    
    compression_retriever = ContextualCompressionRetriever(base_compressor=pipeline, base_retriever=base_retriever)
    
    return compression_retriever

def ensemble_retriever(base_retriever, chunks, provider="Cohere"):
    """
    Creates an ensemble retriever combining BM25 and a compression retriever.

    Args:
        base_retriever: The base retriever to use for compression.
        chunks (list): The text chunks for the BM25 retriever.
        provider (str): The reranker provider ("Cohere" or "HuggingFace"). Defaults to "Cohere".

    Returns:
        EnsembleRetriever: A retriever combining BM25 and compression-based retrieval.
    """
    compression_retriever = ContextualCompressionRetriever(base_compressor=get_reranker(provider), base_retriever=base_retriever)
    bm25_retriever = BM25Retriever.from_texts(chunks, search_kwargs={"k": 4})
    
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, compression_retriever])
    
    return ensemble_retriever

def retriever(llm, vectorstore, chunks=None, retriever_type='reranking_retriever', search_type='similarity', search_kwargs=None):
    """
    Create a history-aware retriever.

    Args:
        llm: Language model for query contextualization.
        vectorstore: Vector store for document retrieval.
        chunks (list, optional): Document chunks for ensemble retrievers. Defaults to None.
        retriever_type (str): Type of retriever to create. Options:
            - 'base_retriever'
            - 'multi_query_retriever'
            - 'reranking_retriever'
            - 'reranking_filtering_retriever'
            - 'ensemble_retriever'
        search_type (str, optional): Search strategy. Options: 'similarity', 'mmr', 'similarity_score_threshold'.
            Defaults to 'similarity'.
        search_kwargs (dict, optional): Additional search parameters. Defaults to None.

    Returns:
        A history-aware retriever object.

    Raises:
        ValueError: If an invalid `retriever_type` is provided.
    """

    ### Contextualize question ###
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    if retriever_type =='web_search_retriever':
        retriever = TavilySearchAPIRetriever()
    else:
        base_retriever = simple_retriever(vectorstore, search_type, search_kwargs)
        
        if retriever_type == 'base_retriever':
            retriever = base_retriever
        elif retriever_type == 'multi_query_retriever':
            retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
        elif retriever_type == 'reranking_retriever':
            retriever = ContextualCompressionRetriever(base_compressor=get_reranker(), base_retriever=base_retriever)
        elif retriever_type == 'reranking_filtering_retriever':
            retriever = create_pipeline_compressor(base_retriever)
        elif retriever_type == 'ensemble_retriever':
            retriever = ensemble_retriever(base_retriever, chunks)
        else:
            raise ValueError(f"Unknown retriever_type: {retriever_type}")
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    
    return history_aware_retriever