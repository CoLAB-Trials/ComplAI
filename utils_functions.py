from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_groq import ChatGroq
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_together import TogetherEmbeddings
from utils.prompts import REGULATORY_EXPERT, MD_CLASS, PROMPT_REWRITER, TEXT_IMPROVER
import os 
    
def initialize_embedding_model(provider: str = "HuggingFace", model: str = "hkunlp/instructor-xl", api_key = os.environ.get("OPENAI_API_KEY")) -> object:
    """
    Initialize an embedding model from a specified provider.
    Parameters:
    provider (str): The provider of the embedding model. Options are "HuggingFace", "OpenAI", and "TogetherAI".
                    Default is "HuggingFace".
    model (str): The specific model to use from the provider. Default is "hkunlp/instructor-xl".
    Returns:
    embeddings: An instance of the embedding model initialized with the specified provider and model.
    """
    
    # Initialize Hugging Face embeddings and ensure it uses CUDA if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if provider == "HuggingFace":
        embeddings = HuggingFaceEmbeddings(model_name=model, model_kwargs={"device": device})
    elif provider == "OpenAI":
        embeddings = OpenAIEmbeddings(model=model, api_key=api_key)
    elif provider == "TogetherAI":
        embeddings = TogetherEmbeddings(model=model)
    
    return embeddings

def setup_llm_pipeline(model_name: str = "meta-llama/Llama-3.2-3B-Instruct", temperature: float = 0) -> HuggingFacePipeline:
    """
    Set up a language model pipeline using the specified model and temperature.
    Args:
        model_name (str): The name or path of the pre-trained model to use. Default is "meta-llama/Llama-3.2-3B-Instruct".
        temperature (float): The temperature to use for text generation. Default is 0.
    Returns:
        HuggingFacePipeline: A pipeline object for text generation using the specified model and tokenizer.
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    device = 0 if torch.cuda.is_available() else -1
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to("cuda" if device == 0 else "cpu")

    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=temperature,
        return_full_text=False,
        pad_token_id=tokenizer.eos_token_id,
        device=device,
        max_new_tokens=512,
    )

    return HuggingFacePipeline(pipeline=text_pipeline)

def llm_initialization(provider: str = "HuggingFace", model: str = "meta-llama/Llama-3.2-3B-Instruct", temperature: float = 0, api_key = os.environ.get("OPENAI_API_KEY")) -> object:
    """
    Initialize a language model (LLM) based on the specified provider and model.
    Parameters:
    provider (str): The provider of the language model. Options are "HuggingFace", "OpenAI", "TogetherAI", and "Groq". Default is "HuggingFace".
    model (str): The specific model to use. Default is "meta-llama/Llama-3.2-3B-Instruct".
    temperature (float): The temperature setting for the model, which controls the randomness of the output. Default is 0.
    Returns:
    llm: An initialized language model object based on the specified provider and model.
    """
    if provider == "HuggingFace":
        llm = setup_llm_pipeline(model_name=model, temperature=temperature)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=model, max_retries=2, api_key=api_key)
    elif provider == "TogetherAI":
        llm = ChatTogether(model=model, temperature=temperature, max_retries=2)
    elif provider == "Groq":
        llm = ChatGroq(model=model, temperature=temperature, max_retries=2)
    
    return llm

def create_conversation_chain(llm: object, history_aware_retriever: object, config: dict) -> object:
    """
    Create a conversation chain based on the provided language model, retriever, and configuration.
    Args:
        llm (object): The language model to be used for generating responses.
        history_aware_retriever (object): The retriever that is aware of the conversation history.
        config (dict): Configuration dictionary containing system settings.
    Returns:
        object: A conversation chain that can handle question-answering with context retrieval.
    Raises:
        KeyError: If the 'system' key is not found in the config dictionary.
    Example:
        config = {
            'system': 'regulatory_expert'
        }
        conversation_chain = create_conversation_chain(llm, history_aware_retriever, config)
    """
    
    if config['system'] == "regulatory_expert":
        system_prompt = REGULATORY_EXPERT
    elif config['system'] == "md_class":
        system_prompt = MD_CLASS  
        
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    conversation_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return conversation_chain

def query_rewriter(llm: object, user_question: str) -> str:
    """
    Rewrites a user's question using a language model.
    This function takes a language model (llm) and a user's question, then rewrites the question
    using a predefined prompt template. The rewritten question is returned.
    Args:
        llm: The language model to use for rewriting the question.
        user_question (str): The original question from the user.
    Returns:
        str: The rewritten question.
    """

    template = PROMPT_REWRITER
    rewrite_prompt = ChatPromptTemplate.from_template(template)
    def _parse(text):
        return text.strip('"').strip("**")
    rewriter = rewrite_prompt | llm | StrOutputParser() | _parse
    new_question = rewriter.invoke({"x": HumanMessage(content=user_question)})
    
    return new_question

def curate_dataset(llm: object, input_text: list[str]) -> list[str]:
    """
    Curate a dataset by improving the input text using a language model.
    This function takes a language model (llm) and a list of input text, then improves each text
    using a predefined prompt template. The improved texts are returned as a dataset.
    Args:
        llm: The language model to use for improving the text.
        input_text (list of str): A list of text strings to be improved.
    Returns:
        list of str: A list of improved text strings.
    """
    
    template = TEXT_IMPROVER
    rewrite_prompt = ChatPromptTemplate.from_template(template)
    rewriter = rewrite_prompt | llm
    
    dataset = []
    for content in input_text:
        rewritten_text = rewriter.invoke({"content": content})
        dataset.append(rewritten_text)
    
    return dataset

def clustering_chunks(vectorstore):
    """
    Cluster document chunks based on their embeddings using Milvus ANN search.

    Args:
        vectorstore: The vector store containing document vectors.
        embeddings: The embeddings model to generate vector representations of texts.

    Returns:
        list: A list of text clusters, each cluster containing concatenated texts.
    """
    # Get all vectors and texts
    results = vectorstore.similarity_search_with_score("", k=16384)  # Get all documents
    texts = [doc[0].page_content for doc in results]

    # Perform clustering using Milvus ANN search
    max_cluster_size = 10
    clusters = []
    visited = set()

    for i, text in enumerate(texts):
        if i in visited:
            continue
        
        # Search for nearest neighbors using Milvus
        similar_docs = vectorstore.similarity_search_with_score(text, k=max_cluster_size)
        
        # Get indices of similar documents
        neighbor_indices = [texts.index(doc.page_content) for doc, _ in similar_docs if texts.index(doc.page_content) not in visited]
        
        # Add the cluster
        clusters.append(neighbor_indices)
        
        # Mark as visited
        visited.update(neighbor_indices)

    # Map clusters to texts
    text_clusters = ["\n".join(texts[idx] for idx in cluster) for cluster in clusters]
            
    return text_clusters