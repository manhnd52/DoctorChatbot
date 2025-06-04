from queryagent.agent import ask
from DatabaseConnector import run_query
from make_answer_easy_agent.agent import makeAnswerEasy

def AskAQuestion(question):
    query = ask(question)
    print(f"QUERY: {query}\n")
    queryResult = run_query(query)
    answer = makeAnswerEasy(question, query, str(queryResult))
    return {
        "query": query,
        "queryResult": queryResult,
        "answer": answer,
    }

