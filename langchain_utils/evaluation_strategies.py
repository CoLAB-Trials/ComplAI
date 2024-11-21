from langchain_together import Together
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import (
    ResponseRelevancy,
    Faithfulness,
)
from ragas import evaluate
from datasets import Dataset
from ragas.run_config import RunConfig
from trulens.apps.langchain import TruChain
from trulens.core import TruSession, Feedback, Select
from trulens.providers.huggingface import Huggingface
from trulens.dashboard import run_dashboard
import numpy as np

def ragas_evaluation_langchain(conversation, llm, embeddings):
    
    file = open("questions.txt", "r")
    questions = []

    while True:
        content = file.readline()
        if not content:
            break
        questions.append(content.strip())  # Using strip() to remove any newline characters

    file.close()
    
    chat_history = []
    answers = []
    contexts = []
    for query in questions:
        response = conversation.invoke({'input': query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": chat_history})
        answers.append(response['answer'])
        contexts.append(["\n\n".join([doc.page_content for doc in response['context']])])

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts
    }
    wrapped_llm = LangchainLLMWrapper(llm)
    wrapped_embeddings = LangchainEmbeddingsWrapper(embeddings)
    # Convert dict to dataset
    dataset = Dataset.from_dict(data)  
    result = evaluate(
        dataset=dataset,
        llm=wrapped_llm,
        embeddings=wrapped_embeddings,
        metrics=[
            #Faithfulness(),
            ResponseRelevancy(),
        ],
        run_config=RunConfig(max_workers=2, timeout=5000),
    )
    print(result)
    
def rag_triad_evaluation_langchain(conversation):
    
    session = TruSession()
    session.reset_database()
    
    from trulens.providers.litellm import LiteLLM
    import litellm
    from trulens.apps.llamaindex.tru_llama import TruLlama

    litellm.set_verbose= True
    provider = LiteLLM(model_engine="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

    # select context to be used in feedback. the location of context is app specific.
    #context_selection = TruChain.select_context(conversation)
    context_selection = Select.RecordCalls.bound.first.mapper.steps__.context.bound.default.last

    import numpy as np

    f_groundedness = (
        Feedback(provider.groundedness_measure_with_cot_reasons,
                name="Groundedness")
        .on(context_selection.collect())
        .on_output()
    )

    f_context_relevance = (
        Feedback(provider.context_relevance_with_cot_reasons,
                name="Context Relevance")
        .on_input()
        .on(context_selection)
        .aggregate(np.mean)
    )

    f_relevance = (
        Feedback(provider.relevance,
                name="Relevance")
        .on_input_output()
    )

    f_conciseness = (
        Feedback(provider.conciseness,
                name="Conciseness")
        .on_output()
    )

    """ provider = Huggingface()
    
    select_retriever_1 = Select.RecordCalls.bound.first.mapper.steps__.context.bound.default.last.collect()
    
    # Define a groundedness feedback function
    f_language_match = (
        Feedback(
            provider.language_match, name="Language Match"
        )
        .on_input_output()
    )
    f_groundedness = (
        Feedback(
            provider.groundedness_measure_with_nli, name="Groundedness"
        )
        .on(select_retriever_1)
        .on_output()
    )
    
    #f_answer_relevance = Feedback(provider.relevance).on_input_output()
    
    f_context_relevance = (
        Feedback(
            provider.context_relevance, name="Context Relevance"
        )
        .on_input()
        .on(select_retriever_1)
        .aggregate(np.mean)
    ) """
    
    tru_rag = TruChain(
        conversation,
        app_name="RAG",
        app_version="base",
        feedbacks=[f_groundedness
                   , f_context_relevance
                   #, f_language_match
                   ],
        selectors_check_warning=True
    )
    
    
    file = open("questions.txt", "r")
    questions = []

    while True:
        content = file.readline()
        if not content:
            break
        questions.append(content.strip())  # Using strip() to remove any newline characters

    file.close()
    chat_history = []
    
    with tru_rag as recording:
        for query in questions:
            conversation.invoke(
                {'input':  query + "\n Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>", "chat_history": chat_history}
            )
        
    session.get_leaderboard()
    run_dashboard(session)