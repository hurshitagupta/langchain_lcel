from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from guards import validate_input


def count_words(data: dict) -> int:
    return len(data["q"].split())


validate_input_runnable = RunnableLambda(validate_input)

chain = (
    validate_input_runnable
    | RunnablePassthrough.assign(
        word_count=RunnableLambda(count_words)
    )
)


if __name__ == "__main__":

    user_input = input("Enter your query: ")

    data = {"q": user_input}

    result = chain.invoke(data)

    print("RESULT:")
    print(result)

    print("\nCHAIN GRAPH:")
    print(chain.get_graph().draw_ascii())