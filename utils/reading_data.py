from unstructured.partition.pdf import partition_pdf
import os
import re
from PyPDF2 import PdfReader
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import pipeline
from llama_parse import LlamaParse
import nest_asyncio
from langchain_community.document_loaders import DirectoryLoader
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader

def reader(folder_path: str = '/mnt/c/Users/pc/Documents/complAI/Training materials for models/', reader= "PyPDF", file_type = "PDF") -> list:
    
    if reader == "PyMuPDF":
        processed_texts = pymupdf_reader_langchain(folder_path)
    elif reader == "PyPDF":
        processed_texts = pypdf_reader_langchain(folder_path)
    elif reader == "Unstructured":
        processed_texts = unstructured_reader_langchain(folder_path)
    elif reader == "LlamaParse":
        if file_type == "PDF":
            processed_texts = load_llama_parse_output(folder_path)
        elif file_type == "Markdown":
            processed_texts = read_markdown_folder_and_split(folder_path)
    
    return processed_texts
    
        
def get_pdf_text_from_folder(folder_path: str = '/mnt/c/Users/pc/Documents/complAI/Training materials for models/', normalization: bool = True) -> list:
    """
    Extracts and processes text from all PDF files in a specified folder.

    Args:
        folder_path (str): The path to the folder containing PDF files. Defaults to '/mnt/c/Users/pc/Documents/complAI/Training materials for models/'.
        normalization (bool): If True, normalizes the text by removing non-alphanumeric characters. Defaults to True.

    Returns:
        list: A list of Document objects, each containing the processed text and metadata with the source filename.
    """
    processed_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            pdf_reader = PdfReader(pdf_path)
            document_parts = [
                re.sub('[^a-zA-Z0-9\s]', '', page.extract_text()) if normalization else page.extract_text()
                for page in pdf_reader.pages
            ]
            processed_texts.append(Document(page_content="\n\n".join(document_parts), metadata={"source": filename}))
    return processed_texts

