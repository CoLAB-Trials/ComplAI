from langchain_core.messages import HumanMessage, SystemMessage
from langchain_utils.chunking_strategies import get_text_chunks
from utils_functions import create_conversation_chain, curate_dataset, initialize_embedding_model, query_rewriter, llm_initialization, clustering_chunks
from langchain_utils.vectorstore_strategies import get_vectorstore, load_vectorstore, vectorstore_existence_check
from langchain_utils.evaluation_strategies import ragas_evaluation_langchain, rag_triad_evaluation_langchain, rag_checker
from langchain_utils.retrieval_strategies import retriever
from utils.reading_data import get_pdf_text_from_folder, reader, txt_reader_langchain
import os
from utils.config import load_config
import csv
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import json
#import langchain 
#langchain.debug = True
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["TORCH_USE_CUDA_DSA"] = "1"

class Classification(BaseModel):
    classification: str = Field(..., description="The classification of the device. The options are 'Class I', 'Class IIa', 'Class IIb', 'Class III'.")
    
def main():
    config = load_config("config.yaml")
    llm_rewriting = llm_initialization(model=config["models"]["rewriting"]["name"], provider=config["models"]["rewriting"]["provider"], temperature=config["models"]["rewriting"]["temperature"])
    llm_generation = llm_initialization(model=config["models"]["generation"]["name"], provider=config["models"]["generation"]["provider"], temperature=config["models"]["generation"]["temperature"])
    embeddings = initialize_embedding_model()
    
    # Load or create vectorstore
    if vectorstore_existence_check(config) and config["vectorstore"]["new"] == False:
        vectorstore = load_vectorstore(embeddings, config, llm=llm_generation)
    else:
        raw_text = reader(config["pdf_path"])
        if config["reader"]["file_type"] == "PDF": 
            text_chunks = get_text_chunks(raw_text, config["chunking"]["chunk_size"], 
                                    config["chunking"]["chunk_overlap"], 
                                    method=config["chunking"]["type"])
        elif config["reader"]["file_type"] == "Markdown":
            text_chunks = raw_text
        print(text_chunks)
        vectorstore = get_vectorstore(text_chunks, embeddings=embeddings, config=config, llm=llm_generation)

        if config["data"]["rewriting"] or config["data"]["clustering"]:
            if config["data"]["clustering"]:
                text_chunks = clustering_chunks(vectorstore=vectorstore, embeddings=embeddings)
            if config["data"]["rewriting"]:
                text_chunks = curate_dataset(llm_rewriting, text_chunks)
            vectorstore = get_vectorstore(text_chunks, embeddings=embeddings, config=config, llm=llm_generation)


    # Setup conversation chain
    llm_retrieve = llm_initialization(model=config["models"]["retrieve"]["name"], provider=config["models"]["retrieve"]["provider"], temperature=config["models"]["retrieve"]["temperature"])
    retriever_chain = retriever(llm_retrieve, vectorstore, config=config, embeddings=embeddings)
    
    conversation = create_conversation_chain(llm_generation, retriever_chain, config)
    chat_history = []
    # Handle different execution modes
    if config["mode"] == "interactive":
        
        while True:
            question = input("Please enter your question: ")
            
            if question.lower() == 'q':
                print("Exiting the conversation. Goodbye!")
                break
            
            query = query_rewriter(llm_rewriting, question) if config["rewrite_query"] else question
            response = conversation.invoke({
                'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
                'chat_history': chat_history
            })
            #chat_history.extend([
            #    HumanMessage(content=question),
            #    SystemMessage(content=response["answer"])
            #])
            print(response["answer"])
    elif config["mode"] == "test_md_class":
        with open("questions.txt", "r") as file:
            questions = [line.strip() for line in file]

        answers = []
        for query in questions:
            for _ in range(1):  # Repeat 3 times for each query
                response = conversation.invoke({
                    'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
                    'chat_history': chat_history
                })
                #outputs.append(response["answer"])
                #print(query)
                #print(response['answer'])
                # Define the schema and the prompt template
                schema = Classification.model_json_schema()

                template = """Use the following answer to extract the medical device classification based on the schema passed. Output should follow the pattern defined in schema.
                No verbose should be present. Output should follow the pattern defined in schema and the output should be in json format only so that it can be directly used with json.loads():
                {context}
                schema: {schema}
                """
                rag_prompt_custom = PromptTemplate.from_template(template)
                llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
                # Use the page content directly within the prompt template
                prompt = rag_prompt_custom.format(context=response["answer"], schema=schema)

                # Execute the LLM with the formatted prompt
                raw_output = llm.predict(prompt)
                cleaned_output = raw_output.replace("json", "").replace("```", "").strip()
                print(response["answer"])
                print(json.loads(cleaned_output))
                answers.append([json.loads(cleaned_output)["classification"]])
         
        with open("output_2.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(answers)

    elif config["mode"] == "eval":
        llm_eval = llm_initialization(model=config["models"]["eval"]["name"], provider=config["models"]["eval"]["provider"], temperature=config["models"]["eval"]["temperature"])
        #ragas_evaluation_langchain(conversation, llm_eval, embeddings, llm_rewriting=llm_rewriting, rewrite=config["rewrite_query"], "eval_with_reference")
        #rag_triad_evaluation_langchain(conversation, llm_rewriting=llm_rewriting, rewrite=config["rewrite_query"])
        rag_checker(conversation, "gpt-4o-mini", llm_rewriting=llm_rewriting, rewrite=config["rewrite_query"])

    return

if __name__ == "__main__":
    main()