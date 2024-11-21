import os
import torch  # to check for CUDA
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
import pandas as pd
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline, AutoModelForSeq2SeqLM
import torch
from langchain import hub
from typing import List
from langchain_openai import ChatOpenAI
import json
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
import time
from utils.reading_data import get_pdf_text_from_folder

def get_text_chunks(text, chunk_size=None, chunk_overlap=None, method="simple"):
    
    if method == "simple":
        chunks = get_simple_text_chunks(text, chunk_size, chunk_overlap)
    elif method == "recursive":
        chunks = get_recursive_text_chunks(text, chunk_size, chunk_overlap)
    elif method == "semantic":
        chunks = get_semantic_text_chunks(text)
    elif method == "agentic":
        chunks = agentic_chunking(text)

    return chunks


def get_simple_text_chunks(text, chunk_size, chunk_overlap):
    """
    Splits the input text into overlapping chunks using a CharacterTextSplitter and returns the result as a DataFrame.

    Parameters:
    text (str): The input text to be split into chunks.

    Returns:
    pd.DataFrame: A DataFrame containing the text chunks in a column named 'CharacterTextSplitter'.
    """
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    return chunks

def get_recursive_text_chunks(text, chunk_size, chunk_overlap):
    """
    Splits the input text into overlapping chunks using a RecursiveCharacterTextSplitter and returns the result as a DataFrame.

    Parameters:
    text (str): The input text to be split into chunks.

    Returns:
    pd.DataFrame: A DataFrame containing the text chunks in a column named 'RecursiveCharacterTextSplitter'.
    """
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    return chunks
 
def get_semantic_text_chunks(text):
    # Initialize Hugging Face embeddings and ensure it uses CUDA if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(device)
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device": device})
    text_splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type=#'percentile', 
            'standard_deviation',
            #'interquartile',
            #'gradient'
        breakpoint_threshold_amount=0.1
    )
    chunks = text_splitter.split_text(text)
    
    return chunks



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
