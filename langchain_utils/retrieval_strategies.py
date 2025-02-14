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
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.retrievers import ParentDocumentRetriever
from langchain.schema import Document

def simple_retriever(vectorstore: Chroma, search_type: str = 'similarity', search_kwargs: dict = None) -> Chroma:
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

def get_reranker(provider: str = "Cohere", model_name: str = None, top_n: int = 10, api_key = os.environ['COHERE_API_KEY']) -> object:
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
        model = HuggingFaceCrossEncoder(model_name=model_name)
        compressor = CrossEncoderReranker(model=model, top_n=top_n)
    elif provider == "Cohere":
        compressor = CohereRerank(cohere_api_key=api_key, model="rerank-multilingual-v3.0", top_n=top_n)

    return compressor

def create_pipeline_compressor(base_retriever: Chroma, model: str = 'hkunlp/instructor-xl', provider: str = "Cohere", top_n: int = 10, model_name: str = None) -> ContextualCompressionRetriever:
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
    relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.7)
    
    compressor = get_reranker(provider, model_name=model_name, top_n=top_n)
    pipeline = DocumentCompressorPipeline(transformers=[compressor, redundant_filter, relevant_filter])
    
    compression_retriever = ContextualCompressionRetriever(base_compressor=pipeline, base_retriever=base_retriever)
    
    return compression_retriever

def ensemble_retriever(retrievers: list) -> EnsembleRetriever:
    """
    Creates an ensemble retriever combining multiple retrievers.

    Args:
        retrievers (list): List of retrievers to combine.

    Returns:
        EnsembleRetriever: A retriever combining multiple retrieval strategies.
    """
    ensemble_retriever = EnsembleRetriever(retrievers=retrievers, k=1)
    
    return ensemble_retriever

def parent_document_retriever(text_chunks: list, embeddings: object) -> ParentDocumentRetriever:
    """
    Creates a parent document retriever that indexes child chunks and retrieves parent documents.

    Args:
        text_chunks (list): List of text chunks to be indexed.
        embeddings: Embedding function to use for vector store.

    Returns:
        ParentDocumentRetriever: A retriever that retrieves parent documents based on child chunks.
    """
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=4000)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=300)
    vectorstore = Chroma(
        collection_name="full_documents", embedding_function=embeddings
    )
    store = InMemoryStore()
    
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )
    retriever.add_documents(text_chunks)
    
    return retriever

def retriever(llm: object, vectorstore: Chroma, chunks: list = None, config: dict = None, embeddings: object = None, api_key = os.environ['COHERE_API_KEY']) -> object:
    """
    Create a history-aware retriever based on the provided configuration.

    Args:
        llm: Language model for query contextualization.
        vectorstore: Vector store for document retrieval.
        chunks (list, optional): Document chunks for ensemble retrievers. Defaults to None.
        config (dict): Configuration dictionary specifying retriever type, search type, and other parameters.
        embeddings (object, optional): Embedding function for parent document retriever. Defaults to None.

    Returns:
        object: A history-aware retriever object.

    Raises:
        ValueError: If an invalid `retriever_type` is provided.
    """
    # Contextualize question
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

    # Determine the type of retriever to create
    retriever_type = config["retrieval"]["type"]
    if retriever_type == 'web_search_retriever':
        retriever = TavilySearchAPIRetriever()
    elif retriever_type == 'parent_document_retriever':
        retriever = parent_document_retriever(chunks, embeddings)
    else:
        base_retriever = simple_retriever(vectorstore, config["retrieval"]["search_type"], config["retrieval"]["search_kwargs"])
        if retriever_type == 'base_retriever':
            retriever = base_retriever
        elif retriever_type == 'multi_query_retriever':
            retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
        elif retriever_type == 'ensemble_retriever':
            retrievers = []
            ensemble_config = config["retrieval"]["ensemble_retriever"]
            if "web_search_retriever" in ensemble_config:
                retrievers.append(TavilySearchAPIRetriever(k=4))
            if "multi_query_retriever" in ensemble_config:
                retrievers.append(MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm))
            if "base_retriever" in ensemble_config:
                retrievers.append(base_retriever)
            if "keyword_retriever" in ensemble_config:
                retrievers.append(BM25Retriever.from_texts(chunks, search_kwargs={"k": 4}))
            retriever = ensemble_retriever(retrievers)
        else:
            raise ValueError(f"Unknown retriever_type: {retriever_type}")

    # Apply filtering and reranking if enabled
    if config["retrieval"]["filtering"]["enabled"] and config["retrieval"]["reranking"]["enabled"]:
        retriever = create_pipeline_compressor(
            retriever,
            model=config["retrieval"]["filtering"]["embedding_model"],
            provider=config["retrieval"]["reranking"]["provider"],
            top_n=config["retrieval"]["reranking"]["top_n"],
            model_name=config["retrieval"]["reranking"]["model_name"]
        )
    elif config["retrieval"]["reranking"]["enabled"]:
        retriever = ContextualCompressionRetriever(
            base_compressor=get_reranker(
                config["retrieval"]["reranking"]["provider"],
                model_name=config["retrieval"]["reranking"]["model_name"],
                top_n=config["retrieval"]["reranking"]["top_n"],
                api_key=api_key
            ),
            base_retriever=retriever
        )

    # Create history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    return history_aware_retriever