def unstructured_reader_langchain(folder_path: str = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/") -> list:
    """
    Read all PDF files in a folder using UnstructuredPDFLoader and return their contents.
    
    Args:
        folder_path (str): Path to folder containing PDF files.
        
    Returns:
        list: List of Document objects containing PDF file contents.
    """
    processed_texts: list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path: str = os.path.join(folder_path, filename)
            loader = UnstructuredPDFLoader(pdf_path)
            pages: list = loader.load()
            processed_texts.extend(pages)
    return processed_texts

def txt_reader_langchain(folder_path: str = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/") -> list:
    """
    Read all PDF files in a folder using UnstructuredPDFLoader and return their contents.
    
    Args:
        folder_path (str): Path to folder containing PDF files.
        
    Returns:
        list: List of Document objects containing PDF file contents.
    """
    processed_texts: list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            pdf_path: str = os.path.join(folder_path, filename)
            loader = TextLoader(pdf_path)
            pages: list = loader.load()
            print(pages)
            processed_texts.extend(pages)
    return processed_texts


def pymupdf_reader_langchain(folder_path: str = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/") -> list:
    """
    Read all PDF files in a folder using PyMuPDFLoader and return their contents.
    
    Args:
        folder_path (str): Path to folder containing PDF files.
        
    Returns:
        list: List of Document objects containing PDF file contents.
    """
    processed_texts: list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path: str = os.path.join(folder_path, filename)
            loader = PyMuPDFLoader(pdf_path)
            pages: list = loader.load()
            processed_texts.extend(pages)
    return processed_texts

def pypdf_reader_langchain(folder_path: str = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/") -> list:
    """
    Read all PDF files in a folder using PyPDFLoader and return their contents.
    
    Args:
        folder_path (str): Path to folder containing PDF files.
        
    Returns:
        list: List of Document objects containing PDF file contents.
    """
    processed_texts: list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path: str = os.path.join(folder_path, filename)
            loader = PyPDFLoader(pdf_path)
            pages: list = loader.load()
            processed_texts.extend(pages)
    return processed_texts
 
def llama_parse_reader(folder_path: str = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/") -> None:
    """
    Parses PDF files in a specified folder using LlamaParse and saves the output as markdown files.

    Args:
        folder_path (str): Path to the folder containing PDF files. Defaults to "/mnt/c/Users/pc/Documents/complAI/Training materials for models/".
    """
    nest_asyncio.apply()
    parser = LlamaParse(result_type="markdown")

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            documents = parser.load_data(os.path.join(folder_path, file))
            output_path = os.path.join(folder_path, f"{os.path.splitext(file)[0]}.md")
            with open(output_path, 'w') as f:
                for doc in documents:
                    f.write(doc.text + '\n')
                    
def load_llama_parse_output(folder_path: str = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/") -> list:
    """
    Loads and parses markdown files from a specified directory.

    This function uses the DirectoryLoader to load all markdown files
    from the given folder path. It returns the loaded documents.

    Args:
        folder_path (str): The path to the directory containing the markdown files.
                            Defaults to "/mnt/c/Users/pc/Documents/complAI/Training materials for models/".

    Returns:
        list: A list of documents loaded from the specified directory.
    """

    loader = DirectoryLoader(folder_path, glob="**/*.md", show_progress=True)
    documents = loader.load()
    return documents

def read_markdown_folder_and_split(folder_path = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/"):
    """
    Read all markdown files in a folder and return their contents split by sections using langchain
    
    Args:
        folder_path (str): Path to folder containing markdown files
        
    Returns:
        list: List of langchain Document objects containing markdown file contents split by sections
    """
    
    headers_to_split_on = [
        ("#", "Header_1"),
        ("##", "Header_2"),
        ("###", "Header_3"),
        ("####", "Header_4"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
    markdown_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                markdown_content = file.read()

            splits = markdown_splitter.split_text(markdown_content)
            for split in splits:
                split.metadata['source'] = filename
                markdown_files.append(split)
    
    required_headers = {"Header_1", "Header_2", "Header_3", "Header_4"}

    def ensure_headers(doc: Document) -> Document:
        for header in required_headers:
            doc.metadata.setdefault(header, "")
        return doc
    
    return [ensure_headers(doc) for doc in markdown_files]

def processing_images_tables(folder_path = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/"):
    """
    Process PDFs to extract and analyze images and tables.
    Args:
        folder_path (str): The path to the folder containing PDF files to be processed. 
                           Defaults to "/mnt/c/Users/pc/Documents/complAI/Training materials for models/".
    Returns:
        list: A list of processed texts extracted from the PDFs, including summaries of tables and descriptions of images.
    """    
    # Set environment variables for image extraction
    os.environ['EXTRACT_IMAGE_BLOCK_CROP_HORIZONTAL_PAD'] = '200'
    os.environ['EXTRACT_IMAGE_BLOCK_CROP_VERTICAL_PAD'] = '100'
    
    # Initialize models
    image_model = AutoModelForCausalLM.from_pretrained(
        "vikhyatk/moondream2", 
        trust_remote_code=True,
        revision="2024-08-26"
    )
    image_tokenizer = AutoTokenizer.from_pretrained(
        "vikhyatk/moondream2",
        revision="2024-08-26"
    )

    device = 0 if torch.cuda.is_available() else -1
    table_pipeline = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-1B-Instruct",
        torch_dtype=torch.bfloat16,
        device=device,
    )

    processed_texts = []
    
    for filename in os.listdir(folder_path):
        if not filename.endswith(".pdf"):
            continue
            
        print(f"Processing {filename}")
        
        # Extract PDF elements
        pdf_elements = partition_pdf(
            filename=os.path.join(folder_path, filename),
            strategy="hi_res",
            extract_images_in_pdf=True,
            infer_table_structure=True,
            chunking_strategy="by_title",
            max_characters=1000,
            new_after_n_chars=900,
            combine_text_under_n_chars=500,
        )

        document_parts = []
        
        for element in pdf_elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                # Process table
                table_summary = table_pipeline(
                    [
                        {"role": "system", "content": "You are an experienced interpreter of tables written in HTML. Present a summary of the information you can extract from the table"},
                        {"role": "user", "content": element.metadata.text_as_html},
                    ],
                    max_new_tokens=256,
                )[0]["generated_text"][-1]['content']
                document_parts.append(table_summary)
            else:
                # Process other elements (text and images)
                for sub_element in element.metadata.orig_elements:
                    if "unstructured.documents.elements.Image" in str(type(sub_element)):
                        image = Image.open(sub_element.metadata.image_path)
                        enc_image = image_model.encode_image(image)
                        image_desc = image_model.answer_question(enc_image, "Describe this image detailedly.", image_tokenizer)
                        document_parts.append(str(image_desc))
                    else:
                        document_parts.append(str(sub_element))
        
        processed_texts.append("\n\n".join(document_parts))
        
    return processed_texts