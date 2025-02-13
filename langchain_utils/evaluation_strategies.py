from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import (
    ResponseRelevancy,
    Faithfulness,
    LLMContextPrecisionWithoutReference,
    LLMContextRecall,
    NoiseSensitivity,
)
from ragas import evaluate
from datasets import Dataset
from ragas.run_config import RunConfig
from trulens.apps.langchain import TruChain
from trulens.core import TruSession, Feedback, Select
from trulens.dashboard import run_dashboard
import pandas as pd
import csv
import json
from ragchecker import RAGResults, RAGChecker
from ragchecker.metrics import all_metrics
from trulens.providers.litellm import LiteLLM
from trulens.providers.openai import OpenAI
import numpy as np
from typing import List, Dict, Any, Optional
from utils_functions import query_rewriter

def rag_checker(conversation: Any, llm: str, llm_rewriting, rewrite: bool = False) -> None:
    """
    Evaluates the responses of a conversation model against a set of reference answers.
    Args:
        conversation (Any): The conversation model to be evaluated.
        llm (str): The name of the language model used for evaluation.
    Returns:
        None
    The function performs the following steps:
    1. Reads questions and reference answers from a CSV file named "questions.csv".
    2. Processes the responses from the conversation model for each question.
    3. Saves the results, including the query, ground truth answer, model response, and retrieved context, to a JSON file named "output.json".
    4. Evaluates the results using the RAGChecker and prints the evaluation results.
    """
    # Read questions and references from CSV
    with open("questions.csv", "r", encoding="utf-8-sig") as csvfile:
        data = list(csv.DictReader(csvfile))
        questions = [row['question'] for row in data]
        references = [row['answer'] for row in data]

    # Process responses
    chat_history = []
    results = []
    
    for i, (query, reference) in enumerate(zip(questions, references)):
        query = query_rewriter(llm_rewriting, query) if rewrite else query
        response = conversation.invoke({
            'input': f"{query}\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
            'chat_history': chat_history
        })
        
        # Create result entry
        results.append({
            "query_id": f"{i:03}",
            "query": query,
            "gt_answer": reference,
            "response": response['answer'],
            "retrieved_context": [
                {"doc_id": f"doc_{j:03}", "text": doc.page_content}
                for j, doc in enumerate(response['context'])
            ]
        })

    # Save results to JSON
    output_file = "output.json"
    with open(output_file, "w") as f:
        json.dump({"results": results}, f, indent=3)

    # Evaluate results
    with open(output_file) as fp:
        rag_results = RAGResults.from_json(fp.read())

    evaluator = RAGChecker(
        extractor_name=llm,
        checker_name=llm,
        batch_size_extractor=32,
        batch_size_checker=32
    )

    evaluator.evaluate(rag_results, all_metrics)
    print(rag_results)
    import pdb
    pdb.set_trace()
    

def ragas_evaluation_langchain(conversation: Any, llm: str, embeddings: Any, llm_rewriting, rewrite: bool = False, eval_method: str = "eval_without_reference") -> None:
    """
    Evaluate a conversation using the RAG evaluation strategy with Langchain.

    Args:
        conversation: The conversation object to be evaluated.
        llm: The language model used for evaluation.
        embeddings: The embeddings model used for evaluation.
        eval_method (str): The evaluation method to use. Options are "eval_with_reference" or "eval_without_reference".

    Returns:
        None
    """
    questions: List[str] = []
    references: List[str] = []
    chat_history: List[str] = []
    answers: List[str] = []
    contexts: List[List[str]] = []

    if eval_method == "eval_with_reference":
        # Read the CSV file
        with open("questions.csv", "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                questions.append(row['question'])
                references.append(row['answer'])

        # Process each question with its corresponding reference text
        for query, reference in zip(questions, references):
            response = conversation.invoke({'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": chat_history})
            answers.append(response['answer'])
            contexts.append(["\n\n".join([doc.page_content for doc in response['context']])])

        data: Dict[str, List[Any]] = {
            "question": questions,
            "reference": references,
            "answer": answers,
            "contexts": contexts
        }
        metrics: List[Any] = [
            Faithfulness(),
            ResponseRelevancy(),
            LLMContextRecall(),
            NoiseSensitivity(),
        ]

    elif eval_method == "eval_without_reference":
        # Read questions from text file
        with open("questions.txt", "r") as file:
            questions = [line.strip() for line in file]

        # Process each question
        for query in questions:
            query = query_rewriter(llm_rewriting, query) if rewrite else query
            response = conversation.invoke({'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": chat_history})
            answers.append(response['answer'])
            contexts.append(["\n\n".join([doc.page_content for doc in response['context']])])

        data = {
            "question": questions,
            "answer": answers,
            "contexts": contexts
        }
        metrics = [
            Faithfulness(),
            ResponseRelevancy(),
            LLMContextPrecisionWithoutReference(),
        ]

    wrapped_llm = LangchainLLMWrapper(llm)
    wrapped_embeddings = LangchainEmbeddingsWrapper(embeddings)

    # Convert dict to dataset
    dataset = Dataset.from_dict(data)
    result = evaluate(
        dataset=dataset,
        llm=wrapped_llm,
        embeddings=wrapped_embeddings,
        metrics=metrics,
        run_config=RunConfig(max_workers=2, timeout=5000),
    )

    print(result)
    pd.set_option('display.max_columns', None)
    df = result.to_pandas()
    print(df)
    
def rag_triad_evaluation_langchain(conversation, llm_rewriting, rewrite: bool = False, provider: str = "OpenAI", model_engine: str = "gpt-4o-mini") -> None:
    """
    Evaluate a conversation using the RAG triad evaluation strategy with Langchain.

    Args:
        conversation: The conversation object to be evaluated.
        provider (str): The provider to use for evaluation. Options are "OpenAI" or "LiteLLM".
        model_engine (str): The model engine to use for the provider.

    Returns:
        None
    """
    session = TruSession()
    session.reset_database()

    if provider == "OpenAI":
        provider_instance = OpenAI(model_engine=model_engine)
    elif provider == "LiteLLM":
        provider_instance = LiteLLM(model_engine=model_engine)
    else:
        raise ValueError("Unsupported provider. Choose either 'OpenAI' or 'LiteLLM'.")

    context_selection = Select.RecordCalls.bound.first.mapper.steps__.context.bound.default.last
    #context_selection = TruChain.select_context(conversation)

    f_groundedness = (
        Feedback(provider_instance.groundedness_measure_with_cot_reasons, name="Groundedness")
        .on(context_selection.collect())
        .on(Select.Record.app.bound.last.mapper.steps__.answer.bound.last.invoke.rets)
    )

    f_context_relevance = (
        Feedback(provider_instance.context_relevance_with_cot_reasons, name="Context Relevance")
        .on_input()
        .on(context_selection)
        .aggregate(np.mean)
    )

    f_relevance = (
        Feedback(provider_instance.relevance_with_cot_reasons, name="Answer Relevance")
        .on_input()
        .on(Select.Record.app.bound.last.mapper.steps__.answer.bound.last.invoke.rets)
    )

    tru_rag = TruChain(
        conversation,
        app_name="RAG",
        app_version="base",
        feedbacks=[f_groundedness, f_context_relevance, f_relevance],
    )

    with open("questions.txt", "r") as file:
        questions = [line.strip() for line in file]

    chat_history = []

    for query in questions:
        with tru_rag as recording:
            query = query_rewriter(llm_rewriting, query) if rewrite else query
            conversation.invoke(
                {'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": chat_history}
            )

    run_dashboard(session)
