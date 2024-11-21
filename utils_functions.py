import os
import re
from PyPDF2 import PdfReader
import time
from langchain_openai import ChatOpenAI
import torch  # to check for CUDA
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import pandas as pd
from langchain_community.document_loaders import BSHTMLLoader, UnstructuredHTMLLoader
from langchain_community.embeddings import HuggingFaceInstructEmbeddings

def read_html():
    loader = UnstructuredHTMLLoader("/mnt/c/Users/pc/Documents/complAI/Training materials for models/MDCG Guidance Documents/Dispositivos médicos - INFARMED, I.P..html")
    data = loader.load()
    data
    
def initialize_embedding_model(provider="HuggingFace", model="hkunlp/instructor-xl"):
        
    # Initialize Hugging Face embeddings and ensure it uses CUDA if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if provider == "HuggingFace":
        embeddings = HuggingFaceInstructEmbeddings(model_name=model, model_kwargs={"device": device})
    elif provider == "OpenAI":
        embeddings = HuggingFaceInstructEmbeddings(model_name=model, model_kwargs={"device": device})
    elif provider == "TogetherAI":
        embeddings = HuggingFaceInstructEmbeddings(model_name=model, model_kwargs={"device": device})
    
    return embeddings

def setup_llm_pipeline(model_name="meta-llama/Llama-3.2-3B-Instruct"):
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float16, trust_remote_code=True
    ).to("cuda" if torch.cuda.is_available() else "cpu")
    
    generation_config = GenerationConfig.from_pretrained(model_name)
    generation_config.max_new_tokens = 512
    generation_config.temperature = 0.7
    generation_config.do_sample = True
    generation_config.repetition_penalty = 1.15
    
    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        generation_config=generation_config,
        return_full_text=False,
        pad_token_id=tokenizer.eos_token_id,
        device = 0
    )
    
    llm = HuggingFacePipeline(pipeline=text_pipeline)
    return llm

def create_conversation_chain(llm, history_aware_retriever):
    
    ### Answer question ###
    system_prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. Respond concisely only to the question asked which will be after \"Human:\"."
        "If there is not sufficient context say \"No sufficient context\" <|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>"
        "\n\n"
        "{context}"
        "\n\n"
    )
    
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

def curate_dataset(input_text):

    llm = ChatOpenAI(
        base_url="https://api.together.xyz/",
        api_key=os.environ["TOGETHER_API_KEY"],
        model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
    )

    # Create the sentence extraction chain
    extraction_chain = llm
    

    for n in range(len(input_text)):
        dataset = []
        content= input_text[n]
        # Test it out
        print(content)
        messages = [
            {"role": "user", "content": f"""I have a text below that I would like you to analyze and improve:

        <text> {content} </text>

        Punctuation: Remove any unnecessary punctuation.
        Relevance: Evaluate if all content is relevant, omitting any parts that may detract from the main message.
        Rewrite: Rewrite the text to improve clarity, flow, or tone as needed.
        Conciseness: Aim for conciseness without sacrificing meaning or detail.
        Grammar and Syntax: Ensure the grammar and syntax are correct.
        Please present only the final revised text, with no explanation or justification. Do not put anything before your answer, not even 'Here is the revised text:'
        Here is the revised text:"""}]
        #Other prompt possibility
        
        sentences = extraction_chain.invoke(messages)
        time.sleep(1)
        dataset.append(sentences.content)
        print(dataset)
        df = pd.DataFrame(list(dataset), columns=['text'])
        df.to_csv('curated_dataset.csv', mode='a', index=False, header=False)
        