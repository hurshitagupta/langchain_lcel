from langchain_core.runnables import RunnableLambda

def primary_model(data):
    print("Primary model called")
    raise ValueError("Primary Model Failed")

def fallback_model(data):
    print("Fallback model called")
    return "Fallback model succeeded"

primary_model_runnable = RunnableLambda(primary_model)

chain = (primary_model_runnable).with_retry(
    retry_if_exception_type=(ValueError,),
    stop_after_attempt=3
).with_fallbacks([RunnableLambda(fallback_model)])


if __name__ == "__main__":
    result = chain.invoke({"q": "Hello"})

    print("\nRESULT:")
    print(result)
