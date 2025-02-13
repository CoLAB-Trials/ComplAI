import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langchain import hub
from typing import List
from langchain_openai import ChatOpenAI
import json
import time
from langchain.schema import HumanMessage
def get_text_chunks(text: str, chunk_size: int = None, chunk_overlap: int = None, method: str = "simple") -> list:
    """
    Splits the given text into chunks based on the specified method.
    Parameters:
    text (str): The text to be chunked.
    chunk_size (int, optional): The size of each chunk. Default is None.
    chunk_overlap (int, optional): The overlap between chunks. Default is None.
    method (str, optional): The method to use for chunking. Options are "simple", "recursive", 
                            "semantic", "agentic", and "contextual". Default is "simple".
    Returns:
    list: A list of text chunks.
    """
    
    if method == "simple":
        chunks = get_simple_text_chunks(text, chunk_size, chunk_overlap)
    elif method == "recursive":
        chunks = get_recursive_text_chunks(text, chunk_size, chunk_overlap)
    elif method == "semantic":
        chunks = get_semantic_text_chunks(text)
    elif method == "agentic":
        chunks = agentic_chunking(text)
    elif method == "contextual":
        chunks = get_contextual_chunks(text, chunk_size, chunk_overlap)

    return chunks


def get_simple_text_chunks(texts: list, chunk_size: int, chunk_overlap: int) -> list:
    """
    Splits the input text into overlapping chunks using a CharacterTextSplitter.

    Parameters:
    texts (list): The input texts to be split into chunks.
    chunk_size (int): The size of each chunk.
    chunk_overlap (int): The overlap between chunks.

    Returns:
    list: A list containing the text chunks.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_documents(texts)
    
    return chunks

def get_recursive_text_chunks(texts: list, chunk_size: int, chunk_overlap: int) -> list:
    """
    Splits the input text into overlapping chunks using a RecursiveCharacterTextSplitter.

    Parameters:
    texts (list): The input texts to be split into chunks.
    chunk_size (int): The size of each chunk.
    chunk_overlap (int): The overlap between chunks.

    Returns:
    list: A list containing the text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_documents(texts)
    
    return chunks

def get_semantic_text_chunks(texts: list) -> list:
    """
    Splits a list of text elements into semantic chunks using Hugging Face embeddings.

    This function initializes Hugging Face embeddings and uses a semantic chunker to split
    each text element into smaller, meaningful chunks based on semantic content. The function
    ensures that the embeddings utilize CUDA if available for faster processing.

    Args:
        texts (list): A list of text elements, where each element is expected to have a 
                      'page_content' attribute containing the text to be chunked.

    Returns:
        list: A list of semantic chunks extracted from the input texts.
    """
    
    device = "cuda" if torch.cuda.is_available() else "cpu"

    embeddings = HuggingFaceInstructEmbeddings(model_name="NeuML/pubmedbert-base-embeddings", model_kwargs={"device": device})
    chunks = []
    text_splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type='percentile', 
            #'standard_deviation',
            #'interquartile',
            #'gradient'
        #breakpoint_threshold_amount=90
    )
    chunks = text_splitter.split_documents(texts)
    return chunks

def get_contextual_chunks(texts: list, chunk_size: int, chunk_overlap: int) -> list:
    """
    Splits the input text into overlapping chunks using a RecursiveCharacterTextSplitter and provides contextual information for each chunk.

    Parameters:
    texts (list): The input texts to be split into chunks.
    chunk_size (int): The size of each chunk.
    chunk_overlap (int): The overlap between chunks.

    Returns:
    list: A list containing the text chunks with contextual information.
    """
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    final_chunks = []
    for text in texts:
        chunks = text_splitter.split_text(text.page_content)
        for chunk in chunks:
            
            DOCUMENT_CONTEXT_PROMPT = """
            <document>
            {doc_content}
            </document>
            """

            CHUNK_CONTEXT_PROMPT = """
            Here is the chunk we want to situate within the whole document
            <chunk>
            {chunk_content}
            </chunk>

            Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
            Answer only with the succinct context and nothing else.
            """
            """ anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
            response = anthropic_client.beta.prompt_caching.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.0,
                messages=[
                    {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text",
                                "text": DOCUMENT_CONTEXT_PROMPT.format(doc_content=text),
                                "cache_control": {"type": "ephemeral"} #we will make use of prompt caching for the full documents
                            },
                            {
                                "type": "text",
                                "text": CHUNK_CONTEXT_PROMPT.format(chunk_content=chunk),
                            },
                        ]
                    },
                ],
                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
            ) """
            chat = ChatOpenAI(
                model="gpt-4o-mini", 
                temperature=0.0
            )

            # Construct the prompts
            document_context_message = HumanMessage(
                content=DOCUMENT_CONTEXT_PROMPT.format(doc_content=text.page_content)
            )
            chunk_context_message = HumanMessage(
                content=CHUNK_CONTEXT_PROMPT.format(chunk_content=chunk)
            )

            # Send the messages to the GPT-4 model
            response = chat([document_context_message, chunk_context_message])
            final_chunks.append(f"{chunk}\n\n{response.content}")
    
    return final_chunks

