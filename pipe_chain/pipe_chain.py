from langchain_openrouter import ChatOpenRouter
from guards import validate_input, validate_output
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

validate_input_runnable = RunnableLambda(validate_input)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an intelligent person, you can answer any question asked by the user. Keep the answer short and precise"),
    ("human", "{q}")
])

model = ChatOpenRouter(
    api_key=os.environ["OPENROUTER_API_KEY"],
    model=os.environ["MODEL_NAME"],
    base_url=os.environ["BASE_URL"],
    max_retries=3,
    timeout=20_000,
    max_tokens=100
)

parser = StrOutputParser()

validate_output_runnable = RunnableLambda(validate_output)

chain = (validate_input_runnable | prompt | model | parser | validate_output_runnable).with_retry(stop_after_attempt=3)


if __name__ == "__main__":

    user_input = input("Enter your query: ")

    data = {"q": user_input}
    
    result = chain.invoke(data)

    print("RESULT:")
    print(result)

    print("\nCHAIN GRAPH:")
    print(chain.get_graph().draw_ascii())