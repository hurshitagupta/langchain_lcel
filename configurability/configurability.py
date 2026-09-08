import os

from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.utils import ConfigurableField

from guards import validate_input, validate_output


load_dotenv()


model = ChatOpenRouter(
    api_key=os.environ["OPENROUTER_API_KEY"],
    model=os.environ["MODEL_NAME"],
    base_url=os.environ["BASE_URL"],
    temperature=0,
    timeout=20_000,
    max_retries=3,
    max_tokens=100
)


configurable_model = model.configurable_fields(
    model_name=ConfigurableField(
        id="model_name",
        name="Model Name",
        description="Model used for the request"
    ),
    temperature=ConfigurableField(
        id="temperature",
        name="Temperature",
        description="Controls randomness of the model"
    )
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an intelligent assistant. "
        "Keep the answer short and precise."
    ),
    ("human", "{q}")
])


validate_input_runnable = RunnableLambda(validate_input)
validate_output_runnable = RunnableLambda(validate_output)


chain = (
    validate_input_runnable
    | prompt
    | configurable_model
    | StrOutputParser()
    | validate_output_runnable
).with_retry(stop_after_attempt=3)


if __name__ == "__main__":

    user_input = input("Enter your query: ")
    data = {"q": user_input}

    print("\nDEFAULT CONFIGURATION:")
    print(f"Model: {os.environ['MODEL_NAME']}")
    print("Temperature: 0")

    default_result = chain.invoke(data)
    print(f"Result: {default_result}")

    print("\nRUNTIME CONFIGURATION:")
    print(f"Model: {os.environ['ALTERNATE_MODEL_NAME']}")
    print("Temperature: 0.7")

    configured_result = chain.invoke(
        data,
        config={
            "configurable": {
                "model_name": os.environ["ALTERNATE_MODEL_NAME"],
                "temperature": 0.7
            }
        }
    )

    print(f"Result: {configured_result}")