def get_proposition_text_chunks(input_text):
    

    model_name = "chentong00/propositionizer-wiki-flan-t5-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    title = "PDF"
    section = ""
    
    propositions = []
    for n in range(len(input_text.iloc[1:,0])):
        content= input_text.iloc[n,0]
        input = f"Title: {title}. Section: {section}. Content: {content}"
        input_ids = tokenizer(input, return_tensors="pt").input_ids
        outputs = model.generate(input_ids.to(device), max_new_tokens=512)

        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        try:
            prop_list = json.loads(output_text)
            propositions.extend(prop_list)
            print(propositions)
        except:
            prop_list = []
            print("[ERROR] Failed to parse output text as JSON.")
    return propositions

def get_proposition_text_chunks_langchain(input_text, llm):

    obj = hub.pull("wfh/proposal-indexing")
    

    # You can explore the prompt template behind this by running the following:
    # obj.get_prompts()[0].messages[0].prompt.template

    # A Pydantic model to extract sentences from the passage
    class Sentences(BaseModel):
        sentences: List[str]

    extraction_llm = llm.with_structured_output(Sentences)


    # Create the sentence extraction chain
    extraction_chain = obj | extraction_llm
    propositions=[]
    for n in range(len(input_text)):
        content= input_text[n]
        # Test it out
        sentences = extraction_chain.invoke(content)
        if sentences is not None:
            propositions.extend(sentences.sentences)
        else:
            print("Warning: 'sentences' is None.")
        print(propositions)
        time.sleep(5)
    return propositions
    
        
        
class ChunkMeta(BaseModel):
    title: str = Field(description="The title of the chunk.")
    summary: str = Field(description="The summary of the chunk.")

def create_new_chunk(chunk_id, proposition, chunks, llm):
    summary_llm = llm.with_structured_output(ChunkMeta)

    summary_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Generate a new summary and a title based on the propositions.",
            ),
            (
                "user",
                "propositions:{propositions}",
            ),
        ]
    )

    summary_chain = summary_prompt_template | summary_llm

    chunk_meta = summary_chain.invoke(
        {
            "propositions": [proposition],
        }
    )

    chunks[chunk_id] = {
        "summary": chunk_meta.summary,
        "title": chunk_meta.title,
        "propositions": [proposition],
    }

    
def add_proposition(chunk_id, proposition, chunks, llm):
    summary_llm = llm.with_structured_output(ChunkMeta)

    summary_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "If the current_summary and title is still valid for the propositions return them."
                "If not generate a new summary and a title based on the propositions.",
            ),
            (
                "user",
                "current_summary:{current_summary}\n\ncurrent_title:{current_title}\n\npropositions:{propositions}",
            ),
        ]
    )

    summary_chain = summary_prompt_template | summary_llm

    chunk = chunks[chunk_id]

    current_summary = chunk["summary"]
    current_title = chunk["title"]
    current_propositions = chunk["propositions"]

    all_propositions = current_propositions + [proposition]

    chunk_meta = summary_chain.invoke(
        {
            "current_summary": current_summary,
            "current_title": current_title,
            "propositions": all_propositions,
        }
    )

    chunk["summary"] = chunk_meta.summary
    chunk["title"] = chunk_meta.title
    chunk["propositions"] = all_propositions


def find_chunk_and_push_proposition(proposition, chunks, llm):

    class ChunkID(BaseModel):
        chunk_id: int = Field(description="The chunk id.")

    allocation_llm = llm.with_structured_output(ChunkID)

    allocation_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You have the chunk ids and the summaries"
                "Find the chunk that best matches the proposition."
                "If no chunk matches, return a new chunk id."
                "Return only the chunk id.",
            ),
            (
                "user",
                "proposition:{proposition}" "chunks_summaries:{chunks_summaries}",
            ),
        ]
    )

    allocation_chain = allocation_prompt | allocation_llm

    chunks_summaries = {
        chunk_id: chunk["summary"] for chunk_id, chunk in chunks.items()
    }

    best_chunk_id = allocation_chain.invoke(
        {"proposition": proposition, "chunks_summaries": chunks_summaries}
    ).chunk_id
    print(best_chunk_id)
    if best_chunk_id not in chunks:
        best_chunk_id = create_new_chunk(best_chunk_id, proposition)
        return

    add_proposition(best_chunk_id, proposition)
    print(chunks)

def agentic_chunking(text):
    
    llm = ChatOpenAI(
        base_url="https://api.together.xyz/",
        api_key=os.environ["TOGETHER_API_KEY"],
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    )
    
    chunks={}

    # Get the text chunks
    text_chunks = get_text_chunks(text, 1000, 200, method="recursive")
    propositions = get_proposition_text_chunks_langchain(text_chunks, llm)
    
    for proposition in propositions:
        find_chunk_and_push_proposition(proposition, chunks, llm)
        
    return chunks
