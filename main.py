from langchain_core.messages import HumanMessage, SystemMessage
from langchain_utils.chunking_strategies import get_text_chunks
from utils_functions import setup_llm_pipeline, create_conversation_chain, curate_dataset, initialize_embedding_model
from langchain_utils.vectorstore_strategies import get_vectorstore
from langchain_utils.evaluation_strategies import ragas_evaluation_langchain, rag_triad_evaluation_langchain
from langchain_utils.retrieval_strategies import retriever
from utils.reading_data import get_pdf_text_from_folder, unstructured_pdf_reader
import argparse
import os
from langchain_together import ChatTogether
from langchain_community.vectorstores import faiss
from utils.config import load_config
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

#import langchain 
#langchain.debug = True
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["TORCH_USE_CUDA_DSA"] = "1"
def main(execution):
    
    config = load_config("config.yaml")
    
    embeddings = initialize_embedding_model()
    
    if os.path.exists("faiss_index_semantic"):
        vectorstore = faiss.FAISS.load_local("faiss_index_semantic", embeddings, allow_dangerous_deserialization=True)
    else:
        pdf_docs = '/mnt/c/Users/pc/Documents/complAI/Training materials for models'
        # Envokes a function that gets the pdf_text
        raw_text = get_pdf_text_from_folder(pdf_docs)
        #print(raw_text)
        # Get the text chunks
        text_chunks = get_text_chunks(raw_text, config["chunking"]["chunk_size"], config["chunking"]["chunk_overlap"], method=config["chunking"]["type"])
        # create vector store
        vectorstore = get_vectorstore(text_chunks, embeddings=embeddings)
    
    llm = setup_llm_pipeline()

    history_aware_retriever = retriever(llm, vectorstore, retriever_type=config["retrieval"]["type"], search_type=config["retrieval"]["search_type"], search_kwargs=config["retrieval"]["search_kwargs"])
    
    # create conversation chain
    conversation = create_conversation_chain(llm, history_aware_retriever)
    
    # Call the invoke method directly on the conversation chain
    template = """Rewrite the given question to make it more clear and relevant to the context of medical device regulation in the European Union.
        Expand on any terms or objects mentioned by providing detailed descriptions or examples.
        If any terms require clarification, include clear and concise explanations directly within the question.
        Avoid including elements that might influence or guide the direction of the response.
        Output only the revised question and nothing else, ending it with '**'.
        Question: {x} 
        Revised Question:"""
    rewrite_prompt = ChatPromptTemplate.from_template(template)
    def _parse(text):
        return text.strip('"').strip("**")
    rewriter = rewrite_prompt | llm | StrOutputParser() | _parse
    
    if execution == "interactive":
        chat_history = []
        file = open("questions.txt", "r")
        while True:
            content = file.readline()
            if not content:
                break
            new_question = rewriter.invoke({"x": HumanMessage(content="What is the classification of the following medical device:" + content)})
            #print(new_question)
            response = conversation.invoke({'input': new_question + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": chat_history})  # Adjust to pass the input as expected
            chat_history.extend([HumanMessage(content=new_question), SystemMessage(content=response["answer"])])
            print(response['answer'])
            #print(response['context'])
    elif execution == "eval":
        llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",)
        ragas_evaluation_langchain(conversation, llm, embeddings)
        rag_triad_evaluation_langchain(conversation)
    elif execution == "curate_dataset":
        curate_dataset(text_chunks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the script in either interactive or evaluation mode.")
    parser.add_argument("--execution", type=str, choices=["interactive", "eval", "curate_dataset"], required=True,
                        help="Choose execution mode: 'interactive' for chat, 'eval' for evaluation functions.")
    args = parser.parse_args()
    main(args.execution)
    main()