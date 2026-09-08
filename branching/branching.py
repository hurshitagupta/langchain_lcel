import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch, RunnableLambda

from guards import validate_input, validate_output


load_dotenv()


model = ChatOpenRouter(
    api_key=os.environ["OPENROUTER_API_KEY"],
    model=os.environ["MODEL_NAME"],
    base_url=os.environ["BASE_URL"],
    timeout=20_000,
    max_retries=3,
    max_tokens=100,
    temperature=0
)


class Classify(BaseModel):
    classification: Literal["maths", "prose"] = Field(
        description="Classify the query as maths or prose"
    )


structured_model = model.with_structured_output(Classify)


classifier_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the user query as maths or prose"),
    ("human", "{q}")
])


classifier_chain = classifier_prompt | structured_model


maths_prompt = ChatPromptTemplate.from_messages([
    ("system", "Solve the maths question. Keep the answer short and precise."),
    ("human", "{q}")
])

maths_chain = maths_prompt | model | StrOutputParser()


prose_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's question. Keep the answer short and precise."),
    ("human", "{q}")
])

prose_chain = prose_prompt | model | StrOutputParser()


def is_maths(data: dict) -> bool:
    return data["classification"].classification == "maths"


validate_input_runnable = RunnableLambda(validate_input)
validate_output_runnable = RunnableLambda(validate_output)


chain = (
    validate_input_runnable
    | RunnablePassthrough.assign(
        classification=classifier_chain
    )
    | RunnableBranch(
        (is_maths, maths_chain),
        prose_chain
    )
    | validate_output_runnable
).with_retry(stop_after_attempt=3)


if __name__ == "__main__":

    user_input = input("Enter your query: ")

    result = chain.invoke({"q": user_input})

    print("\nRESULT:")
    print(result)

    print("\nCHAIN GRAPH:")
    print(chain.get_graph().draw_ascii())


